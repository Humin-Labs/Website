# routes/activity_routes.py
from flask import render_template, redirect, request, session, flash, url_for, jsonify, abort
from datetime import datetime
import json

def register_activity_routes(app, db):
    """Registers all routes related to course activities."""

    from app import Course, Progress  # avoid circular import

    # ---------------------------------------------------------------------
    # UTILITY: Define ActivityProgress model dynamically if needed
    # ---------------------------------------------------------------------
    class ActivityProgress(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100))
        course_code = db.Column(db.String(10))
        current_step = db.Column(db.Integer, default=0)
        completed = db.Column(db.Boolean, default=False)

    # ✅ FIX: Create tables *inside* an app context so Gunicorn doesn’t crash
    with app.app_context():
        db.create_all()

    # ---------------------------------------------------------------------
    # ROUTE: Activity runner
    # ---------------------------------------------------------------------
    @app.route("/activity/<course_code>/<int:step>", methods=["GET", "POST"])
    def course_activity(course_code, step):
        """Handle individual activity step pages."""
        if "username" not in session:
            return redirect("/login")

        username = session["username"]
        course = Course.query.filter_by(code=course_code).first_or_404()

        # --------------------------------------------------------------
        # Select appropriate activity data
        # --------------------------------------------------------------
        if course.topic == "energy_and_matter":
            from modules.entry_ticket import ENTRY_TICKET_EAM
            activity_data = ENTRY_TICKET_EAM
        else:
            # Default fallback activity
            activity_data = [
                {
                    "title": "Testing to Robotics",
                    "body": "Robots are used in a variety of industries and can help assist humans in everyday tasks.",
                    "type": "info",
                }
            ]

        total_steps = len(activity_data)

        if step < 0 or step >= total_steps:
            return redirect(url_for("activity_complete", course_code=course_code))

        page = activity_data[step]

        # --------------------------------------------------------------
        # Handle POST (user clicked Next)
        # --------------------------------------------------------------
        if request.method == "POST":
            progress = Progress.query.filter_by(username=username, module=course.code).first()
            if not progress:
                progress = Progress(username=username, module=course.code, score=0)
                db.session.add(progress)

            progress.score = min(step + 1, total_steps)
            db.session.commit()

            # next step or finish
            if step + 1 >= total_steps:
                return redirect(url_for("activity_complete", course_code=course_code))
            else:
                return redirect(url_for("course_activity", course_code=course_code, step=step + 1))

        # --------------------------------------------------------------
        # Render vertical activity layout
        # --------------------------------------------------------------
        return render_template(
            "activity.html",
            course=course,
            step=step,
            total_steps=total_steps,
            page=page
        )

    # ---------------------------------------------------------------------
    # ROUTE: Completion page (no hardcoded next)
    # ---------------------------------------------------------------------
    @app.route("/activity/<course_code>/complete")
    def activity_complete(course_code):
        """Show clean completion screen (Return to Course only)."""
        course = Course.query.filter_by(code=course_code).first_or_404()

        # Optional: attempt to check if a “next_activity” exists in layout
        next_activity_url = None
        try:
            layout_json = None
            if hasattr(course, "layout") and course.layout:
                layout_json = json.loads(course.layout or "{}")
            if layout_json and "next_activity" in layout_json:
                next_activity_url = url_for("course_activity", course_code=course.code, step=0)
        except Exception:
            next_activity_url = None

        return render_template(
            "activity_complete.html",
            course=course,
            next_activity_url=next_activity_url
        )

    # ---------------------------------------------------------------------
    # OPTIONAL: API endpoint for AJAX checking of progress
    # ---------------------------------------------------------------------
    @app.route("/api/progress/<course_code>")
    def api_progress(course_code):
        """Return JSON with current progress."""
        if "username" not in session:
            abort(403)
        username = session["username"]
        progress = Progress.query.filter_by(username=username, module=course_code).first()
        if not progress:
            return jsonify({"progress": 0, "complete": False})
        return jsonify({
            "progress": progress.score,
            "complete": progress.score >= 1
        })

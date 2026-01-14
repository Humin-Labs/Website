# app.py
from flask import (
    Flask, render_template, request, redirect, session,
    jsonify, url_for, flash, abort, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func
import random, string, json

# ==========================================================
#  APP CONFIGURATION
# ==========================================================
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

app.secret_key = "replace_this_with_a_secure_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////opt/Website/database.db"
db = SQLAlchemy(app)

@app.context_processor
def inject_session():
    return dict(session=session)

# ==========================================================
#  MODELS
# ==========================================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default="student")

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    module = db.Column(db.String(100))
    score = db.Column(db.Integer)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    creator = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(50), nullable=False, default="energy_and_matter")

class CourseLayout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), nullable=False, index=True)
    layout_json = db.Column(db.Text, nullable=False, default="{}")
    updated_by = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

# ==========================================================
#  CORE ROUTES
# ==========================================================
@app.route("/")
def home():
    logged_in = "username" in session
    return render_template("index.html", logged_in=logged_in)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["username"] = username
            session["role"] = user.role
            return redirect("/")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if User.query.filter_by(username=username).first():
            return render_template("login.html", error="Username already exists", show_signup=True)
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = username
        session["role"] = role
        return redirect("/")
    return render_template("login.html", show_signup=True)

@app.route("/logout")
def logout():
    if "username" in session:
        username = session["username"]
        past_time = datetime.utcnow() - timedelta(minutes=10)
        for e in Progress.query.filter_by(username=username).all():
            e.last_seen = past_time
        db.session.commit()
        session.clear()
    return redirect("/")

# ==========================================================
#  MOBILE LAB SECTION
# ==========================================================
@app.route("/MobileLab")
def mobile_lab():
    if "username" not in session:
        return redirect("/login")
    return render_template("MobileLab.html")

@app.route("/circuits")
def circuits_page():
    return render_template("circuit_game.html")

@app.route("/mobilelab/forces_linkages")
def forces_linkages_index():
    return render_template("mobilelab/forces_linkages/index.html")

@app.route("/mobilelab/forces_linkages/<lesson_id>")
def forces_linkages_lesson(lesson_id):
    tmpl = f"mobilelab/forces_linkages/{lesson_id}.html"
    return render_template(tmpl)

@app.route("/mobilelab/forces_linkages/entry_ticket")
def forces_linkages_entry_ticket():
    return render_template("entry_tickets/FL_ticket_1.html", course={"code": "1G6EAI"})

@app.route("/mobilelab/forces_linkages/exit_ticket")
def forces_linkages_exit_ticket():
    return render_template("mobilelab/forces_linkages/lesson3.html")

@app.route("/mobilelab/entry_tickets/EaM_enTicket_1")
def energy_and_matter_entry_ticket():
    return render_template("entry_tickets/EaM_enTicket_1.html", course={"code": "1G6EAI"})

@app.route("/topbar")
def topbar_snippet():
    return render_template("includes/topbar.html")

# ==========================================================
#  HUMIN ACADEMY
# ==========================================================
@app.route("/HuminAcademy", methods=["GET", "POST"])
def humin_academy():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    role = session.get("role", "student")

    if request.method == "POST":
        if role == "teacher" and "course_name" in request.form:
            course_name = request.form["course_name"]
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            topic_guess = "energy_and_matter" if "energy" in course_name.lower() or "matter" in course_name.lower() else "robotics"
            new_course = Course(name=course_name, code=code, creator=username, topic=topic_guess)
            db.session.add(new_course)
            db.session.commit()
            flash(f"Created '{course_name}' — Course Code: {code}", "success")
        elif role == "student" and "course_code" in request.form:
            entered_code = request.form["course_code"]
            course = Course.query.filter_by(code=entered_code).first()
            flash(f"Joined course: {course.name}" if course else "Invalid course code.",
                  "success" if course else "error")

    courses = Course.query.filter_by(creator=username).all() if role == "teacher" else Course.query.all()
    for c in courses:
        c.student_count = Progress.query.filter_by(module=c.code).count()

    return render_template("HuminAcademy.html", role=role, courses=courses)

@app.route("/enter_course/<code>")
def enter_course(code):
    session["active_course"] = code
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    role = session.get("role", "student")
    course = Course.query.filter_by(code=code).first()
    if not course:
        flash("Course not found.", "error")
        return redirect(url_for("humin_academy"))

    prog = Progress.query.filter_by(username=username, module=course.code).first()
    if not prog:
        prog = Progress(username=username, module=course.code, score=0)
        db.session.add(prog)
    prog.last_seen = datetime.utcnow()
    db.session.commit()

    cutoff = datetime.utcnow() - timedelta(minutes=3)
    enrolled_students = Progress.query.filter_by(module=course.code).all()
    online_users = [s.username for s in enrolled_students if s.last_seen >= cutoff]

    existing_layout = CourseLayout.query.filter_by(course_code=course.code).order_by(CourseLayout.id.desc()).first()
    layout_json = existing_layout.layout_json if existing_layout else "{}"

    return render_template(
        "CourseView.html",
        course=course,
        role=role,
        enrolled_students=enrolled_students,
        online_users=online_users,
        current_user=username,
        layout_json=layout_json,
        current_progress=prog.score,
    )

# ==========================================================
#  START COURSE DAY
# ==========================================================
@app.route("/course/<code>/start/<int:day>")
def start_course_day(code, day):
    course = Course.query.filter_by(code=code).first_or_404()
    layout_record = CourseLayout.query.filter_by(course_code=code).order_by(CourseLayout.id.desc()).first()
    if not layout_record:
        abort(404, description="No layout found for this course")

    layout_data = json.loads(layout_record.layout_json or "{}")
    lanes = layout_data.get("lanes", [])
    if day < 1 or day > len(lanes):
        abort(404)

    lane = lanes[day - 1]
    modules = lane.get("items", [])
    first_step = 0
    username = session.get("username")
    progress = Progress.query.filter_by(username=username, module=code).first()
    if progress and progress.score:
        first_step = progress.score

    return redirect(url_for("course_activity", course_code=code, step=first_step, day=day))

# ==========================================================
#  COURSE LAYOUT API (for +Add Day / Deploy)
# ==========================================================
@app.route("/api/course/<code>/layout", methods=["GET"])
def get_course_layout(code):
    layout = CourseLayout.query.filter_by(course_code=code).order_by(CourseLayout.id.desc()).first()
    return jsonify({"layout": layout.layout_json if layout else "{}"})

@app.route("/api/course/<code>/layout", methods=["POST"])
def save_course_layout(code):
    if "username" not in session:
        return jsonify({"error": "not logged in"}), 403
    if session.get("role") != "teacher":
        return jsonify({"error": "only teachers can deploy"}), 403
    payload = request.get_json(silent=True) or {}
    rec = CourseLayout(course_code=code, layout_json=payload.get("layout", "{}"), updated_by=session["username"])
    db.session.add(rec)
    db.session.commit()
    return jsonify({"ok": True})

# ==========================================================
#  REGISTER ACTIVITY ROUTES
# ==========================================================
from routes.activity_routes import register_activity_routes
register_activity_routes(app, db)

# ==========================================================
#  HUMIN CAD ROUTES
# ==========================================================
@app.route("/cad")
def cad_page():
    """Serve main CAD app interface"""
    return send_from_directory("/opt/Website/static/cad", "index.html")

@app.route("/cad/<path:filename>")
def cad_static(filename):
    """Serve CAD static assets (bundles, libs, CSS)"""
    return send_from_directory("/opt/Website/huminlabs_jsketcher/dist", filename)

# ==========================================================
#  MAIN ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

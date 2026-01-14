# modules/entry_tickets/robotics.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# ==========================================================
# HUMIN Labs Entry Ticket — Robotics
# Default / Fallback Module
# ==========================================================

ENTRY_TICKET_ELECTRONICS = [
    {
        "type": "content",
        "title": "testing to Robotics",
        "body": (
            "Robots are used in a variety of industries and can help assist "
            "humans in everyday tasks."
        ),
    },
    {
        "type": "mcq",
        "title": "Purpose of Robotics",
        "stem": "Which of the following is a key benefit of robots in manufacturing?",
        "choices": [
            "They eliminate all human jobs",
            "They make production slower but safer",
            "They improve consistency and precision in repetitive tasks",
            "They replace computers in factories",
        ],
        "answer": 2,
    },
    {
        "type": "short",
        "prompt": "Describe one way robots are used in your community.",
    },
]


def init_models(db: SQLAlchemy):
    """Return the ActivityProgress model."""
    if "activity_progress" in db.metadata.tables:
        for cls in db.Model.registry._class_registry.values():
            if hasattr(cls, "__tablename__") and cls.__tablename__ == "activity_progress":
                return cls

    class ActivityProgress(db.Model):
        __tablename__ = "activity_progress"
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100))
        course_code = db.Column(db.String(10))
        step = db.Column(db.Integer)
        correct = db.Column(db.Boolean, default=False)
        text_response = db.Column(db.Text)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        completed = db.Column(db.Boolean, default=False)

    return ActivityProgress

# modules/entry_tickets/energy_and_matter.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# ==========================================================
# HUMIN Labs Entry Ticket — Energy and Matter
# Aligned with 2023 Alabama Course of Study: Science (Grades 6–8)
# ==========================================================

ENTRY_TICKET_EAM = [
    # --- Introductory Concept ---
    {
        "type": "content",
        "title": "What Is Energy?",
        "body": (
            "Energy is the ability to cause change or do work. "
            "It exists in many forms — light, heat, motion, and electricity — "
            "and can move from one object to another."
        ),
    },
    {
        "type": "mcq",
        "title": "Energy Example",
        "stem": "Which of the following demonstrates energy being used to do work?",
        "choices": [
            "A book resting on a table",
            "A student lifting a backpack",
            "A cold spoon sitting in water",
            "A pencil lying on a desk",
        ],
        "answer": 1,
    },

    # --- Transformation of Energy ---
    {
        "type": "content",
        "title": "Energy Transformations",
        "body": (
            "Energy can change from one form to another — for example, "
            "electrical energy can become light and heat energy in a lamp."
        ),
    },
    {
        "type": "mcq",
        "title": "Energy Conversion",
        "stem": "When you turn on a toaster, electrical energy is transformed into:",
        "choices": [
            "Sound energy",
            "Heat energy",
            "Nuclear energy",
            "Mechanical energy",
        ],
        "answer": 1,
    },

    # --- Conservation of Energy ---
    {
        "type": "content",
        "title": "Conservation of Energy",
        "body": (
            "Energy cannot be created or destroyed, only changed in form. "
            "This is known as the **Law of Conservation of Energy**."
        ),
    },
    {
        "type": "mcq",
        "title": "Energy Conservation Principle",
        "stem": "Which statement best describes the law of conservation of energy?",
        "choices": [
            "Energy disappears when work is done.",
            "Energy can be created by machines.",
            "Energy is reused by living organisms only.",
            "Energy changes form but the total amount stays the same.",
        ],
        "answer": 3,
    },

    # --- Matter and Energy Relationship ---
    {
        "type": "content",
        "title": "Matter and Energy",
        "body": (
            "All matter is made of particles in motion. "
            "The motion of these particles determines the temperature and state "
            "(solid, liquid, or gas) of the substance."
        ),
    },
    {
        "type": "mcq",
        "title": "Thermal Energy and Particles",
        "stem": "As the temperature of a solid increases, the particles:",
        "choices": [
            "Stop moving completely",
            "Move faster and farther apart",
            "Move slower and closer together",
            "Turn into light energy",
        ],
        "answer": 1,
    },

    # --- Multiple Concept Integration ---
    {
        "type": "multi",
        "title": "Forms of Energy",
        "stem": "Select all the forms of energy below.",
        "choices": ["Sound", "Heat", "Mass", "Light"],
        "answers": [0, 1, 3],
    },

    # --- Reflection / Open Response ---
    {
        "type": "short",
        "prompt": "Describe one example of how energy changes form in your daily life.",
    },
]


# ==========================================================
# Database Model Initialization
# ==========================================================
def init_models(db: SQLAlchemy):
    """Define and return the ActivityProgress model dynamically (only once)."""
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

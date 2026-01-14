# modules/entry_ticket.py
"""
Defines structured content for Energy and Matter Entry Ticket.
Each step is a dictionary with title, body, and (optional) options or image.
"""

ENTRY_TICKET_EAM = [
    {
        "title": "What Is Energy?",
        "body": "Energy is the ability to cause change or do work. "
                "It exists in many forms—light, heat, motion, and electricity—and "
                "can move from one object to another.",
        "type": "info"
    },
    {
        "title": "Forms of Energy",
        "body": "The main forms of energy are kinetic (motion), potential (stored), "
                "thermal, chemical, and electrical. All these forms can transform "
                "into one another depending on the system.",
        "type": "info"
    },
    {
        "title": "Energy Transfer",
        "body": "Energy can be transferred through conduction, convection, and radiation. "
                "In each case, energy moves from areas of higher energy to areas of lower energy.",
        "type": "info"
    },
    {
        "title": "Energy Transformation Example",
        "body": "When you turn on a light bulb, electrical energy transforms into "
                "light and heat energy — showing how energy changes form.",
        "type": "info"
    },
    {
        "title": "Energy in Everyday Life",
        "body": "We use energy for everything—from heating our homes to powering our phones. "
                "Understanding how energy moves helps us use it efficiently.",
        "type": "info"
    },
    {
        "title": "Energy Sources",
        "body": "Renewable sources (like solar and wind) replenish naturally, "
                "while non-renewable ones (like fossil fuels) can run out over time.",
        "type": "info"
    },
    {
        "title": "Law of Conservation of Energy",
        "body": "Energy cannot be created or destroyed; it only changes form. "
                "This means total energy in a closed system always stays the same.",
        "type": "info"
    },
    {
        "title": "Energy Efficiency",
        "body": "Some energy is always lost as heat during transformations, "
                "so improving efficiency reduces waste and conserves resources.",
        "type": "info"
    },
    {
        "title": "Check Your Understanding",
        "body": "Which of these is NOT a form of energy?",
        "options": [
            "Light",
            "Heat",
            "Sound",
            "Gravity"
        ],
        "type": "quiz"
    },
    {
        "title": "You're Ready!",
        "body": "You’ve completed the Energy and Matter Entry Ticket. "
                "Click next to finish.",
        "type": "complete"
    }
]

# modules/entry_tickets/__init__.py
"""
Initializes the HUMIN Labs entry ticket modules.

Each entry ticket corresponds to a curriculum topic and can be accessed dynamically
through the activity_routes.py logic. New tickets can be added by simply creating
a new module in this directory and importing it here.
"""

from .energy_and_matter import ENTRY_TICKET_EAM, init_models
from .robotics import ENTRY_TICKET_ELECTRONICS

__all__ = [
    "ENTRY_TICKET_EAM",
    "ENTRY_TICKET_ELECTRONICS",
    "init_models",
]

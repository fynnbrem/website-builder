"""Elements with pre-filled content."""

from elements.templates import get_header_with_icon
from src.util.tinyhtml_extended import h

CONTACT_HEADER = get_header_with_icon("Ansprechpartner", "face", outlined=False)
EVENT_HEADER = get_header_with_icon("Wann und Wo", "calendar_month")
AGE_HEADER = get_header_with_icon("Teilnehmeralter", "group")
REGISTRATION_HEADER = get_header_with_icon("Anmeldung", "app_registration")

GROUP_FULL = h("p")(
    "Unser Sportkurs ist aktuell voll. Sie können sich allerdings auf die Warteliste setzen lassen, und wir informieren Sie, sobald ein Platz frei wird."
)

PARA_SPACER = h("p")(
    h("span")()
)  # The para needs to contain something (the empty span) to work properly.
"""A spacer that matches the size of the bottom margin of a <p> element."""

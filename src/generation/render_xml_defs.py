"""Render XML page definitions into HTML.

This module dynamically parses any XML element by using varius parsers decorated with `element_parser`,
which in turn can be accessed via `parse_element` to return the HTML rendered by the passed element.
"""

import shutil
import xml.etree.ElementTree as ETree
from pathlib import Path
from typing import Callable

from tinyhtml import SupportsRender

import src.elements.constants as const
import src.elements.templates as tmpl
from elements.templates import horizontal_line
from generation.dedicated.all_pages import (
    generate_course_list_from_database,
    generate_aux_list_from_database,
)
from src.generation.database_parse import CONTACTS, LOCATIONS, get_style, get_head
from src.generation.dedicated.all_event_dates import (
    generate_date_tables_from_database,
)
from src.util.tinyhtml_extended import h, H
from util.path import get_page_file_name, get_page_files, Folders


def parse_xml(file: str | Path) -> ETree.Element:
    """Returns the root of the XML `file`."""
    tree = ETree.parse(file)
    return tree.getroot()


_ELEMENT_PARSERS: dict[str, Callable[[ETree.Element], SupportsRender]] = {
    "allEventDates": generate_date_tables_from_database,
    "allCourses": generate_course_list_from_database,
    "allAux": generate_aux_list_from_database,
}


def element_parser(*tags: str):
    """Decorated elements will be registered in `ELEMENT_PARSERS` under all `tags`."""

    def inner(func):
        """Register the `func` under all `tags`."""
        for tag in tags:
            _ELEMENT_PARSERS[tag] = func
        return func

    return inner


def convert_to_html(root: ETree.Element) -> str:
    """Converts the page definition into a complete HTML string including the necessary head and style."""
    body = root.find("body")
    appendix = root.find("appendix")

    return h("div")(
        # Get the meta elements.
        get_head(),
        get_style(),
        # Concatenate the body.
        (parse_element(e) for e in body),
        # Concatenate the appendix.
        (
            (parse_element(e) for e in get_appendix_elements(appendix))
            if appendix
            else None
        ),
    ).render()


def get_appendix_elements(appendix: ETree.Element) -> list[ETree.Element]:
    """Returns all defined elements in the `appendix` in the correct order."""
    elements = [
        appendix.find(t)
        for t in [
            # Show the most relevant information first.
            "eventData",
            "ageData",
            "registrationData",
            "contactData",
        ]
    ]

    return [e for e in elements if e is not None]


def parse_element(element: ETree.Element) -> SupportsRender:
    """Parse any element based on its tag.
    This accesses the parsers registered in `ELEMENT_PARSERS`."""
    return _ELEMENT_PARSERS[element.tag](element)


# noinspection PyMissingOrEmptyDocstring
@element_parser("opener")
def parse(element: ETree.Element) -> H:
    return tmpl.opener(element.text)


# noinspection PyMissingOrEmptyDocstring
@element_parser("para")
def parse(element: ETree.Element) -> H:
    return h("p")(element.text)


# noinspection PyMissingOrEmptyDocstring
@element_parser("div")
def parse(element: ETree.Element) -> H:
    return h("div")(element.text)


# noinspection PyMissingOrEmptyDocstring
@element_parser("header")
def parse(element: ETree.Element) -> H:
    return tmpl.header(element.text)


# noinspection PyMissingOrEmptyDocstring
@element_parser("largeHeader")
def parse(element: ETree.Element) -> H:
    return tmpl.large_header(element.text)


# noinspection PyMissingOrEmptyDocstring
@element_parser("centerImage")
def parse(element: ETree.Element) -> H:
    return tmpl.image(element.text, center=True)


# noinspection PyMissingOrEmptyDocstring
@element_parser("sideImage")
def parse(element: ETree.Element) -> H:
    return tmpl.image(element.text, center=False)


# noinspection PyMissingOrEmptyDocstring
@element_parser("ul", "ol")
def parse(element: ETree.Element) -> H:
    return h(element.tag, style={"margin-bottom": 4})(
        parse_element(e) for e in element.findall("li")
    )


# noinspection PyMissingOrEmptyDocstring
@element_parser("li")
def parse(element: ETree.Element) -> H:
    return h("li")(element.text)


# noinspection PyMissingOrEmptyDocstring
@element_parser("groupFull")
def parse(_: ETree.Element) -> H:
    return const.GROUP_FULL


# noinspection PyMissingOrEmptyDocstring
@element_parser("contactData")
def parse(element: ETree.Element) -> H:
    return h("div")(
        const.CONTACT_HEADER,
        h("div", style={"margin-left": 16})(
            (parse_element(c) for c in element),
        ),
    )


# noinspection PyMissingOrEmptyDocstring
@element_parser("registrationData")
def parse(element: ETree.Element) -> H:
    return h("div")(
        const.REGISTRATION_HEADER,
        h("div", style={"margin-left": 16})(
            (parse_element(c) for c in element),
        ),
    )


# noinspection PyMissingOrEmptyDocstring
@element_parser("primaryMail")
def parse(element: ETree.Element) -> H:
    return h("div", style={"margin-top": 4, "margin-bottom": 4})(
        (tmpl.contact_mail(element.text, bold=True))
    )


@element_parser("contact")
def parse(element: ETree.Element) -> H:
    """Renders a single <contact> with their name and contact methods."""
    contact = CONTACTS[element.text]
    return h("div")(
        tmpl.contact_name(contact.name),
        h("div", style={"margin-left": 8})(
            # Arrange the contact methods in a sensible manner (Likeliest method is mobile, then phone, then mail).
            tmpl.contact_mobile(contact.mobile) if contact.mobile is not None else None,
            tmpl.contact_phone(contact.phone) if contact.phone is not None else None,
            tmpl.contact_mail(contact.mail) if contact.mail is not None else None,
        ),
        const.PARA_SPACER,
    )


@element_parser("eventData")
def parse(element: ETree.Element) -> H:
    """Renders any amount of <eventGroup>s within this <eventData>.
    Multiple groups are separated by a horizontal line."""

    event_groups = element.findall("eventGroup")
    if len(event_groups) == 0:
        raise ValueError("Cannot render event data without any event groups.")

    return h("div")(
        const.EVENT_HEADER,
        parse_element(event_groups[0]),
        # Generate all groups after the first with a horizontal line above them.
        *[
            (
                horizontal_line(
                    margin_top=8, margin_bottom=8, margin_left=16, margin_right=16
                ),
                parse_element(e),
            )
            for e in event_groups[1:]
        ],
        const.PARA_SPACER,
    )


@element_parser("eventGroup")
def parse(element: ETree.Element) -> H:
    """Renders the <eventGroup> by showing all dates and the location associated with this group."""
    # Put the event dates into a list.
    event_dates = element.findall("eventDate")

    dates_listing = h("ul", style={"margin-bottom": 4})(
        h("li")(ed.text) for ed in event_dates
    )

    return h("div")(
        h("div", style={"margin-left": 16})(
            dates_listing,
            # Append the location info last.
            parse_element(element.find("eventLocation")),
        ),
    )


# noinspection PyMissingOrEmptyDocstring
@element_parser("eventLocation")
def parse(element: ETree.Element) -> H:
    key = element.text
    location = LOCATIONS[key]
    return tmpl.event_location(
        name=location.name, address=location.address, map_link=location.map_link
    )


# noinspection PyMissingOrEmptyDocstring
@element_parser("ageData")
def parse(element: ETree.Element) -> H:
    return h("div")(
        const.AGE_HEADER, h("div", style={"margin-left": 16})(tmpl.age(element.text))
    )


def render_page_def(file: Path) -> None:
    """Renders the page data specified in the `file`
    as HTML and stores the result in `./database/rendered/<pageId>.html`."""
    # Read the data file.
    root = parse_xml(file)
    id_ = root.find("meta/pageId")
    if id_ is None or id_.text is None or id_.text.strip() == "":
        raise ValueError("Page ID is undefined.")
    # Convert the data.
    html = convert_to_html(root)
    # Store the data.
    with open(
        Folders.rendered / get_page_file_name(id_.text), "w", encoding="utf-8"
    ) as stream:
        stream.write(html)


def render_all_page_defs() -> None:
    """Renders all page data defined in the `./database/pages` folder.
    This initially clears the folder where the files will be placed (`./database/rendered`)
    """
    shutil.rmtree(Folders.rendered)
    Folders.rendered.mkdir()

    for page in get_page_files():
        render_page_def(page)

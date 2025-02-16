"""Models and functions to help parse the content of the database."""
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ETree

from tinyhtml import raw

from src.util.tinyhtml_extended import H, h
from util.path import get_page_files, Folders


@dataclass(kw_only=True)
class Contact:
    """All data that defines a contact.
    All contact methods (mobile/phone/mail) are optional."""
    name: str
    key: str
    mobile: str | None
    phone: str | None
    mail: str | None


@dataclass(kw_only=True)
class Location:
    """All data that defines a location."""
    name: str
    key: str
    address: str
    map_link: str



def _text_if_exist(element: ETree.Element | None) -> str | None:
    """Returns the `text` of the `element` if the element exists."""
    if element is None:
        return None
    else:
        return element.text



def _parse_contacts() -> dict[str, Contact]:
    """Parses the `contacts.xml` from the database.
    The contacts are returned as `key:Contact`-mapping."""
    contacts = dict()

    file = r"database/contacts.xml"
    root = ETree.parse(file).getroot()
    contacts_elem = root.findall("contact")
    for ce in contacts_elem:
        key = _text_if_exist(ce.find("key"))
        name = _text_if_exist(ce.find("name"))
        if name is None or key is None:
            raise ValueError(f'Loosely defined contact. Name: "{name}". Key: "{key}".')

        contact = Contact(
            name=name,
            key=key,
            mobile=_text_if_exist(ce.find("mobile")),
            phone=_text_if_exist(ce.find("phone")),
            mail=_text_if_exist(ce.find("mail")),
        )

        contacts[key] = contact

    return contacts

CONTACTS: dict[str, Contact] = _parse_contacts()

def _parse_locations() -> dict[str, Location]:
    """Parses the `contacts.xml` from the database.
    The contacts are returned as `key:Location`-mapping."""

    locations = dict()

    file = r"database/locations.xml"
    root = ETree.parse(file).getroot()
    contacts_elem = root.findall("location")
    for ce in contacts_elem:
        key = _text_if_exist(ce.find("key"))
        name = _text_if_exist(ce.find("name"))
        if name is None or key is None:
            raise ValueError(f'Loosely defined location. Name: "{name}". Key: "{key}".')

        location = Location(
            name=name,
            key=key,
            address=_text_if_exist(ce.find("address")),
            map_link=_text_if_exist(ce.find("mapLink")),
        )

        locations[key] = location
    return locations

LOCATIONS: dict[str, Location] = _parse_locations()



def get_head() -> raw:
    """Gets the <head> for the document."""
    return raw(open(Folders.res / "head.html").read())


def get_style() -> H:
    """Gets the required <style> for the document."""
    style = open(Folders.res / "style.css").read()
    return h("style")(style)




def _get_id_to_title() -> dict[str, str]:
    """Returns all defined page IDs as mapping to their title."""
    mapping = dict()
    for file in get_page_files():
        title, id_ = get_title_and_id(file)
        mapping[id_] = title

    return mapping


def get_title_and_id(file: Path) -> tuple[str, str]:
    """Returns the page title and page ID as defined in the page data in the `file`."""
    root = ETree.parse(file).getroot()
    page_title = root.find("meta/pageTitle")
    page_id = root.find("meta/pageId")
    if page_id is None or page_title is None:
        raise ValueError(
            f'Loosely defined page data. Title: "{page_title}". ID: "{page_id}".'
        )
    return page_title.text, page_id.text


ID_TO_TITLE: dict[str, str] = _get_id_to_title()
"""All defined page IDs as mapping to their title."""

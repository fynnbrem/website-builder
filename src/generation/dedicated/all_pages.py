"""Generation of overview that lists all other pages."""
import xml.etree.ElementTree as ETree
from pathlib import Path

import elements.templates
from upload.upload import get_page_url
from util.path import get_page_files
from util.tinyhtml_extended import H, h

VALID_PAGE_TYPES = ["course", "aux", "overview"]


def get_metadata(file: Path) -> tuple[str, str, str]:
    """Returns the page title, page ID and page type as defined in the page data in the `file`."""
    root = ETree.parse(file).getroot()

    page_title = root.find("meta/pageTitle")
    page_id = root.find("meta/pageId")
    page_type = root.find("meta/pageType")

    if page_id is None or page_title is None or page_type is None:
        raise ValueError(
            f'Loosely defined page data. Title: "{page_title}". ID: "{page_id}".'
        )
    if page_type.text not in VALID_PAGE_TYPES:
        raise ValueError(f'Invalid page type: "{page_type}"')
    return page_title.text, page_id.text, page_type.text


def generate_course_list_from_database(_: ETree.Element) -> H:
    """Generates a list of all courses."""
    return _generate_page_list("course")

def generate_aux_list_from_database(_: ETree.Element) -> H:
    """Generates a list of all auxiliary pages (This does not include the overview page)."""
    return _generate_page_list("aux")


def _generate_page_list(page_type: str) -> H:
    """Generates a list of all pages that have the matching `page_type`.
    The entries will be sorted alphabetically by their title."""
    pages = [get_metadata(f) for f in get_page_files()]

    # Only keep courses.
    pages = [d for d in pages if d[2] == page_type]
    # Sort the courses alphabetically by title.
    pages = sorted(pages, key=lambda x: x[0])

    # Create the element containing links.
    # The links are created from the ID and display the title.
    return h("ul")(h("li")(elements.templates.get_link(get_page_url(i))(t)) for t, i, _ in pages)

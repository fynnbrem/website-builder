"""Common path operations, folder names and file names for the project."""

from pathlib import Path


class Folders:
    """Common folders used in the project."""

    res = Path() / "res"
    database = Path() / "database"
    rendered = database / "rendered"
    pages = database / "pages"


def _is_valid_page_file(file: Path) -> bool:
    return file.suffix == ".xml" and not file.name.startswith("_")


def get_page_files() -> list[Path]:
    """Returns all page definition files.
    This excludes files starting with an underscore."""
    return [f for f in Folders.pages.iterdir() if _is_valid_page_file(f)]


def get_page_file_name(page_id: str) -> str:
    """Streamlined function to generate the name for the generated HTML for a page."""
    return page_id + ".html"

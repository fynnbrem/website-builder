"""Handling the API routes and uploading the data."""
import os

import requests
from dotenv import load_dotenv
from requests import auth

from src.generation.database_parse import get_title_and_id
from util.path import get_page_file_name, Folders, get_page_files

load_dotenv()

AUTH = auth.HTTPBasicAuth(
    os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_API_KEY")
)
ORIGIN_URL =os.getenv("ORIGIN_URL")

def get_page_url(page_id: str) -> str:
    """Returns the URL to the page with the `page_id`."""
    return ORIGIN_URL + f"/?page_id={page_id}"


def get_api_url(page_id: str) -> str:
    """Returns the URL of the API for `page_id`."""
    return ORIGIN_URL + f"/wp-json/wp/v2/pages/{page_id}"


def get_page_title(url: str) -> str:
    """Returns the title in the response of the API `url`."""
    res = requests.get(url)
    res.raise_for_status()
    return res.json()["title"]["rendered"]


def validate_url_title(url: str, title: str) -> None:
    """Asserts that the API `url` responds with the expected `title`.

    :raises AssertionError:
        When the assertion failed."""
    fetched_title = get_page_title(url)
    assert get_page_title(url) == title, (
        "The URL you tried to access does not have the matching title.\n"
        "This is a safety mechanism, to fix this, check that the ID is still correct and update the database with the correct title.\n",
        f'Fetched title: "{fetched_title}". Defined title: "{title}"',
    )


def update_content(url: str, *, content: str, expected_title: str) -> None:
    """Updates the page at the API `url` with the content.
    Requires the `expected_title` to validate that the target page is the expected page.

    :raises HTTPError:
        When the API request fails."""
    validate_url_title(url, expected_title)
    payload = {"content": content}
    res = requests.put(url, json=payload, auth=AUTH)
    res.raise_for_status()


def update_all_content() -> None:
    """Updates all pages that have a defined XML with their rendered content defined in "./generated".
     This expects the rendered content files to have the name `<pageId>.html`.

     :raises HTTPError:
        When any API request fails.
        Note that any successful request until then will *not* be undone.
     """
    for page in get_page_files():
        page_title, page_id = get_title_and_id(page)

        html_file = Folders.rendered / get_page_file_name(page_id)
        html = open(html_file, encoding="utf-8").read()

        update_content(get_api_url(page_id), content=html, expected_title=page_title)


if __name__ == "__main__":
    update_all_content()

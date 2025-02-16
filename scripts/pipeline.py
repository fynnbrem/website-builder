"""Runs the entire conversion and upload pipeline for all defined pages in `./database/pages`.
This will first convert all pages in bulk and then upload them."""

from src.generation.render_xml_defs import render_all_page_defs
from src.upload.upload import update_all_content

if __name__ == "__main__":
    print("Starting Conversion")
    render_all_page_defs()
    print("Finished Conversion")
    print("Starting Upload")
    update_all_content()
    print("Finished Upload")

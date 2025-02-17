"""Generation of the tables used to display all event dates."""

import datetime
import xml.etree.ElementTree as ETree
from collections import defaultdict
from dataclasses import dataclass

import pandas as pd
from tinyhtml import SupportsRender, frag

import src.elements.templates as tmpl
from elements.templates import get_link
from generation.database_parse import LOCATIONS
from src.elements.templates import header
from src.generation.database_parse import ID_TO_TITLE
from src.upload.upload import get_page_url
from src.util.tinyhtml_extended import H, h
from util.path import Folders


@dataclass(kw_only=True)
class EventDate:
    """All data that defines an event date in the table.

    Must have either a `courseId` or `displayName` defined.
    If both are defined, the `displayName` will overwrite the `courseId`.
    """

    day: str
    startTime: datetime.time
    endTime: datetime.time
    courseId: str | None
    extraInfo: str | None
    displayName: str | None
    isCooperation: str
    location: str


DAY_TRANSLATE = {
    "monday": "Montag",
    "tuesday": "Dienstag",
    "wednesday": "Mittwoch",
    "thursday": "Donnerstag",
    "friday": "Freitag",
    "saturday": "Samstag",
    "sunday": "Sonntag",
}


def read_data() -> pd.DataFrame:
    """Reads the event data from the database."""
    df = pd.read_csv(
        Folders.database / "event_dates.csv",
        sep=";",
        dtype={
            "day": str,
            "startTime": str,
            "endTime": str,
            "courseId": str,
            "extraInfo": str,
            "displayName": str,
            "cooperation": bool,
            "location": str,
        },
    )
    df = df.where(pd.notna(df), None)
    return df


TIME_FORMAT = "%H:%M"


def cast_time(time: str) -> datetime.time:
    """Casts the `time`-string into a `datetime.time`."""
    return datetime.datetime.strptime(time, TIME_FORMAT).time()


def format_time(time: datetime.time) -> str:
    """Formats the `time` as `str`."""
    return time.strftime(TIME_FORMAT)


def by_start_time(event_date: EventDate) -> datetime.time:
    """Returns the `startTime` of the `ed`."""
    return event_date.startTime


def get_event_dates(df: pd.DataFrame) -> dict[str, dict[str, list[EventDate]]]:
    """Reads all event dates from the database.
    The dates will be sorted by their start time.

    :returns:
        The event days grouped first by location and then by day.
        `dict[<location>, dict[<day>, list[EventDate]]]`"""
    event_dates = defaultdict(lambda: defaultdict(list))
    for _, row in df.iterrows():
        data = row.to_dict()
        data["startTime"] = cast_time(data["startTime"])
        data["endTime"] = cast_time(data["endTime"])

        ed = EventDate(**data)
        event_dates[ed.location][ed.day].append(ed)
    for day_data in [
        day_data
        for location_data in event_dates.values()
        for day_data in location_data.values()
    ]:
        day_data.sort(key=by_start_time)

    # Cast the `defaultdict` back into a `dict` before returning.
    return {k: dict(v) for k, v in event_dates.items()}


def get_link_from_id(page_id) -> H:
    """Generate a hyperlink to the page with the `page_id`. The display text is the page's title."""
    return get_link(get_page_url(page_id))(ID_TO_TITLE[page_id])


def generate_table(event_dates: list[EventDate]) -> H:
    """Generate a table for a single day.
    This will render the dates in whichever order they were passed."""
    rows: list[SupportsRender] = list()
    for ed in event_dates:
        time = h("div")(
            format_time(ed.startTime),
            h("br"),
            "–" + format_time(ed.endTime),
        )

        # Get the name.
        # Take the display name or generate it from the ID.
        if ed.displayName is not None:
            name = ed.displayName
        else:
            name = get_link_from_id(ed.courseId)

        # Concatenate additional info for the text.
        sub_texts = list()
        if ed.isCooperation:
            sub_texts.append("(Kooperation, geschlossene Gruppe)")
        if ed.extraInfo is not None:
            sub_texts.append(ed.extraInfo)

        text = h("div")(name, *[(h("br"), st) for st in sub_texts])

        # Create the row.
        row = h("tr")(
            h("td")(time),
            h("td")(text),
        )
        rows.append(row)

    return h("table")(h("colgroup")(h("col", style={"width": 100})), rows)


def generate_tables_for_days(event_dates: dict[str, list[EventDate]]) -> frag:
    """Generates tables for each day defined in the `event_dates` using `generate_table()`.
    Each table gets the day as header."""
    elements: list[SupportsRender] = list()

    for day, events in event_dates.items():
        elements.append(header(DAY_TRANSLATE[day]))
        elements.append(generate_table(events))

    return frag(
        elements,
    )


def generate_tables_for_locations(
    event_dates: dict[str, dict[str, list[EventDate]]],
) -> H:
    """Generates tables for each location defined in the `event_dates` using `generate_tables_for_days()`.
    Each table group gets the location as header."""
    html = list()
    for location, location_data in event_dates.items():
        day_tables = generate_tables_for_days(location_data)
        location_name = LOCATIONS[location].name
        html.append(tmpl.large_header(f"Trainingszeiten {location_name}"))
        html.append(day_tables)

    return h("div")(*html)


def generate_date_tables_from_database(_: ETree.Element) -> H:
    """Generates the training date tables from the data in `database/event_dates.csv`."""
    data = read_data()
    event_data = get_event_dates(data)
    return generate_tables_for_locations(event_data)

# Website Builder

This project works as super-ordinated CMS for WordPress.

Here you can define style-agnostic XML files for your pages which will then be rendered as HTML and uploaded to their
corresponding page.

## Intent

This was made as WordPress does not work properly as CMS due to the non-separable editing of data and layout. In
contrast, this project enables you to exclusively edit the data and let the actual HTML be automatically generated.

This project is intended mostly for personal use and is highly specialized to render information about a sports course.
You can see an exemplary
result [here](https://www.tvjahn-bad-lippspringe.de/turnen/parkour/).

In this intent, most styles are hardcoded. But most elements don't have any style at all or just some loose styling, so
most styling will still come from whatever template is used.

## Usage

### Setup

You need a `.env` with the following keys:

- `WORDPRESS_USER`: Your WordPress username.
- `WORDPRESS_API_KEY`: Your WordPress API key (Any "Application Password").
- `ORIGIN_URL`: The URL on which your WordPress is hosted.

### Defining Page Defs

To define page defs, follow these steps:

1. The page must be created in WordPress so you can retrieve the ID and title.
2. Create a definition XML in `./database/pages`. The title may be arbitrary.
  - Filenames starting with an underscore will be ignored.

For details, refer to the exemplary def in [`./help/Example Page Def.xml`](./help/Example Page Def.xml).

### Defining Shared Data

There are some special data files which are used to generate specific, data-heavy XML elements.
These must all be located in `./database`. The files are:

- `contacts.xml`
    - All contact cards, for consistent representation of contacts.
- `locations.xml`
    - All location cards, for consistent representation of locations.
- `event_dates.csv`
    - All event dates, for generating an overview.

For details, refer to [`./help/Defining Shared Data.md`](./help/Defining Shared Data.md).

### Running the Pipeline

The pipeline consists of two steps:

1. Render all page data.
2. Upload all rendered page data.

To run the full pipeline, run [`./scripts/pipeline.py`](./scripts/pipeline.py).

## Limitations

Only the "content" part of the pages gets modified, this has some implications:

- The global style is still defined by the template.
- Defining document-wide CSS classes is very limited, inline-styles are preferred.
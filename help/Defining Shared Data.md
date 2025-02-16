# Defining Shared Data

Besides the page defs, there are also some specialized data files that either are more data-heavy than the defs or are shared among different page defs.

Here you find a guide on how to define and use the three specialized data files.
These three are:
- Contacts
- Locations
- Event Dates

## Contacts

- File: `./database/contacts.xml`
- Purpose: Centralized storage of contact info.\
They are accessed by the `<contact>`-tag.

### Example Content
```xml
<root>
    <contact>
        <key>mister_foo</key>
        <name>Mister Foo</name>
        <mobile>0123 456 7890</mobile>
        <mail>mister.foo@example.com</mail>
    </contact>
    <contact>
        <key>miss_foo</key>
        <name>Miss Foo</name>
        <phone>0123 456</phone>
    </contact>
</root>
```
A contact must at least have the `<key>` (For the defs to access it) and `<name>` (To display the name) children.
The other tags are contact methods and are completely optional.

Available contact methods are:
- "mail": E-Mail
- "mobile": Mobile Phone
- "phone": Phone

## Locations

- File: `./database/locations.xml`
- Purpose: Centralized storage of contact info.\
They are accessed by the `<location>`-tag.

### Example content
```xml
<root>
    <location>
        <key>my_location</key>
        <name>My Location</name>
        <address>Example Street 2, Exampleton</address>
        <mapLink>https://maps.app.goo.gl/example</mapLink>
    </location>
</root>
```
All children for the `<location>` are required.
The purpose of each tag is as follows:
- `<key>`: A unique key to identify the location from the page def.
- `<name>`: The display name.
- `<address>`: The human-readable address.
- `<mapLink>`: A google-maps link to the address.

## Event Dates
- File: `./database/event_dates.csv`
- Purpose: Listing of all event dates so they can be aggregated on a single page.\
The content will be rendered by the `<allEventDataes>`-tag.
- Format: Semicolon-separated CSV.

### Example Content

| day     | startTime | endTime | courseId | extraInfo      | displayName | isCooperation | location    |
|---------|-----------|---------|----------|----------------|-------------|---------------|-------------|
| monday  | 09:30     | 11:30   |          |                | Custom Name | 1             | my_location |
| tuesday | 16:30     | 17:30   | 1234     | Custom Subtext |             | 0             | my_location |

The `day` is used to create separate tables for each day.
The `courseId` will be used to automatically retrieve the title of the page, otherwise use `displayName`.
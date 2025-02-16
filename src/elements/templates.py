"""Element templates that require minimal data and provide a consistent appearance across the document."""

from tinyhtml import SupportsRender, frag

from util.tinyhtml_extended import H, h


def opener(content: str) -> H:
    """A centered, bold text."""
    return h("p", style={"text-align": "center", "font-size": 18})(h("strong")(content))


def horizontal_line(
    width: int | None = None,
    margin_bottom: int | None = None,
    margin_top: int | None = None,
    margin_left: int | None = None,
    margin_right: int | None = None,
) -> h:
    """A <hr> with easy-access styling."""
    style = dict()
    if width is not None:
        style["width"] = width
    if margin_bottom is not None:
        style["margin-bottom"] = margin_bottom
    if margin_top is not None:
        style["margin-top"] = margin_top
    if margin_left is not None:
        style["margin-left"] = margin_left
    if margin_right is not None:
        style["margin-right"] = margin_right
    return h("hr", style=style)


def image(link: str, *, center: bool) -> H:
    """Embeds the link as image with one of two styles (centered or right-aligned).
    :param link:
        The link to the image.
    :param center:
        Whether to display the image as centered or right-aligned."""
    return h("p")(
        h("a", href=link)(
            h(
                "img",
                klass="aligncenter" if center else "alignright",
                src=link,
                alt="",
                # Centered images are a centerpiece and should be wide.
                # Side images are just an extra and should be narrow.
                style={
                    "width": "80%" if center else "35%",
                    "height": "auto",
                    "box-shadow": "0 4px 10px rgba(0, 0, 0, 0.3)",
                    "border-radius": 3,
                },
            )
        )
    )


def contact_name(name: str) -> H:
    """Text with a small bottom margin to display the name of a contact."""
    return h("div", style={"margin-bottom": 4})(name)


def contact_phone(number: str) -> H:
    """The `number` with a phone icon.
    The `number` is also embedded as tel-hyperlink."""
    compact_number = number.replace(" ", "")
    return get_info_with_icon(
        get_link(f"tel:{compact_number}", new_tab=True)(number),
        "phone",
        outlined=False,
        # ↑ The outlined phone is rather thin, so use filled here.
    )


contact_mobile = contact_phone
"""The render for mobile and phone contact currently is the same.
This will change once the material UI font includes the WhatsApp icon."""


def contact_mail(address: str, bold=False) -> H:
    """The email `address` with an email icon.
    The `address` is embedded as mailto-hyperlink."""
    if bold:
        address = h("strong")(address)
    return get_info_with_icon(
        get_link(f"mailto:{address}", new_tab=True)(address),
        "alternate_email",
    )


def event_location(name: str, address: str, map_link: str) -> H:
    """Formats a location address as follows:
    1. A "location" icon.
    2. The `name` of the address.
    3. The exact `address` as hyperlink to the `map_link` in brackets."""
    address_html = frag(
        " " + name + " (",
        get_link(map_link, new_tab=True)(
            address,
        ),
        ")",
    )
    return h("div")(
        get_text_with_icon(
            address_html,
            icon="location_on",
            icon_size=18,
            outlined=False,
        ),
    )


def age(age_text: str) -> H:
    """The text in a <p> to display the age data."""
    return h("p")(age_text)


def header(title: SupportsRender) -> H:
    """A <div> with bold font and a medium bottom margin."""
    return h("div", style={"margin-bottom": 8})(h("strong")(title))


def large_header(title: SupportsRender) -> H:
    """A <div> with bold, large font and a large bottom margin."""
    return h("div", style={"font-size": 24, "margin-bottom": 16})(h("strong")(title))


def get_text_with_icon(
    content: SupportsRender,
    icon: str,
    icon_size: int,
    margin_bottom=0,
    margin_left=0,
    outlined=True,
) -> H:
    """Generates text with an icon in front of it.
    Both elements will be center aligned.

    :param content:
        The content to render.
    :param icon:
        The icon name.
        See https://fonts.google.com/icons.
    :param icon_size:
        The size of the icon in pixels.
    :param margin_bottom:
        The bottom margin.
    :param margin_left:
        The left margin.
    :param outlined:
        Whether to select the outlined or filled variant of the icon."""
    if outlined:
        klass = "material-icons-outlined"
    else:
        klass = "material-icons"
    return h("div", style={"align-items": "center", "display": "flex"})(
        h(
            "span",
            klass=klass,
            style={
                "font-size": icon_size,
                "margin-bottom": margin_bottom,
                "margin-left": margin_left,
            },
        )(icon),
        h("span", style={"margin-left": 4})(content),
    )


def get_header_with_icon(title: str, icon: str, outlined=True) -> H:
    """Bold text with a large sized icon."""
    return get_text_with_icon(
        h("strong")(title), icon, icon_size=32, margin_bottom=4, outlined=outlined
    )


def get_info_with_icon(title: str | H, icon: str, outlined=True) -> H:
    """Text with a medium-sized icon."""
    return get_text_with_icon(title, icon, icon_size=24, outlined=outlined)


def get_link(link: str, *, new_tab=False, no_opener: bool | None = None) -> h:
    """Generates an <a> element with a hyperlink.

    :param link:
        The link target.
    :param new_tab:
        Whether to open the link in a new tab.
    :param no_opener:
        Whether to use the "noopener" value.
        If set to none, this defaults to `true` if opening in a new tab and `false` otherwise.

    """
    if no_opener is None:
        no_opener = new_tab
    kwargs = {
        "href": link,
    }
    if new_tab:
        kwargs["target"] = "_blank"
    if no_opener:
        kwargs["rel"] = "noopener"

    return h("a", **kwargs)

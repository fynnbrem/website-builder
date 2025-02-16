"""Extension of the `tinhytml` package.
- Integrates the `style` keyword into `h` so now styles can be defined as
Python `dict` and will then be implicitly converted into an inline style.
"""

import tinyhtml

# noinspection PyProtectedMember
H = tinyhtml._h
"""Publicly accessible alias for `tinyhtml._h`."""


# noinspection PyPep8Naming
# (The name mimics the default name)
class h(tinyhtml.h):
    """Opens and closes an HTML element."""

    def __init__(self, __name: str, **attrs: tinyhtml.Attribute) -> None:
        if "style" in attrs:
            attrs["style"] = make_style(attrs["style"])

        super().__init__(__name, **attrs)


def make_style(style: dict[str, str | int]) -> str:
    """Converts the `dict` to CSS style definition.
    `int` values are interpreted as "px" units."""
    as_str = ""
    for k, v in style.items():
        if isinstance(v, int):
            if v == 0:
                v = "0"
            else:
                v = f"{v}px"
        as_str += f"{k}: {v}; "
    return as_str

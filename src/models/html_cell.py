from dataclasses import dataclass


@dataclass
class HtmlCell:

    text: str

    rag: str

    bg_colour: str | None = None

    font_colour: str | None = None
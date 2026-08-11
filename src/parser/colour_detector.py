import re


class ColourDetector:
    """
    Detects RAG status from HTML cell background colour.
    """

    GREEN = {
        "#00b050",
        "#92d050",
        "#47d459",
        "green",
        "rgb(0,176,80)"
    }

    AMBER = {
        "#ffc000",
        "#ffff00",
        "orange",
        "yellow",
        "rgb(255,192,0)"
    }

    RED = {
        "#ff0000",
        "#c00000",
        "red",
        "rgb(255,0,0)"
    }

    GREY = {
        "#bfbfbf",
        "#d9d9d9"
    }

    @staticmethod
    def detect(cell):

        background = None

        if cell.has_attr("bgcolor"):
            background = cell["bgcolor"]

        elif cell.has_attr("style"):

            match = re.search(
                r"background(?:-color)?\s*:\s*([^;]+)",
                cell["style"],
                re.IGNORECASE
            )

            if match:
                background = match.group(1).strip()

        if background is None:
            return None, None

        colour = background.lower().replace(" ", "")

        if colour in ColourDetector.GREEN:
            rag = "GREEN"

        elif colour in ColourDetector.AMBER:
            rag = "AMBER"

        elif colour in ColourDetector.RED:
            rag = "RED"

        elif colour in ColourDetector.GREY:
            rag = "GREY"

        else:
            rag = "UNKNOWN"

        return background, rag
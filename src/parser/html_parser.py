from bs4 import BeautifulSoup

from parser.colour_detector import ColourDetector
from models.html_cell import HtmlCell

import re


class HtmlParser:
    """
    Parses the HTML body and converts HTML tables
    into a matrix of HtmlCell objects.
    """

    def __init__(self, html: str):

        self.html = html

        self.soup = BeautifulSoup(html, "lxml")

    # ---------------------------------------------------------

    def get_tables(self):
        """
        Returns all HTML tables.
        """

        return self.soup.find_all("table")

    # ---------------------------------------------------------

    def table_to_matrix(self, table):
        """
        Converts one HTML table into a matrix of HtmlCell objects.

        Returns:
            List[List[HtmlCell]]
        """

        matrix = []

        rows = table.find_all("tr")

        for row in rows:

            row_data = []

            cells = row.find_all(["td", "th"])

            for cell in cells:

                text = cell.get_text(
                    separator=" ",
                    strip=True
                )

                bg_colour, rag = ColourDetector.detect(cell)

                font_colour = None

                if cell.has_attr("style"):

                    match = re.search(
                        r"color\s*:\s*([^;]+)",
                        cell["style"],
                        re.IGNORECASE
                    )

                    if match:

                        font_colour = match.group(1).strip()

                row_data.append(

                    HtmlCell(

                        text=text,

                        rag=rag,

                        bg_colour=bg_colour,

                        font_colour=font_colour

                    )

                )

            matrix.append(row_data)

        return matrix
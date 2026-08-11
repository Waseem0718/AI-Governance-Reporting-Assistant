import json
from pathlib import Path
from dataclasses import asdict


class JsonExporter:
    """
    Exports a RagReport object to JSON.
    """

    def __init__(self):

        self.output_folder = Path("output/json")
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def export(self, report):

        report_dict = asdict(report)

        filename = (
            report.received_date.strftime("%Y-%m-%d")
            if report.received_date
            else "unknown_date"
        )

        file_path = self.output_folder / f"{filename}.json"

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(
                report_dict,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        return file_path
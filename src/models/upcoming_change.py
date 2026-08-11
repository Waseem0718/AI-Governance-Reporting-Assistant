from dataclasses import dataclass


@dataclass
class UpcomingChange:

    area: str

    change_description: str

    planned_date: str

    change_number: str

    status: str
from dataclasses import dataclass


@dataclass
class Incident:

    serial_number: str

    zendesk: str

    system: str

    date: str

    problem_description: str

    raised_by: str

    next_steps: str
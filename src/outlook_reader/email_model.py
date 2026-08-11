from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmailModel:
    """
    Represents a single Outlook email.
    """

    subject: str
    sender: str
    received_time: datetime
    html_body: str
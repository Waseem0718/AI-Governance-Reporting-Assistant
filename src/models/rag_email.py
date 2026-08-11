from dataclasses import dataclass
from datetime import datetime


@dataclass
class RagEmail:
    """
    Represents one RAG report email.
    """

    file_name: str
    subject: str
    sender: str
    received_date: datetime | None
    html_body: str
    attachments: list[str]
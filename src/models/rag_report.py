from dataclasses import dataclass
from datetime import datetime

from models.infrastructure import Infrastructure
from models.vulnerability import Vulnerability
from models.upcoming_change import UpcomingChange
from models.incident import Incident
from models.development_activity import DevelopmentActivity
from models.vulnerability_finding import VulnerabilityFinding


@dataclass
class RagReport:

    report_id: str
    version: str
    generated_at: str

    subject: str
    sender: dict

    received_date: datetime
    report_date: str

    infrastructure: list[Infrastructure]
    vulnerabilities: list[Vulnerability]
    upcoming_changes: list[UpcomingChange]
    incidents: list[Incident]
    development_activities: list[DevelopmentActivity]
    vulnerability_findings: list[VulnerabilityFinding]
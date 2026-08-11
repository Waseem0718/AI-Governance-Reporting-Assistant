from parser.html_parser import HtmlParser

from parser.infrastructure_parser import InfrastructureParser
from parser.vulnerability_parser import VulnerabilityParser
from parser.upcoming_changes_parser import UpcomingChangesParser
from parser.incident_parser import IncidentParser
from parser.development_activity_parser import DevelopmentActivitiesParser
from parser.vulnerability_finding_parser import VulnerabilityFindingParser

from models.rag_report import RagReport

from datetime import datetime

from utils.sender_normalizer import SenderNormalizer


class ReportBuilder:
    """
    Builds one complete RagReport object
    from a RagEmail.
    """

    def __init__(self):

        self.infrastructure_parser = InfrastructureParser()

        self.vulnerability_parser = VulnerabilityParser()

        self.upcoming_changes_parser = UpcomingChangesParser()

        self.incident_parser = IncidentParser()

        self.development_activities_parser = DevelopmentActivitiesParser()
        
        self.vulnerability_finding_parser = VulnerabilityFindingParser()
        

    def build(self, email):
        

        parser = HtmlParser(email.html_body)

        tables = parser.get_tables()

        if len(tables) < 5:

            raise Exception(
                "Expected 5 tables in RAG report."
            )

        infrastructure = self.infrastructure_parser.parse(
            parser.table_to_matrix(tables[0])
        )

        vulnerabilities = self.vulnerability_parser.parse(
            parser.table_to_matrix(tables[1])
        )
        
        vulnerability_findings = []

        for queue in vulnerabilities:

            vulnerability_findings.extend(

                self.vulnerability_finding_parser.parse(

                    queue.queue_name,

                    queue.top_fixes

                )

            )

        upcoming_changes = self.upcoming_changes_parser.parse(
            parser.table_to_matrix(tables[2])
        )

        incidents = self.incident_parser.parse(
            parser.table_to_matrix(tables[3])
        )

        development_activities = self.development_activities_parser.parse(
            parser.table_to_matrix(tables[4])
        )
        

        return RagReport(

            report_id=f"RAG-{email.received_date.strftime('%Y%m%d')}",

            version="1.0",

            generated_at=datetime.now().isoformat(),

            subject=email.subject.replace("\x00", "").strip(),

            sender=SenderNormalizer.normalize(email.sender),

            received_date=email.received_date,
            
            report_date=email.received_date.strftime("%Y-%m-%d"),
            
            infrastructure=infrastructure,

            vulnerabilities=vulnerabilities,

            upcoming_changes=upcoming_changes,

            incidents=incidents,

            vulnerability_findings=vulnerability_findings,

            development_activities=development_activities
            
            

        )
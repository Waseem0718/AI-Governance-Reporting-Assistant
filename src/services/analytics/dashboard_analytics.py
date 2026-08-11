from analytics.infrastructure_analytics import InfrastructureAnalytics
from analytics.vulnerability_analytics import VulnerabilityAnalytics
from analytics.incident_analytics import IncidentAnalytics
from analytics.change_analytics import ChangeAnalytics
from analytics.development_analytics import DevelopmentAnalytics


class DashboardAnalytics:

    def __init__(self, repository):

        self.infrastructure = InfrastructureAnalytics(repository)
        self.vulnerability = VulnerabilityAnalytics(repository)
        self.incident = IncidentAnalytics(repository)
        self.change = ChangeAnalytics(repository)
        self.development = DevelopmentAnalytics(repository)

    def build(self):

        return {

            "infrastructure":
                self.infrastructure.latest_summary(),

            "vulnerabilities":
                self.vulnerability.latest_summary(),

            "incidents":
                self.incident.latest_summary(),

            "changes":
                self.change.latest_summary(),

            "development":
                self.development.latest_summary()
        }
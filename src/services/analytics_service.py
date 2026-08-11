class AnalyticsService:

    def __init__(self, repository):

        self.repository = repository

    # -----------------------------------------------------
    # Reports
    # -----------------------------------------------------

    def get_latest_report(self):

        return self.repository.report_repository.get_latest_report()

    # -----------------------------------------------------
    # Infrastructure
    # -----------------------------------------------------

    def get_latest_infrastructure(self, report_id):

        return self.repository.infrastructure_repository.get_latest_infrastructure(report_id)

    def get_infrastructure_summary(self, report_id):

        return {

            "overall_status":
                self.repository.infrastructure_repository.get_overall_status(report_id),

            "status_summary":
                self.repository.infrastructure_repository.get_status_summary(report_id),

            "amber_systems":
                self.repository.infrastructure_repository.get_amber_systems(report_id),

            "grey_systems":
                self.repository.infrastructure_repository.get_grey_systems(report_id),

            "attention_required":
                self.repository.infrastructure_repository.get_non_green_systems(report_id)

        }

    # -----------------------------------------------------
    # Vulnerabilities
    # -----------------------------------------------------

    def get_latest_vulnerabilities(self, report_id):

        return self.repository.vulnerability_repository.get_latest(report_id)

    def get_vulnerability_summary(self, report_id):

        return self.repository.vulnerability_repository.get_latest_summary(report_id)

    def get_normalized_vulnerabilities(self, report_id):

        return self.repository.vulnerability_finding_repository.get_latest(report_id)

    # -----------------------------------------------------
    # Incidents
    # -----------------------------------------------------

    def get_latest_incidents(self):

        return self.repository.incident_repository.get_latest()

    # -----------------------------------------------------
    # Upcoming Changes
    # -----------------------------------------------------

    def get_latest_changes(self):

        return self.repository.upcoming_changes_repository.get_latest()

    # -----------------------------------------------------
    # Development Activities
    # -----------------------------------------------------

    def get_latest_development(self):

        return self.repository.development_repository.get_latest()

    # -----------------------------------------------------
    # Dashboard
    # -----------------------------------------------------

    def get_dashboard(self, report_id):

        return {

            "report":
                self.get_latest_report(),

            "infrastructure":
                self.get_infrastructure_summary(report_id),

            "vulnerabilities":
                self.get_vulnerability_summary(report_id),

            "incidents":
                self.get_latest_incidents(),

            "changes":
                self.get_latest_changes(),

            "development":
                self.get_latest_development()

        }

    # -----------------------------------------------------
    # AI Context
    # -----------------------------------------------------

    def get_context(self, report_id):

        return {

            "report":
                self.get_latest_report(),

            "infrastructure":
                self.get_infrastructure_summary(report_id),

            "vulnerabilities":
                self.get_vulnerability_summary(report_id),

            "normalized_vulnerabilities":
                self.get_normalized_vulnerabilities(report_id),

            "incidents":
                self.get_latest_incidents(),

            "changes":
                self.get_latest_changes(),

            "development":
                self.get_latest_development()

        }
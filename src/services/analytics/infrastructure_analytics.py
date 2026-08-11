class InfrastructureAnalytics:

    def __init__(self, repository):
        self.repo = repository.infrastructure_repository
        self.report_repo = repository.report_repository

    def latest_summary(self):

        latest = self.report_repo.get_latest_report()

        report_id = latest["report_id"]

        return {

            "overall_status":
                self.repo.get_overall_status(report_id),

            "status_summary":
                self.repo.get_status_summary(report_id),

            "non_green":
                self.repo.get_non_green_systems(report_id),

            "amber":
                self.repo.get_amber_systems(report_id),

            "grey":
                self.repo.get_grey_systems(report_id)
        }
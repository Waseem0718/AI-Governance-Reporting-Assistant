class DevelopmentAnalytics:

    def __init__(self, repository):

        self.repo = repository.development_repository
        self.report_repo = repository.report_repository

    def latest_summary(self):

        latest = self.report_repo.get_latest_report()

        report_id = latest["report_id"]

        activities = self.repo.get_by_report(report_id)

        return {

            "total": len(activities),

            "activities": activities
        }
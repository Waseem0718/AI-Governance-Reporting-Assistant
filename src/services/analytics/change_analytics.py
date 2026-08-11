class ChangeAnalytics:

    def __init__(self, repository):

        self.repo = repository.upcoming_changes_repository
        self.report_repo = repository.report_repository

    def latest_summary(self):

        latest = self.report_repo.get_latest_report()

        report_id = latest["report_id"]

        changes = self.repo.get_by_report(report_id)

        return {

            "total": len(changes),

            "changes": changes
        }
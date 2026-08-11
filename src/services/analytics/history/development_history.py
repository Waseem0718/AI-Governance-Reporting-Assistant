class DevelopmentHistory:
    """
    Performs historical analysis on Development Activities.
    """

    def __init__(self, repository):

        self.repository = repository

    # ---------------------------------------------------------
    # Raw History
    # ---------------------------------------------------------

    def _history(self, application):

        return self.repository.development_repository.get_application_history(
            application
        )

    # ---------------------------------------------------------
    # Latest Activity
    # ---------------------------------------------------------

    def get_latest_status(self, application):

        return self.repository.development_repository.get_latest_by_application(
            application
        )

    # ---------------------------------------------------------
    # Unique Updates
    # ---------------------------------------------------------

    def get_unique_updates(self, application):

        rows = self._history(application)

        unique = {}

        for row in rows:

            key = row["activity"].strip().lower()

            unique[key] = row

        return list(unique.values())

    # ---------------------------------------------------------
    # Completed Work
    # ---------------------------------------------------------

    def get_completed_work(self, application):

        rows = self._history(application)

        completed = []

        completed_keywords = [

            "completed",
            "deployed",
            "successful",
            "working as expected",
            "implemented",
            "finished"

        ]

        for row in rows:

            text = (
                row["activity"] + " " + row["status"]
            ).lower()

            if any(word in text for word in completed_keywords):

                completed.append(row)

        return completed

    # ---------------------------------------------------------
    # Pending Work
    # ---------------------------------------------------------

    def get_pending_work(self, application):

        rows = self._history(application)

        pending = []

        pending_keywords = [

            "testing",
            "progress",
            "pending",
            "ongoing",
            "started",
            "in progress",
            "monitoring",
            "business testing"

        ]

        for row in rows:

            text = (
                row["activity"] + " " + row["status"]
            ).lower()

            if any(word in text for word in pending_keywords):

                pending.append(row)

        return pending

    # ---------------------------------------------------------
    # Complete History Object
    # ---------------------------------------------------------

    def get_application_history(self, application):

        return {

            "application": application,

            "history":
                self._history(application),

            "latest":
                self.get_latest_status(application),

            "completed":
                self.get_completed_work(application),

            "pending":
                self.get_pending_work(application),

            "unique_updates":
                self.get_unique_updates(application)

        }

    # ---------------------------------------------------------
    # Monthly Summary
    # ---------------------------------------------------------

    def get_monthly_summary(self, application):

        history = self.get_application_history(application)

        return {

            "application": application,

            "latest":
                history["latest"],

            "completed":
                history["completed"],

            "pending":
                history["pending"],

            "unique_updates":
                history["unique_updates"]

        }

    # ---------------------------------------------------------
    # Dashboard Summary
    # ---------------------------------------------------------

    def get_summary(self, application):

        history = self.get_application_history(application)

        return {

            "application": application,

            "total_updates":
                len(history["history"]),

            "unique_updates":
                len(history["unique_updates"]),

            "completed_updates":
                len(history["completed"]),

            "pending_updates":
                len(history["pending"]),

            "latest":
                history["latest"]

        }

    # ---------------------------------------------------------
    # Lookup Helpers
    # ---------------------------------------------------------

    def get_applications(self):

        return self.repository.development_repository.get_applications()

    def get_activity_types(self, application):

        activities = self._history(application)

        return sorted(

            {

                activity["activity_type"]

                for activity in activities

            }

        )

    def get_environments(self, application):

        activities = self._history(application)

        return sorted(

            {

                activity["environment"]

                for activity in activities

            }

        )

    def get_activity_type_history(self, activity_type):

        return self.repository.development_repository.get_by_activity_type(
            activity_type
        )

    def get_environment_history(self, environment):

        return self.repository.development_repository.get_by_environment(
            environment
        )
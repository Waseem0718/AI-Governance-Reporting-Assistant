from difflib import SequenceMatcher


class DevelopmentEvolution:

    def __init__(self, repository):

        self.repository = repository

    # -----------------------------------------------------
    # All activities of an application
    # -----------------------------------------------------

    def _activities(self, application):

        return self.repository.development_repository.get_by_application(
            application
        )

    # -----------------------------------------------------
    # Similarity
    # -----------------------------------------------------

    def _is_similar(self, text1, text2, threshold=0.80):

        return SequenceMatcher(

            None,

            text1.lower(),

            text2.lower()

        ).ratio() >= threshold

    # -----------------------------------------------------
    # New Updates
    # -----------------------------------------------------

    def get_new_updates(self, application):

        activities = self._activities(application)

        updates = []

        for activity in activities:

            found = False

            for existing in updates:

                if self._is_similar(

                    activity["activity"],

                    existing["activity"]

                ):

                    found = True
                    break

            if not found:

                updates.append(activity)

        return updates

    # -----------------------------------------------------
    # Completed Activities
    # -----------------------------------------------------

    def get_completed_updates(self, application):

        activities = self._activities(application)

        completed_keywords = [

            "completed",
            "complete",
            "successful",
            "success",
            "closed",
            "implemented",
            "deployed in prod",
            "business confirmed"

        ]

        completed = []

        for activity in activities:

            text = (

                activity["activity"] + " " +

                activity["status"]

            ).lower()

            if any(keyword in text for keyword in completed_keywords):

                completed.append(activity)

        return completed

    # -----------------------------------------------------
    # Pending Activities
    # -----------------------------------------------------

    def get_pending_updates(self, application):

        activities = self._activities(application)

        pending_keywords = [

            "testing",
            "business testing",
            "in progress",
            "progress",
            "ongoing",
            "pending",
            "planned",
            "waiting",
            "yet to",
            "monitoring"

        ]

        pending = []

        for activity in activities:

            text = (

                activity["activity"] + " " +

                activity["status"]

            ).lower()

            if any(keyword in text for keyword in pending_keywords):

                pending.append(activity)

        return pending

    # -----------------------------------------------------
    # Latest Activity
    # -----------------------------------------------------

    def get_latest_updates(self, application):

        activities = self._activities(application)

        if not activities:

            return []

        return [activities[-1]]

    # -----------------------------------------------------
    # Activity Timeline
    # -----------------------------------------------------

    def get_activity_progress(self, application):

        return self._activities(application)

    # -----------------------------------------------------
    # Status Evolution
    # -----------------------------------------------------

    def get_status_changes(self, application):

        activities = self._activities(application)

        history = []

        for activity in activities:

            history.append(

                {

                    "report_id": activity["report_id"],

                    "activity": activity["activity"],

                    "status": activity["status"]

                }

            )

        return history

    # -----------------------------------------------------
    # Environment Evolution
    # -----------------------------------------------------

    def get_environment_changes(self, application):

        activities = self._activities(application)

        history = []

        for activity in activities:

            history.append(

                {

                    "report_id": activity["report_id"],

                    "activity": activity["activity"],

                    "environment": activity["environment"]

                }

            )

        return history

    # -----------------------------------------------------
    # Complete Evolution
    # -----------------------------------------------------

    def get_application_evolution(self, application):

        return {

            "application": application,

            "new_updates":
                self.get_new_updates(application),

            "completed":
                self.get_completed_updates(application),

            "pending":
                self.get_pending_updates(application),

            "latest":
                self.get_latest_updates(application),

            "status_changes":
                self.get_status_changes(application),

            "environment_changes":
                self.get_environment_changes(application)

        }

    # -----------------------------------------------------
    # AI Summary
    # -----------------------------------------------------

    def get_monthly_summary(self, application):

        evolution = self.get_application_evolution(application)

        return {

            "application": application,

            "total_updates":
                len(self._activities(application)),

            "unique_updates":
                len(evolution["new_updates"]),

            "completed_updates":
                len(evolution["completed"]),

            "pending_updates":
                len(evolution["pending"]),

            "latest_update":
                evolution["latest"],

            "updates":
                evolution["new_updates"]

        }
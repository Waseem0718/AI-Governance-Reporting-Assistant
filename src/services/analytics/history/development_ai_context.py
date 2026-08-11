from services.analytics.history.development_history import DevelopmentHistory
from services.analytics.history.development_evolution import DevelopmentEvolution


class DevelopmentAIContext:

    def __init__(self, repository):

        self.history = DevelopmentHistory(repository)
        self.evolution = DevelopmentEvolution(repository)

    # -----------------------------------------------------
    # Complete AI Context for an Application
    # -----------------------------------------------------

    def build_context(self, application):

        history = self.history.get_application_history(application)

        evolution = self.evolution.get_application_evolution(application)

        return {

            "application": application,

            # Historical Information
            "latest_update":
                history["latest"],

            "unique_updates":
                history["unique_updates"],

            "pending_updates":
                history["pending"],

            "completed_updates":
                history["completed"],

            # Evolution
            "new_updates":
                evolution["new_updates"],

            "status_changes":
                evolution["status_changes"],

            "environment_changes":
                evolution["environment_changes"],

            # Metadata
            "total_updates":
                len(history["history"]),

            "activity_types":
                self.history.get_activity_types(application),

            "environments":
                self.history.get_environments(application)

        }

    # -----------------------------------------------------
    # AI Context for all Applications
    # -----------------------------------------------------

    def build_all_context(self):

        contexts = []

        for application in self.history.get_applications():

            contexts.append(

                self.build_context(application)

            )

        return contexts

    # -----------------------------------------------------
    # Context by Activity Type
    # -----------------------------------------------------

    def build_activity_context(self, activity_type):

        return self.history.get_activity_type_history(
            activity_type
        )

    # -----------------------------------------------------
    # Context by Environment
    # -----------------------------------------------------

    def build_environment_context(self, environment):

        return self.history.get_environment_history(
            environment
        )
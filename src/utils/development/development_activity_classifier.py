from utils.development.activity_type_extractor import ActivityTypeExtractor
from utils.development.environment_extractor import EnvironmentExtractor
from utils.development.status_normalizer import StatusNormalizer


class DevelopmentActivityClassifier:

    @classmethod
    def classify(cls, application, activity, status):

        activity = activity or ""
        status = status or ""

        # --------------------------------------------------
        # Activity Type
        # --------------------------------------------------

        activity_type = ActivityTypeExtractor.extract(activity)

        # --------------------------------------------------
        # Environment
        # --------------------------------------------------

        environment = EnvironmentExtractor.extract(
            application,
            activity,
            status
        )

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        # First try the source status
        normalized_status = StatusNormalizer.normalize(status)

        # If source status is Unknown, derive status
        # from the activity text.
        if normalized_status == "Unknown":

            normalized_status = StatusNormalizer.normalize(
                activity
            )

        return {

            "activity_type": activity_type,

            "environment": environment,

            "status": normalized_status

        }
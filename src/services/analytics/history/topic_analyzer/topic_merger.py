class TopicMerger:
    """
    Groups development activities by application.

    Governance topics are application-centric.

    The application field from the development activity is treated as
    the source of truth for governance grouping.

    Example:

        Licensing
            ├── Release
            ├── Testing
            ├── Deployment
            └── Rollback

        PTX
            ├── Migration
            └── Testing

    Release, API, Migration, Infrastructure, Rollback, etc. are
    activities/details within an application and must not become
    separate governance topics.
    """

    UNKNOWN_APPLICATION = "Unclassified"

    @classmethod
    def merge(cls, extracted_activities):
        """
        Group extracted development activities by application.

        Parameters
        ----------
        extracted_activities : list[dict]
            List of extracted development activity dictionaries.

        Returns
        -------
        list[dict]
            Application-level topics in the format expected by
            TimelineBuilder.

        Example output:

        [
            {
                "topic_name": "Licensing",
                "representative": {...},
                "activities": [...]
            },
            {
                "topic_name": "PTX",
                "representative": {...},
                "activities": [...]
            }
        ]
        """

        topics = {}

        for activity in extracted_activities:

            application = cls._get_application(activity)

            if application not in topics:

                topics[application] = {
                    "topic_name": application,
                    "representative": activity,
                    "activities": []
                }

            topics[application]["activities"].append(activity)

        return list(topics.values())

    # ---------------------------------------------------------
    # Get application
    # ---------------------------------------------------------

    @classmethod
    def _get_application(cls, activity):
        """
        Get the governance application from the development activity.

        Priority:

        1. application field
        2. applications list
        3. Unclassified

        The application column is treated as the primary source of truth.
        """

        # -----------------------------------------------------
        # 1. Primary source: application field
        # -----------------------------------------------------

        application = activity.get("application")

        if application:

            application = str(application).strip()

            if application:
                return application

        # -----------------------------------------------------
        # 2. Fallback: applications list
        # -----------------------------------------------------

        applications = activity.get("applications", [])

        if applications:

            valid_applications = [

                str(app).strip()

                for app in applications

                if app and str(app).strip()

            ]

            if len(valid_applications) == 1:

                return valid_applications[0]

            if len(valid_applications) > 1:

                # Multiple applications were detected.
                # Do not arbitrarily select one.
                return cls._handle_multiple_applications(
                    valid_applications
                )

        # -----------------------------------------------------
        # 3. No application available
        # -----------------------------------------------------

        return cls.UNKNOWN_APPLICATION

    # ---------------------------------------------------------
    # Multiple applications
    # ---------------------------------------------------------

    @classmethod
    def _handle_multiple_applications(cls, applications):
        """
        Handle an activity where multiple applications are detected.

        For the first refinement, we keep the activity together rather
        than incorrectly assigning it to one application.

        Example:

            ["Licensing", "PTX"]

        becomes:

            "Licensing / PTX"

        This makes the situation visible and prevents silent
        misclassification.
        """

        unique_applications = sorted(
            set(applications)
        )

        return " / ".join(unique_applications)
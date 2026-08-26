from datetime import datetime


class AIContextBuilder:
    """
    Converts Development Evolution into a detailed,
    factual and AI-ready governance context.

    Design goals
    ------------

    1. Preserve application/topic level structure.
    2. Preserve all meaningful business changes.
    3. Preserve status/environment/activity-type progression.
    4. Preserve releases, APIs, business objects, technologies,
       infrastructure and integrations.
    5. Preserve useful activity evidence for each application.
    6. Avoid excessive compression of governance information.
    7. Provide enough context for the LLM to produce
       application-specific governance narratives.
    8. Remain completely LLM-independent.
    """

    # =========================================================
    # PUBLIC BUILDER
    # =========================================================

    @classmethod
    def build(cls, evolutions):

        contexts = []

        for evolution in evolutions:

            context = {
                "topic": evolution.get("topic"),

                # High-level period information
                "timeline_summary":
                    cls._build_timeline_summary(evolution),

                # Human-readable evolution
                "business_story":
                    cls._build_business_story(evolution),

                # Latest known business state
                "current_state":
                    cls._build_current_state(evolution),

                # Important governance milestones
                "business_milestones":
                    cls._build_business_milestones(evolution),

                # Detailed activities/evidence
                "activity_details":
                    cls._build_activity_details(evolution),

                # Status movement
                "status_progression":
                    cls._build_status_progression(evolution),

                # Environment movement
                "environment_progression":
                    cls._build_environment_progression(evolution),

                # Activity type movement
                "activity_type_progression":
                    cls._build_activity_type_progression(evolution),

                # All meaningful changes
                "important_changes":
                    cls._build_important_changes(evolution),

                # Consolidated governance evidence
                "governance_evidence":
                    cls._build_governance_evidence(evolution),

                # Application-specific narrative material
                "application_summary":
                    cls._build_application_summary(evolution)
            }

            contexts.append(context)

        return contexts

    # =========================================================
    # BUSINESS STORY
    # =========================================================

    @classmethod
    def _build_business_story(cls, evolution):

        story = []

        for item in evolution.get("evolution", []):

            item_type = item.get("type")

            # -------------------------------------------------
            # Stable period
            # -------------------------------------------------

            if item_type == "Stable":

                start = cls._format_date(
                    item.get("start_date")
                )

                end = cls._format_date(
                    item.get("end_date")
                )

                if start == end:

                    story.append(
                        f"{start} : "
                        f"Business remained stable."
                    )

                else:

                    story.append(
                        f"{start} to {end} : "
                        f"Business remained stable."
                    )

                continue

            # -------------------------------------------------
            # Business change
            # -------------------------------------------------

            if item_type == "Business Change":

                date = cls._format_date(
                    item.get("date")
                )

                changes = item.get(
                    "changes",
                    []
                )

                if not changes:

                    activity = item.get(
                        "activity",
                        ""
                    )

                    if activity:

                        story.append(
                            f"{date} : {activity}"
                        )

                    continue

                for change in changes:

                    if change == "Initial State":

                        activity = item.get(
                            "activity",
                            ""
                        )

                        if activity:

                            story.append(
                                f"{date} : "
                                f"Initial business state established. "
                                f"Activity: {activity}"
                            )

                        else:

                            story.append(
                                f"{date} : "
                                f"Initial business state established."
                            )

                        continue

                    if change == "No Business Change":
                        continue

                    if change.startswith(
                        "Release Added"
                    ):

                        parts = change.split(
                            ":",
                            1
                        )

                        if len(parts) == 2:

                            release = parts[1].strip()

                            story.append(
                                f"{date} : "
                                f"Release {release} introduced."
                            )

                        continue

                    story.append(
                        f"{date} : {change}"
                    )

        return story

    # =========================================================
    # CURRENT STATE
    # =========================================================

    @classmethod
    def _build_current_state(cls, evolution):

        current_state = {}

        for item in reversed(
            evolution.get("evolution", [])
        ):

            if item.get("type") != "Business Change":
                continue

            state = item.get(
                "state",
                {}
            )

            if state:

                current_state = dict(state)

                break

        return cls._normalize_state(
            current_state
        )

    # =========================================================
    # BUSINESS MILESTONES
    # =========================================================

    @classmethod
    def _build_business_milestones(cls, evolution):

        milestones = []

        topic = evolution.get(
            "topic",
            "Application"
        )

        latest_state = cls._build_current_state(
            evolution
        )

        # -----------------------------------------------------
        # Topic initiation
        # -----------------------------------------------------

        milestones.append(
            f"{topic} initiated."
        )

        # -----------------------------------------------------
        # Releases
        # -----------------------------------------------------

        for release in latest_state.get(
            "releases",
            []
        ):

            milestones.append(
                f"{release} introduced."
            )

        # -----------------------------------------------------
        # APIs
        # -----------------------------------------------------

        for api in latest_state.get(
            "apis",
            []
        ):

            milestones.append(
                f"{api} API/integration active."
            )

        # -----------------------------------------------------
        # Business objects
        # -----------------------------------------------------

        status = latest_state.get(
            "status",
            "Unknown"
        )

        for obj in latest_state.get(
            "business_objects",
            []
        ):

            milestones.append(
                f"{obj} under "
                f"{str(status).lower()}."
            )

        # -----------------------------------------------------
        # Technologies
        # -----------------------------------------------------

        for tech in latest_state.get(
            "technologies",
            []
        ):

            milestones.append(
                f"{tech} technology in use."
            )

        # -----------------------------------------------------
        # Infrastructure
        # -----------------------------------------------------

        for infra in latest_state.get(
            "infrastructure",
            []
        ):

            milestones.append(
                f"{infra} infrastructure involved."
            )

        # -----------------------------------------------------
        # Integrations
        # -----------------------------------------------------

        for integration in latest_state.get(
            "integrations",
            []
        ):

            milestones.append(
                f"{integration} integration involved."
            )

        return cls._unique(
            milestones
        )

    # =========================================================
    # TIMELINE SUMMARY
    # =========================================================

    @classmethod
    def _build_timeline_summary(cls, evolution):

        changes = 0
        stable_periods = 0

        start_date = None
        end_date = None

        latest_state = {}

        for item in evolution.get(
            "evolution",
            []
        ):

            item_type = item.get(
                "type"
            )

            if item_type == "Business Change":

                changes += 1

                state = item.get(
                    "state",
                    {}
                )

                if state:
                    latest_state = state

                date = item.get(
                    "date"
                )

                if start_date is None:
                    start_date = date

                end_date = date

            elif item_type == "Stable":

                stable_periods += 1

                stable_start = item.get(
                    "start_date"
                )

                stable_end = item.get(
                    "end_date"
                )

                if start_date is None:
                    start_date = stable_start

                end_date = stable_end

        return {

            "start_date": start_date,

            "end_date": end_date,

            "business_changes": changes,

            "stable_periods": stable_periods,

            "current_status":
                latest_state.get(
                    "status"
                ),

            "environment":
                latest_state.get(
                    "environment"
                ),

            "activity_type":
                latest_state.get(
                    "activity_type"
                )

        }

    # =========================================================
    # ACTIVITY DETAILS
    # =========================================================

    @classmethod
    def _build_activity_details(cls, evolution):

        activities = []

        for item in evolution.get(
            "evolution",
            []
        ):

            if item.get(
                "type"
            ) != "Business Change":

                continue

            date = item.get(
                "date"
            )

            activity = item.get(
                "activity",
                ""
            )

            changes = item.get(
                "changes",
                []
            )

            state = item.get(
                "state",
                {}
            )

            activity_record = {

                "date": date,

                "activity": activity,

                "status":
                    state.get(
                        "status"
                    ),

                "environment":
                    state.get(
                        "environment"
                    ),

                "activity_type":
                    state.get(
                        "activity_type"
                    ),

                "changes":
                    list(changes)

            }

            activities.append(
                activity_record
            )

        return activities

    # =========================================================
    # STATUS PROGRESSION
    # =========================================================

    @classmethod
    def _build_status_progression(cls, evolution):

        progression = []

        previous = None

        for item in evolution.get(
            "evolution",
            []
        ):

            if item.get(
                "type"
            ) != "Business Change":

                continue

            state = item.get(
                "state",
                {}
            )

            status = state.get(
                "status"
            )

            if status is None:
                continue

            if status != previous:

                progression.append({

                    "date":
                        item.get(
                            "date"
                        ),

                    "status":
                        status

                })

                previous = status

        return progression

    # =========================================================
    # ENVIRONMENT PROGRESSION
    # =========================================================

    @classmethod
    def _build_environment_progression(
        cls,
        evolution
    ):

        progression = []

        previous = None

        for item in evolution.get(
            "evolution",
            []
        ):

            if item.get(
                "type"
            ) != "Business Change":

                continue

            state = item.get(
                "state",
                {}
            )

            environment = state.get(
                "environment"
            )

            if environment is None:
                continue

            if environment != previous:

                progression.append({

                    "date":
                        item.get(
                            "date"
                        ),

                    "environment":
                        environment

                })

                previous = environment

        return progression

    # =========================================================
    # ACTIVITY TYPE PROGRESSION
    # =========================================================

    @classmethod
    def _build_activity_type_progression(
        cls,
        evolution
    ):

        progression = []

        previous = None

        for item in evolution.get(
            "evolution",
            []
        ):

            if item.get(
                "type"
            ) != "Business Change":

                continue

            state = item.get(
                "state",
                {}
            )

            activity_type = state.get(
                "activity_type"
            )

            if activity_type is None:
                continue

            if activity_type != previous:

                progression.append({

                    "date":
                        item.get(
                            "date"
                        ),

                    "activity_type":
                        activity_type

                })

                previous = activity_type

        return progression

    # =========================================================
    # IMPORTANT CHANGES
    # =========================================================

    @classmethod
    def _build_important_changes(
        cls,
        evolution
    ):

        changes = []

        for item in evolution.get(
            "evolution",
            []
        ):

            if item.get(
                "type"
            ) != "Business Change":

                continue

            date = item.get(
                "date"
            )

            for change in item.get(
                "changes",
                []
            ):

                if change in (
                    "Initial State",
                    "No Business Change"
                ):
                    continue

                changes.append({

                    "date": date,

                    "change": change

                })

        return changes

    # =========================================================
    # GOVERNANCE EVIDENCE
    # =========================================================

    @classmethod
    def _build_governance_evidence(
        cls,
        evolution
    ):
        """
        Builds a richer evidence section.

        This is deliberately less compressed than
        business_story/current_state.

        The LLM can use this section to write a
        more complete application narrative.
        """

        evidence = []

        for item in evolution.get(
            "evolution",
            []
        ):

            if item.get(
                "type"
            ) != "Business Change":

                continue

            date = item.get(
                "date"
            )

            activity = item.get(
                "activity",
                ""
            )

            changes = item.get(
                "changes",
                []
            )

            state = item.get(
                "state",
                {}
            )

            evidence.append({

                "date": date,

                "activity": activity,

                "status":
                    state.get(
                        "status"
                    ),

                "environment":
                    state.get(
                        "environment"
                    ),

                "activity_type":
                    state.get(
                        "activity_type"
                    ),

                "changes":
                    list(changes),

                "releases":
                    cls._as_list(
                        state.get(
                            "releases"
                        )
                    ),

                "apis":
                    cls._as_list(
                        state.get(
                            "apis"
                        )
                    ),

                "business_objects":
                    cls._as_list(
                        state.get(
                            "business_objects"
                        )
                    ),

                "technologies":
                    cls._as_list(
                        state.get(
                            "technologies"
                        )
                    ),

                "infrastructure":
                    cls._as_list(
                        state.get(
                            "infrastructure"
                        )
                    ),

                "integrations":
                    cls._as_list(
                        state.get(
                            "integrations"
                        )
                    )

            })

        return evidence

    # =========================================================
    # APPLICATION SUMMARY
    # =========================================================

    @classmethod
    def _build_application_summary(
        cls,
        evolution
    ):
        """
        Creates structured application-level material
        for the final governance prompt.

        This intentionally contains more information than
        the short executive summary.
        """

        state = cls._build_current_state(
            evolution
        )

        topic = evolution.get(
            "topic"
        )

        summary = {

            "application": topic,

            "current_status":
                state.get(
                    "status"
                ),

            "environment":
                state.get(
                    "environment"
                ),

            "activity_type":
                state.get(
                    "activity_type"
                ),

            "releases":
                cls._as_list(
                    state.get(
                        "releases"
                    )
                ),

            "apis":
                cls._as_list(
                    state.get(
                        "apis"
                    )
                ),

            "business_objects":
                cls._as_list(
                    state.get(
                        "business_objects"
                    )
                ),

            "technologies":
                cls._as_list(
                    state.get(
                        "technologies"
                    )
                ),

            "infrastructure":
                cls._as_list(
                    state.get(
                        "infrastructure"
                    )
                ),

            "integrations":
                cls._as_list(
                    state.get(
                        "integrations"
                    )
                ),

            "status_progression":
                cls._build_status_progression(
                    evolution
                ),

            "environment_progression":
                cls._build_environment_progression(
                    evolution
                ),

            "activity_type_progression":
                cls._build_activity_type_progression(
                    evolution
                ),

            "important_changes":
                cls._build_important_changes(
                    evolution
                )

        }

        return summary

    # =========================================================
    # STATE NORMALIZATION
    # =========================================================

    @classmethod
    def _normalize_state(
        cls,
        state
    ):

        normalized = {}

        for key, value in state.items():

            normalized[key] = cls._normalize_value(
                value
            )

        return normalized

    # =========================================================
    # VALUE NORMALIZATION
    # =========================================================

    @classmethod
    def _normalize_value(
        cls,
        value
    ):

        if isinstance(
            value,
            set
        ):

            return sorted(
                list(value)
            )

        if isinstance(
            value,
            tuple
        ):

            return list(value)

        if isinstance(
            value,
            list
        ):

            return [
                cls._normalize_value(
                    item
                )
                for item in value
            ]

        if isinstance(
            value,
            dict
        ):

            return {
                key:
                    cls._normalize_value(
                        val
                    )

                for key, val
                in value.items()
            }

        return value

    # =========================================================
    # AS LIST
    # =========================================================

    @classmethod
    def _as_list(
        cls,
        value
    ):

        if value is None:
            return []

        if isinstance(
            value,
            set
        ):

            return sorted(
                list(value)
            )

        if isinstance(
            value,
            (list, tuple)
        ):

            return list(value)

        return [value]

    # =========================================================
    # UNIQUE
    # =========================================================

    @staticmethod
    def _unique(values):

        result = []

        seen = set()

        for value in values:

            if value in seen:
                continue

            seen.add(value)

            result.append(
                value
            )

        return result

    # =========================================================
    # DATE FORMATTER
    # =========================================================

    @staticmethod
    def _format_date(value):

        if not value:
            return value

        try:

            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).strftime(
                "%d-%b-%Y"
            )

        except (
            ValueError,
            TypeError
        ):

            return value
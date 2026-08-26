class DevelopmentEvolutionBuilder:
    """
    Converts business states into detailed business evolution.

    Design goals
    ------------

    1. Preserve actual business changes.
    2. Group consecutive no-change periods for timeline analysis.
    3. DO NOT lose the underlying RAG/activity information
       during stable periods.
    4. Preserve:
         - report_id
         - report_date
         - activity
         - status
         - environment
         - activity_type
         - state
         - changes
    5. Allow AIContextBuilder to use detailed RAG evidence.
    6. Avoid making any AI/LLM decisions.
    """

    # =========================================================
    # PUBLIC BUILDER
    # =========================================================

    @classmethod
    def build(cls, business_states):

        evolutions = []

        for topic in business_states:

            evolution = []

            current_stable_period = None

            states = topic.get(
                "states",
                []
            )

            for state in states:

                changes = state.get(
                    "changes",
                    []
                )

                # -------------------------------------------------
                # Determine whether this is a no-business-change
                # state.
                # -------------------------------------------------

                no_change = (
                    len(changes) == 1
                    and changes[0] == "No Business Change"
                )

                # =================================================
                # STABLE PERIOD
                # =================================================

                if no_change:

                    if current_stable_period is None:

                        current_stable_period = {

                            "type": "Stable",

                            "start_date":
                                state.get(
                                    "report_date"
                                ),

                            "end_date":
                                state.get(
                                    "report_date"
                                ),

                            "report_ids": [],

                            "activities": []

                        }

                    else:

                        current_stable_period[
                            "end_date"
                        ] = state.get(
                            "report_date"
                        )

                    # -------------------------------------------------
                    # IMPORTANT:
                    # Preserve the RAG evidence even though the
                    # business state itself is stable.
                    # -------------------------------------------------

                    report_id = state.get(
                        "report_id"
                    )

                    if report_id:

                        current_stable_period[
                            "report_ids"
                        ].append(
                            report_id
                        )

                    current_stable_period[
                        "activities"
                    ].append(
                        cls._build_activity_evidence(
                            state
                        )
                    )

                    continue

                # =================================================
                # BUSINESS CHANGE
                # =================================================

                # -------------------------------------------------
                # Flush previous stable period first.
                # -------------------------------------------------

                if current_stable_period:

                    evolution.append(
                        current_stable_period
                    )

                    current_stable_period = None

                # -------------------------------------------------
                # Preserve complete business-change information.
                # -------------------------------------------------

                evolution.append({

                    "type":
                        "Business Change",

                    "date":
                        state.get(
                            "report_date"
                        ),

                    "report_id":
                        state.get(
                            "report_id"
                        ),

                    "changes":
                        list(changes),

                    "activity":
                        state.get(
                            "activity",
                            ""
                        ),

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

                    "state":
                        cls._copy_state(
                            state.get(
                                "state",
                                {}
                            )
                        ),

                    "evidence":
                        cls._build_activity_evidence(
                            state
                        )

                })

            # =====================================================
            # FLUSH FINAL STABLE PERIOD
            # =====================================================

            if current_stable_period:

                evolution.append(
                    current_stable_period
                )

            # =====================================================
            # RESULT
            # =====================================================

            evolutions.append({

                "topic":
                    topic.get(
                        "topic"
                    ),

                "evolution":
                    evolution

            })

        return evolutions

    # =========================================================
    # BUILD ACTIVITY EVIDENCE
    # =========================================================

    @classmethod
    def _build_activity_evidence(
        cls,
        state
    ):
        """
        Preserve the original RAG-level information.

        This is especially important for stable periods.

        Example:

        07-Jul
        activity = "Mainframe-to-PTX..."
        status = "Planned"

        Even if there is no business-state change,
        the activity is still useful to the AI.
        """

        return {

            "report_id":
                state.get(
                    "report_id"
                ),

            "report_date":
                state.get(
                    "report_date"
                ),

            "activity":
                state.get(
                    "activity",
                    ""
                ),

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
                list(
                    state.get(
                        "changes",
                        []
                    )
                ),

            "state":
                cls._copy_state(
                    state.get(
                        "state",
                        {}
                    )
                )

        }

    # =========================================================
    # COPY STATE
    # =========================================================

    @classmethod
    def _copy_state(
        cls,
        state
    ):
        """
        Safely copy the business state.

        Converts sets to lists so that the resulting
        structure remains easy to serialize and consume.
        """

        if not isinstance(
            state,
            dict
        ):

            return {}

        result = {}

        for key, value in state.items():

            result[key] = cls._normalize_value(
                value
            )

        return result

    # =========================================================
    # NORMALIZE VALUE
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

            return [
                cls._normalize_value(
                    item
                )
                for item in value
            ]

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
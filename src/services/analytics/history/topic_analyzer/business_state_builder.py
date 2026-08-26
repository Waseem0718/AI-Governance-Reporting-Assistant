from copy import deepcopy
from typing import Any


class BusinessStateBuilder:
    """
    Converts chronological topic events into cumulative business states.

    RAG reports are treated as snapshots.

    Important state-handling rule:
        Unknown / None / empty values mean that the current RAG did not
        provide meaningful information for that field. They do NOT overwrite
        a previously known state.

    Example:

        02-Jul -> status = "Testing"
        08-Jul -> status = "Unknown"
        09-Jul -> status = "Deployed"

    Result:

        02-Jul -> Testing
        08-Jul -> Testing
        09-Jul -> Deployed

    This prevents false business-state changes such as:

        Testing -> Unknown
        PROD -> Unknown
    """

    # ---------------------------------------------------------
    # Fields whose values accumulate throughout the timeline
    # ---------------------------------------------------------

    COLLECTION_FIELDS = {
        "releases": "Release",
        "apis": "API",
        "business_objects": "Business Object",
        "technologies": "Technology",
        "infrastructure": "Infrastructure",
        "integrations": "Integration",
    }

    # ---------------------------------------------------------
    # Fields representing the latest meaningful business state
    # ---------------------------------------------------------

    SIMPLE_FIELDS = {
        "status": "Status",
        "environment": "Environment",
        "activity_type": "Activity Type",
    }

    # ---------------------------------------------------------
    # Values considered as "no information"
    # ---------------------------------------------------------

    UNKNOWN_VALUES = {
        "",
        "unknown",
        "none",
        "null",
        "n/a",
        "na",
        "-",
    }

    # ---------------------------------------------------------
    # Public builder
    # ---------------------------------------------------------

    @classmethod
    def build(
        cls,
        timelines: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:

        results = []

        for timeline in timelines:

            previous_state = None
            states = []

            # -------------------------------------------------
            # Always process events chronologically
            # -------------------------------------------------

            events = sorted(
                timeline.get("events", []),
                key=lambda event: event.get("report_date") or "",
            )

            for event in events:

                # ---------------------------------------------
                # Build cumulative current state
                # ---------------------------------------------

                current_state = cls._build_state(
                    previous_state=previous_state,
                    event=event,
                )

                # ---------------------------------------------
                # Compare against previous state
                # ---------------------------------------------

                changes = cls._compare_states(
                    previous_state=previous_state,
                    current_state=current_state,
                )

                # ---------------------------------------------
                # Store state snapshot
                # ---------------------------------------------

                states.append(
                    {
                        "report_date": event.get("report_date"),

                        "report_id": event.get("report_id"),

                        "activity": event.get(
                            "activity",
                            ""
                        ),

                        "state": deepcopy(current_state),

                        "changes": changes,
                    }
                )

                # ---------------------------------------------
                # Current state becomes previous state
                # ---------------------------------------------

                previous_state = deepcopy(current_state)

            # -------------------------------------------------
            # Store topic result
            # -------------------------------------------------

            results.append(
                {
                    "topic": timeline.get(
                        "topic_name",
                        "Unknown"
                    ),

                    "states": states,
                }
            )

        return results

    # =========================================================
    # Build cumulative state
    # =========================================================

    @classmethod
    def _build_state(
        cls,
        previous_state: dict[str, Any] | None,
        event: dict[str, Any],
    ) -> dict[str, Any]:

        # =====================================================
        # FIRST EVENT
        # =====================================================

        if previous_state is None:

            state = {
                "application": event.get(
                    "application"
                ),

                "status": cls._meaningful_value(
                    event.get("status")
                ),

                "environment": cls._meaningful_value(
                    event.get("environment")
                ),

                "activity_type": cls._meaningful_value(
                    event.get("activity_type")
                ),

                "releases": set(
                    event.get("releases", [])
                ),

                "apis": set(
                    event.get("apis", [])
                ),

                "business_objects": set(
                    event.get("business_objects", [])
                ),

                "technologies": set(
                    event.get("technologies", [])
                ),

                "infrastructure": set(
                    event.get("infrastructure", [])
                ),

                "integrations": set(
                    event.get("integrations", [])
                ),
            }

            return state

        # =====================================================
        # EXISTING STATE
        # =====================================================

        state = deepcopy(previous_state)

        # -----------------------------------------------------
        # Application
        #
        # Application is the governance identity.
        # Only replace it when a meaningful value is available.
        # -----------------------------------------------------

        application = cls._meaningful_value(
            event.get("application")
        )

        if application is not None:
            state["application"] = application

        # -----------------------------------------------------
        # Latest meaningful status
        #
        # IMPORTANT:
        #
        # Unknown does NOT overwrite the previous status.
        # -----------------------------------------------------

        status = cls._meaningful_value(
            event.get("status")
        )

        if status is not None:
            state["status"] = status

        # -----------------------------------------------------
        # Latest meaningful environment
        #
        # Unknown does NOT overwrite the previous environment.
        # -----------------------------------------------------

        environment = cls._meaningful_value(
            event.get("environment")
        )

        if environment is not None:
            state["environment"] = environment

        # -----------------------------------------------------
        # Latest meaningful activity type
        #
        # Unknown does NOT overwrite the previous activity type.
        # -----------------------------------------------------

        activity_type = cls._meaningful_value(
            event.get("activity_type")
        )

        if activity_type is not None:
            state["activity_type"] = activity_type

        # =====================================================
        # CUMULATIVE BUSINESS KNOWLEDGE
        # =====================================================

        for field in cls.COLLECTION_FIELDS:

            state.setdefault(
                field,
                set()
            )

            values = event.get(
                field,
                []
            )

            if values:

                state[field].update(
                    value
                    for value in values
                    if cls._meaningful_value(value) is not None
                )

        return state

    # =========================================================
    # Determine whether a value contains meaningful information
    # =========================================================

    @classmethod
    def _meaningful_value(
        cls,
        value: Any
    ) -> Any:

        if value is None:
            return None

        # -----------------------------------------------------
        # Strings
        # -----------------------------------------------------

        if isinstance(value, str):

            cleaned = value.strip()

            if not cleaned:
                return None

            if cleaned.lower() in cls.UNKNOWN_VALUES:
                return None

            return cleaned

        # -----------------------------------------------------
        # Lists / sets / tuples
        #
        # These are handled separately by collection logic.
        # -----------------------------------------------------

        if isinstance(value, (list, set, tuple)):

            meaningful = [
                item
                for item in value
                if cls._meaningful_value(item) is not None
            ]

            return meaningful if meaningful else None

        return value

    # =========================================================
    # Compare consecutive cumulative states
    # =========================================================

    @classmethod
    def _compare_states(
        cls,
        previous_state: dict[str, Any] | None,
        current_state: dict[str, Any],
    ) -> list[str]:

        # -----------------------------------------------------
        # First event
        # -----------------------------------------------------

        if previous_state is None:
            return ["Initial State"]

        changes = []

        # -----------------------------------------------------
        # Compare simple/latest-state fields
        # -----------------------------------------------------

        for field, display_name in cls.SIMPLE_FIELDS.items():

            cls._compare_simple_field(
                field=field,
                display_name=display_name,
                previous_state=previous_state,
                current_state=current_state,
                changes=changes,
            )

        # -----------------------------------------------------
        # Compare cumulative collections
        # -----------------------------------------------------

        for field, display_name in cls.COLLECTION_FIELDS.items():

            cls._compare_collection_field(
                field=field,
                display_name=display_name,
                previous_state=previous_state,
                current_state=current_state,
                changes=changes,
            )

        # -----------------------------------------------------
        # No meaningful change
        # -----------------------------------------------------

        if not changes:
            changes.append("No Business Change")

        return changes

    # =========================================================
    # Compare simple fields
    # =========================================================

    @classmethod
    def _compare_simple_field(
        cls,
        field: str,
        display_name: str,
        previous_state: dict[str, Any],
        current_state: dict[str, Any],
        changes: list[str],
    ) -> None:

        previous_value = previous_state.get(
            field
        )

        current_value = current_state.get(
            field
        )

        # -----------------------------------------------------
        # Nothing known yet
        # -----------------------------------------------------

        if current_value is None:
            return

        # -----------------------------------------------------
        # No previous meaningful value
        #
        # We don't report this as a "change" because the first
        # meaningful value is not necessarily a state transition.
        # -----------------------------------------------------

        if previous_value is None:
            return

        # -----------------------------------------------------
        # Actual state transition
        # -----------------------------------------------------

        if previous_value != current_value:

            changes.append(
                f"{display_name} changed: "
                f"{previous_value} → {current_value}"
            )

    # =========================================================
    # Compare cumulative collection fields
    # =========================================================

    @staticmethod
    def _compare_collection_field(
        field: str,
        display_name: str,
        previous_state: dict[str, Any],
        current_state: dict[str, Any],
        changes: list[str],
    ) -> None:

        previous_values = set(
            previous_state.get(
                field,
                set()
            )
        )

        current_values = set(
            current_state.get(
                field,
                set()
            )
        )

        # -----------------------------------------------------
        # Newly discovered values
        # -----------------------------------------------------

        added_values = (
            current_values - previous_values
        )

        for value in sorted(
            added_values,
            key=str
        ):

            changes.append(
                f"{display_name} Added : {value}"
            )

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # Removals are intentionally ignored.
        #
        # A daily RAG report is a snapshot and may simply omit
        # something mentioned previously. Absence does not mean
        # that the item was removed.
        # -----------------------------------------------------

    # =========================================================
    # Utility: Convert state sets to JSON-friendly lists
    # =========================================================

    @classmethod
    def normalize_state_for_output(
        cls,
        state: dict[str, Any]
    ) -> dict[str, Any]:

        normalized = {}

        for key, value in state.items():

            if isinstance(value, set):

                normalized[key] = sorted(
                    value,
                    key=str
                )

            else:

                normalized[key] = value

        return normalized
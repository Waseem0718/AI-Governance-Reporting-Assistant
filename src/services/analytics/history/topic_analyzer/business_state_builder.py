from copy import deepcopy
from typing import Any


class BusinessStateBuilder:
    """
    Converts chronological topic events into cumulative business states.

    RAG reports are treated as snapshots. If an entity is absent from a later
    report, it is not considered removed unless explicit removal logic is
    introduced in the future.
    """

    COLLECTION_FIELDS = {
        "releases": "Release",
        "apis": "API",
        "business_objects": "Business Object",
        "technologies": "Technology",
        "infrastructure": "Infrastructure",
        "integrations": "Integration",
    }

    SIMPLE_FIELDS = {
        "status": "Status",
        "environment": "Environment",
        "activity_type": "Activity Type",
    }

    # ---------------------------------------------------------
    # Public builder
    # ---------------------------------------------------------

    @classmethod
    def build(cls, timelines: list[dict[str, Any]]) -> list[dict[str, Any]]:
        results = []

        for timeline in timelines:
            previous_state = None
            states = []

            events = sorted(
                timeline.get("events", []),
                key=lambda event: event.get("report_date") or "",
            )

            for event in events:
                current_state = cls._build_state(
                    previous_state=previous_state,
                    event=event,
                )

                changes = cls._compare_states(
                    previous_state=previous_state,
                    current_state=current_state,
                )

                states.append(
                    {
                        "report_date": event.get("report_date"),
                        "report_id": event.get("report_id"),
                        "activity": event.get("activity", ""),
                        "state": deepcopy(current_state),
                        "changes": changes,
                    }
                )

                previous_state = deepcopy(current_state)

            results.append(
                {
                    "topic": timeline.get("topic_name", "Unknown"),
                    "states": states,
                }
            )

        return results

    # ---------------------------------------------------------
    # Build cumulative state
    # ---------------------------------------------------------

    @classmethod
    def _build_state(
        cls,
        previous_state: dict[str, Any] | None,
        event: dict[str, Any],
    ) -> dict[str, Any]:

        if previous_state is None:
            return {
                "application": event.get("application"),
                "status": event.get("status"),
                "environment": event.get("environment"),
                "activity_type": event.get("activity_type"),
                "releases": set(event.get("releases", [])),
                "apis": set(event.get("apis", [])),
                "business_objects": set(
                    event.get("business_objects", [])
                ),
                "technologies": set(event.get("technologies", [])),
                "infrastructure": set(
                    event.get("infrastructure", [])
                ),
                "integrations": set(event.get("integrations", [])),
            }

        state = deepcopy(previous_state)

        # Latest report controls the current scalar state.
        state["application"] = event.get(
            "application",
            state.get("application"),
        )

        state["status"] = event.get(
            "status",
            state.get("status"),
        )

        state["environment"] = event.get(
            "environment",
            state.get("environment"),
        )

        state["activity_type"] = event.get(
            "activity_type",
            state.get("activity_type"),
        )

        # Business knowledge is cumulative.
        for field in cls.COLLECTION_FIELDS:
            state.setdefault(field, set())
            state[field].update(event.get(field, []))

        return state

    # ---------------------------------------------------------
    # Compare consecutive cumulative states
    # ---------------------------------------------------------

    @classmethod
    def _compare_states(
        cls,
        previous_state: dict[str, Any] | None,
        current_state: dict[str, Any],
    ) -> list[str]:

        if previous_state is None:
            return ["Initial State"]

        changes = []

        for field, display_name in cls.SIMPLE_FIELDS.items():
            cls._compare_simple_field(
                field=field,
                display_name=display_name,
                previous_state=previous_state,
                current_state=current_state,
                changes=changes,
            )

        for field, display_name in cls.COLLECTION_FIELDS.items():
            cls._compare_collection_field(
                field=field,
                display_name=display_name,
                previous_state=previous_state,
                current_state=current_state,
                changes=changes,
            )

        if not changes:
            changes.append("No Business Change")

        return changes

    # ---------------------------------------------------------
    # Compare scalar values
    # ---------------------------------------------------------

    @staticmethod
    def _compare_simple_field(
        field: str,
        display_name: str,
        previous_state: dict[str, Any],
        current_state: dict[str, Any],
        changes: list[str],
    ) -> None:

        previous_value = previous_state.get(field)
        current_value = current_state.get(field)

        if previous_value != current_value:
            changes.append(
                f"{display_name} changed: "
                f"{previous_value} → {current_value}"
            )

    # ---------------------------------------------------------
    # Compare cumulative collections
    # ---------------------------------------------------------

    @staticmethod
    def _compare_collection_field(
        field: str,
        display_name: str,
        previous_state: dict[str, Any],
        current_state: dict[str, Any],
        changes: list[str],
    ) -> None:

        previous_values = set(previous_state.get(field, set()))
        current_values = set(current_state.get(field, set()))

        added_values = current_values - previous_values

        for value in sorted(added_values):
            changes.append(f"{display_name} Added : {value}")

        # Removals are intentionally ignored because daily RAG reports may
        # omit previously mentioned items without meaning they were removed.
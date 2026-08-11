class DevelopmentEvolutionBuilder:
    """
    Converts business states into business evolution.

    Version 1

    - Groups consecutive 'No Business Change' states
    - Preserves actual business changes
    """

    @classmethod
    def build(cls, business_states):

        evolutions = []

        for topic in business_states:

            evolution = []

            current_period = None

            for state in topic["states"]:

                changes = state["changes"]

                no_change = (
                    len(changes) == 1
                    and changes[0] == "No Business Change"
                )

                # ----------------------------------
                # Stable Period
                # ----------------------------------

                if no_change:

                    if current_period is None:

                        current_period = {

                            "type": "Stable",

                            "start_date": state["report_date"],

                            "end_date": state["report_date"],

                            "report_ids": [state["report_id"]]

                        }

                    else:

                        current_period["end_date"] = state["report_date"]

                        current_period["report_ids"].append(
                            state["report_id"]
                        )

                    continue

                # ----------------------------------
                # Flush previous stable period
                # ----------------------------------

                if current_period:

                    evolution.append(current_period)

                    current_period = None

                # ----------------------------------
                # Business Change
                # ----------------------------------

                evolution.append({

                    "type": "Business Change",

                    "date": state["report_date"],

                    "report_id": state["report_id"],

                    "changes": changes,

                    "activity": state["activity"],

                    "state": state["state"]

                })

            # ----------------------------------
            # Flush final stable period
            # ----------------------------------

            if current_period:

                evolution.append(current_period)

            evolutions.append({

                "topic": topic["topic"],

                "evolution": evolution

            })

        return evolutions
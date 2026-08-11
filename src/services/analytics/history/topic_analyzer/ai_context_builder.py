from datetime import datetime


class AIContextBuilder:
    """
    Converts Development Evolution into an AI-ready context.

    This class is completely LLM independent.
    """

    @classmethod
    def build(cls, evolutions):

        contexts = []

        for evolution in evolutions:

            contexts.append({

                "topic": evolution["topic"],

                "timeline_summary": cls._build_timeline_summary(evolution),

                "business_story": cls._build_business_story(evolution),

                "current_state": cls._build_current_state(evolution),

                "business_milestones": cls._build_business_milestones(evolution)

            })

        return contexts

    # --------------------------------------------------------
    # Business Story
    # --------------------------------------------------------

    @classmethod
    def _build_business_story(cls, evolution):

        story = []

        for item in evolution["evolution"]:

            if item["type"] == "Stable":

                start = datetime.strptime(
                    item["start_date"],
                    "%Y-%m-%d"
                ).strftime("%d-%b-%Y")

                end = datetime.strptime(
                    item["end_date"],
                    "%Y-%m-%d"
                ).strftime("%d-%b-%Y")

                story.append(
                    f"{start} to {end} : Business remained stable."
                )

            else:

                date = datetime.strptime(
                    item["date"],
                    "%Y-%m-%d"
                ).strftime("%d-%b-%Y")

                if item["changes"] == ["Initial State"]:

                    story.append(
                        f"{date} : Initial business state established."
                    )

                else:

                    for change in item["changes"]:

                        if change.startswith("Release Added"):

                            release = change.split(":")[1].strip()

                            story.append(
                                f"{date} : Release {release} introduced."
                            )

                        else:

                            story.append(
                                f"{date} : {change}"
                            )

        return story

    # --------------------------------------------------------
    # Current State
    # --------------------------------------------------------

    @classmethod
    def _build_current_state(cls, evolution):

        current_state = {}

        for item in reversed(evolution["evolution"]):

            if item["type"] == "Business Change":

                current_state = dict(item["state"])

                break

        for key, value in current_state.items():

            if isinstance(value, set):

                current_state[key] = sorted(list(value))

        return current_state

    # --------------------------------------------------------
    # Business Milestones
    # --------------------------------------------------------

    @classmethod
    def _build_business_milestones(cls, evolution):

        milestones = []

        latest_state = cls._build_current_state(evolution)

        milestones.append(
            f"{evolution['topic']} initiated."
        )

        for release in latest_state.get("releases", []):

            milestones.append(
                f"{release} introduced."
            )

        for api in latest_state.get("apis", []):

            milestones.append(
                f"{api} integration active."
            )

        for obj in latest_state.get("business_objects", []):

            milestones.append(
                f"{obj} under {latest_state.get('status','Unknown').lower()}."
            )

        for tech in latest_state.get("technologies", []):

            milestones.append(
                f"{tech} technology in use."
            )

        for infra in latest_state.get("infrastructure", []):

            milestones.append(
                f"{infra} infrastructure involved."
            )

        return milestones
    
    # --------------------------------------------------------
    # Timeline Summary
    # --------------------------------------------------------

    @classmethod
    def _build_timeline_summary(cls, evolution):

        changes = 0
        stable = 0

        start_date = None
        end_date = None

        latest_state = {}

        for item in evolution["evolution"]:

            if item["type"] == "Business Change":

                changes += 1

                latest_state = item["state"]

                if start_date is None:

                    start_date = item["date"]

                end_date = item["date"]

            else:

                stable += 1

                if start_date is None:

                    start_date = item["start_date"]

                end_date = item["end_date"]

        return {

            "start_date": start_date,

            "end_date": end_date,

            "business_changes": changes,

            "stable_periods": stable,

            "current_status": latest_state.get("status"),

            "environment": latest_state.get("environment")

        }
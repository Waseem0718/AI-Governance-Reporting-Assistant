from collections import defaultdict


class TimelineBuilder:
    """
    Builds chronological timelines from actual development history.
    """

    def __init__(self, repository):

        self.repository = repository

    # -------------------------------------------------------
    # Build Timeline
    # -------------------------------------------------------

    @classmethod
    def build(cls, topics):

        timelines = []

        for topic in topics:

            activities = sorted(

                topic["activities"],

                key=lambda x: x["report_date"]

            )

            events = []

            for activity in activities:

                events.append(

                    cls._create_event(activity)

                )

            timelines.append({

                "topic_name": topic["topic_name"],

                "events": events

            })

        return timelines
    
    @staticmethod
    @staticmethod
    def _create_event(activity):

        return {

            "report_date": activity["report_date"],

            "report_id": activity["report_id"],

            "application": activity["application"],

            "activity": activity["activity"],

            "activity_type": activity["activity_type"],

            "status": activity["status"],

            "environment": activity["environment"],

            "normalized_text": activity.get("normalized_text", ""),

            "keywords": activity.get("keywords", []),

            "applications": activity.get("applications", []),

            "activities": activity.get("activities", []),

            "releases": activity.get("releases", []),

            "apis": activity.get("apis", []),

            "business_objects": activity.get("business_objects", []),

            "technologies": activity.get("technologies", []),

            "infrastructure": activity.get("infrastructure", []),

            "integrations": activity.get("integrations", [])

        }
from collections import defaultdict
from services.analytics.history.topic_analyzer.topic_priority import TopicPriority

from .similarity_engine import SimilarityEngine


class TopicMerger:

    SIMILARITY_THRESHOLD = 0.70

    @classmethod
    def merge(cls, extracted_activities):

        topics = {}

        for activity in extracted_activities:

            topic_key = TopicPriority.choose(activity)

            if topic_key in topics:

                topics[topic_key]["activities"].append(activity)

                continue

            merged = False

            for existing_key, topic in topics.items():

                similarity = SimilarityEngine.compare(

                    topic["representative"],
                    activity

                )

                if similarity["overall_score"] >= cls.SIMILARITY_THRESHOLD:

                    topic["activities"].append(activity)

                    merged = True

                    break

            if merged:

                continue

            topics[topic_key] = {

                "topic_name": topic_key,

                "representative": activity,

                "activities": [activity]

            }

        return list(topics.values())
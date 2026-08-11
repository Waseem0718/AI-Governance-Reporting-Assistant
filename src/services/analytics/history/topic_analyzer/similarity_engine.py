from difflib import SequenceMatcher


class SimilarityEngine:
    """
    Enterprise Similarity Engine

    Compares two extracted development activities.

    Returns:
        0.0 - 1.0 similarity score
    """

    # -------------------------------
    # Text Similarity
    # -------------------------------

    @staticmethod
    def _text_similarity(text1, text2):

        return SequenceMatcher(

            None,
            text1.lower(),
            text2.lower()

        ).ratio()

    # -------------------------------
    # Keyword Similarity
    # -------------------------------

    @staticmethod
    def _keyword_similarity(k1, k2):

        if not k1 or not k2:

            return 0

        s1 = set(k1)
        s2 = set(k2)

        intersection = len(s1 & s2)
        union = len(s1 | s2)

        return intersection / union

    # -------------------------------
    # Entity Similarity
    # -------------------------------

    @staticmethod
    def _entity_similarity(e1, e2):

        if not e1 or not e2:

            return 0

        s1 = {

            (

                entity.entity_type,

                entity.value

            )

            for entity in e1

        }

        s2 = {

            (

                entity.entity_type,

                entity.value

            )

            for entity in e2

        }

        intersection = len(s1 & s2)
        union = len(s1 | s2)

        return intersection / union

    # -------------------------------
    # Overall Similarity
    # -------------------------------

    @classmethod
    def compare(cls, activity1, activity2):

        text_score = cls._text_similarity(

            activity1["normalized_text"],
            activity2["normalized_text"]

        )

        keyword_score = cls._keyword_similarity(

            activity1["keywords"],
            activity2["keywords"]

        )

        entity_score = cls._entity_similarity(

            activity1["entities"],
            activity2["entities"]

        )

        overall = (

            text_score * 0.30 +

            keyword_score * 0.30 +

            entity_score * 0.40

        )

        return {

            "overall_score": round(overall, 3),

            "text_score": round(text_score, 3),

            "keyword_score": round(keyword_score, 3),

            "entity_score": round(entity_score, 3),

            "is_same_topic": overall >= 0.70

        }

    # -------------------------------
    # Compare one against many
    # -------------------------------

    @classmethod
    def compare_with_all(cls, source, others):

        results = []

        for activity in others:

            score = cls.compare(

                source,
                activity

            )

            results.append({

                "activity": activity,

                "similarity": score

            })

        results.sort(

            key=lambda x: x["similarity"]["overall_score"],

            reverse=True

        )

        return results
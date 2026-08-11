class TopicPriority:

    """
    Chooses the business topic from extracted entities.
    """

    PRIORITY = {

        "Release":100,

        "API":90,

        "Migration":80,

        "BusinessObject":70,

        "Infrastructure":60,

        "Application":55,

        "Integration":50,

        "Technology":40,

        "Activity":20,

        "Keyword":10

    }

    @classmethod
    def choose(cls, extracted):

        entities = extracted["entities"]

        if not entities:

            return extracted["normalized_text"]

        best = None
        score = -1

        for entity in entities:

            priority = cls.PRIORITY.get(

                entity.entity_type,

                0

            )

            if priority > score:

                score = priority
                best = entity

        return cls._friendly_name(best)

    @staticmethod
    def _friendly_name(entity):

        if entity is None:

            return "Unknown"

        if entity.entity_type == "Release":

            return entity.value.split("_Release")[0] + " Release"

        return entity.value
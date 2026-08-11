from .entity import Entity
from . import entity_rules


class EntityExtractor:

    @staticmethod
    def _extract(dictionary, entity_type, text):

        entities = []

        lower = text.lower()

        for canonical, aliases in dictionary.items():

            for alias in aliases:

                if alias.lower() in lower:

                    entities.append(

                        Entity(

                            entity_type=entity_type,

                            value=canonical,

                            source=alias,

                            confidence=1.0

                        )

                    )

                    break

        return entities

    @classmethod
    def extract(cls, normalized):

        text = normalized["normalized"]

        result = {

            "normalized_text": text,

            "applications": [],

            "activities": [],

            "technologies": [],

            "environments": normalized["environments"],

            "infrastructure": [],

            "apis": [],

            "business_objects": [],

            "integrations": [],

            "releases": normalized["release_ids"],

            "keywords": [],

            "entities": [],

            "confidence": 1.0

        }

        # -----------------------------
        # Applications
        # -----------------------------

        apps = cls._extract(

            entity_rules.APPLICATIONS,

            "Application",

            text

        )

        result["entities"].extend(apps)

        result["applications"] = [

            entity.value

            for entity in apps

        ]

        # -----------------------------
        # Activities
        # -----------------------------

        activities = cls._extract(

            entity_rules.ACTIVITIES,

            "Activity",

            text

        )

        result["entities"].extend(activities)

        result["activities"] = [

            entity.value

            for entity in activities

        ]

        # -----------------------------
        # Technologies
        # -----------------------------

        techs = cls._extract(

            entity_rules.TECHNOLOGIES,

            "Technology",

            text

        )

        result["entities"].extend(techs)

        result["technologies"] = [

            entity.value

            for entity in techs

        ]

        # -----------------------------
        # Infrastructure
        # -----------------------------

        infra = cls._extract(

            entity_rules.INFRASTRUCTURE,

            "Infrastructure",

            text

        )

        result["entities"].extend(infra)

        result["infrastructure"] = [

            entity.value

            for entity in infra

        ]

        # -----------------------------
        # APIs
        # -----------------------------

        apis = cls._extract(

            entity_rules.APIS,

            "API",

            text

        )

        result["entities"].extend(apis)

        result["apis"] = [

            entity.value

            for entity in apis

        ]

        # -----------------------------
        # Integrations
        # -----------------------------

        integrations = cls._extract(

            entity_rules.INTEGRATIONS,

            "Integration",

            text

        )

        result["entities"].extend(integrations)

        result["integrations"] = [

            entity.value

            for entity in integrations

        ]

        # -----------------------------
        # Business Objects
        # -----------------------------

        business = cls._extract(

            entity_rules.BUSINESS_OBJECTS,

            "BusinessObject",

            text

        )

        result["entities"].extend(business)

        result["business_objects"] = [

            entity.value

            for entity in business

        ]

        # -----------------------------
        # Releases
        # -----------------------------

        for release in normalized["release_ids"]:

            result["entities"].append(

                Entity(

                    entity_type="Release",

                    value=release,

                    source=release

                )

            )

        # -----------------------------
        # Environments
        # -----------------------------

        for environment in normalized["environments"]:

            result["entities"].append(

                Entity(

                    entity_type="Environment",

                    value=environment,

                    source=environment

                )

            )

        # -----------------------------
        # Keywords
        # -----------------------------

        keywords = set()

        keywords.update(result["applications"])

        keywords.update(result["activities"])

        keywords.update(result["technologies"])

        keywords.update(result["infrastructure"])

        keywords.update(result["apis"])

        keywords.update(result["business_objects"])

        keywords.update(result["integrations"])

        keywords.update(result["releases"])

        keywords.update(result["environments"])

        keywords.update(normalized["actions"])

        keywords.update(normalized["status_words"])

        result["keywords"] = sorted(keywords)

        return result
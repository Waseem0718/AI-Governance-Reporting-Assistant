import re
import string


class TextNormalizer:
    """
    AGRA Universal Text Normalizer (V2)

    Produces structured metadata that can be used by
    EntityExtractor, TopicAnalyzer and AI Context Builder.
    """

    # ---------------------------------------------------------
    # Stop Words
    # ---------------------------------------------------------

    STOP_WORDS = {

        "the", "a", "an",
        "is", "are", "was", "were",
        "be", "been", "being",

        "of", "to", "for", "from",
        "with", "this", "that",
        "these", "those",

        "it", "its", "and",

        "in", "on", "at",
        "into", "onto",
        "during", "via",
        "through", "by"

    }

    # ---------------------------------------------------------
    # Environments
    # ---------------------------------------------------------

    ENVIRONMENTS = {

        "ppe",
        "prod",
        "production",
        "dev",
        "development",
        "uat",
        "sit",
        "dr"

    }

    # ---------------------------------------------------------
    # Technologies
    # ---------------------------------------------------------

    TECHNOLOGIES = {

        "openshift",
        "kubernetes",
        "k8s",
        "docker",
        "aks",
        "vm",

        "windows",
        "linux",

        "oracle",
        "sql",
        "mssql",
        "postgres",
        "redis",

        "kafka",
        "splunk",
        "newrelic",

        "terraform",
        "ansible",

        "nginx",
        "apache",
        "tomcat"

    }

    # ---------------------------------------------------------
    # Action Normalization
    # ---------------------------------------------------------

    ACTIONS = {

        "deployed": "deploy",
        "deployment": "deploy",
        "deploying": "deploy",

        "migrated": "migration",
        "migrate": "migration",
        "migrating": "migration",

        "upgraded": "upgrade",
        "upgrading": "upgrade",

        "configured": "configure",
        "configuring": "configure",

        "implemented": "implement",
        "implementing": "implement",

        "testing": "test",
        "tested": "test",

        "rollback": "restore",
        "restored": "restore",
        "restoring": "restore",

        "monitoring": "monitor",
        "monitored": "monitor"

    }

    # ---------------------------------------------------------
    # Status Mapping
    # ---------------------------------------------------------

    STATUS_WORDS = {

        "completed": "Completed",
        "complete": "Completed",

        "testing": "Testing",
        "test": "Testing",

        "progress": "In Progress",
        "ongoing": "In Progress",
        "started": "In Progress",

        "monitor": "Monitoring",
        "monitoring": "Monitoring",

        "deploy": "Deployment",
        "deployed": "Deployment",

        "rollback": "Rollback",
        "restore": "Rollback",
        "restored": "Rollback",

        "failed": "Failed",
        "failure": "Failed",

        "pending": "Pending",

        "implemented": "Implemented",

        "success": "Completed",
        "successful": "Completed"

    }

    # ---------------------------------------------------------
    # Main Normalizer
    # ---------------------------------------------------------

    @classmethod
    def normalize(cls, text):

        if not text:

            return {

                "original": "",
                "normalized": "",

                "release_ids": [],
                "versions": [],
                "years": [],

                "environments": [],
                "technologies": [],

                "actions": [],
                "status_words": []

            }

        original = text

        release_ids = cls._extract_release_ids(text)
        versions = cls._extract_versions(text)
        years = cls._extract_years(text)

        environments = cls._extract_environments(text)
        technologies = cls._extract_technologies(text)

        text = text.lower()

        text = cls._replace_special_characters(text)

        text = cls._remove_dates(text)

        text = cls._remove_release_numbers(text)

        text = cls._normalize_versions(text)

        text = cls._normalize_actions(text)

        text = cls._remove_punctuation(text)

        text = cls._remove_extra_spaces(text)

        text = cls._remove_stop_words(text)

        actions = cls._extract_actions(text)

        status = cls._extract_status(text)

        return {

            "original": original,

            "normalized": text,

            "release_ids": release_ids,

            "versions": versions,

            "years": years,

            "environments": environments,

            "technologies": technologies,

            "actions": actions,

            "status_words": status

        }

    # ---------------------------------------------------------
    # Text Cleanup
    # ---------------------------------------------------------

    @staticmethod
    def _replace_special_characters(text):

        return (

            text

            .replace("_", " ")

            .replace("-", " ")

            .replace("/", " ")

            .replace("\\", " ")

            .replace("&", " and ")

        )

    @staticmethod
    def _remove_dates(text):

        patterns = [

            r"\b20\d{6}\b",
            r"\b20\d{2}-\d{2}-\d{2}\b",
            r"\b\d{2}/\d{2}/20\d{2}\b",
            r"\b\d{1,2}[/-]\d{1,2}[/-]20\d{2}\b"

        ]

        for pattern in patterns:

            text = re.sub(pattern, " ", text)

        return text

    @staticmethod
    def _remove_release_numbers(text):

        return re.sub(

            r"release\s*\d+",

            "release",

            text,

            flags=re.IGNORECASE

        )

    @staticmethod
    def _normalize_versions(text):

        replacements = {

            r"windows\s+2012": "windows server",
            r"windows\s+2016": "windows server",
            r"windows\s+2019": "windows server",
            r"windows\s+2022": "windows server",

            r"sql\s*server\s*2012": "sql server",
            r"sql\s*server\s*2016": "sql server",
            r"sql\s*server\s*2019": "sql server",
            r"sql\s*server\s*2022": "sql server"

        }

        for pattern, replacement in replacements.items():

            text = re.sub(

                pattern,

                replacement,

                text,

                flags=re.IGNORECASE

            )

        return text

    @classmethod
    def _normalize_actions(cls, text):

        words = []

        for word in text.split():

            words.append(

                cls.ACTIONS.get(word, word)

            )

        return " ".join(words)

    @staticmethod
    def _remove_punctuation(text):

        return text.translate(

            str.maketrans("", "", string.punctuation)

        )

    @staticmethod
    def _remove_extra_spaces(text):

        return " ".join(text.split())

    @classmethod
    def _remove_stop_words(cls, text):

        return " ".join(

            [

                word

                for word in text.split()

                if word not in cls.STOP_WORDS

            ]

        )

    # ---------------------------------------------------------
    # Metadata Extraction
    # ---------------------------------------------------------

    @staticmethod
    def _extract_release_ids(text):

        return re.findall(

            r"[A-Za-z0-9]+_Release_\d{8}",

            text,

            flags=re.IGNORECASE

        )

    @staticmethod
    def _extract_versions(text):

        return re.findall(

            r"\bv\d+(\.\d+)?\b",

            text,

            flags=re.IGNORECASE

        )

    @staticmethod
    def _extract_years(text):

        return re.findall(

            r"\b20\d{2}\b",

            text

        )

    @classmethod
    def _extract_environments(cls, text):

        found = []

        lower = text.lower()

        for env in cls.ENVIRONMENTS:

            pattern = rf"\b{re.escape(env)}\b"

            if re.search(pattern, lower):

                found.append(env.upper())

        return sorted(set(found))

    @classmethod
    def _extract_technologies(cls, text):

        found = []

        lower = text.lower()

        for tech in cls.TECHNOLOGIES:

            pattern = rf"\b{re.escape(tech)}\b"

            if re.search(pattern, lower):

                found.append(tech)

        return sorted(set(found))

    @classmethod
    def _extract_actions(cls, text):

        found = set()

        words = text.lower().split()

        for word in words:

            if word in cls.ACTIONS.values():

                found.add(word)

        return sorted(found)

    @classmethod
    def _extract_status(cls, text):

        found = set()

        words = text.lower().split()

        for word in words:

            if word in cls.STATUS_WORDS:

                found.add(

                    cls.STATUS_WORDS[word]

                )

        return sorted(found)
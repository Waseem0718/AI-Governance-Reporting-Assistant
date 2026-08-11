import re


class ActivityTypeExtractor:

    PATTERNS = {

        "Release": [
            r"\brelease\b",
            r"\bdeployed\b"
        ],

        "Migration": [
            r"\bmigration\b",
            r"\bmigrating\b"
        ],

        "API Onboarding": [
            r"\bapi\b",
            r"\bonboarding\b"
        ],

        "DR Exercise": [
            r"\bdr\b",
            r"\bdisaster recovery\b",
            r"\bexercise\b"
        ],

        "Provisioning": [
            r"\bprovision\b"
        ],

        "Access Review": [
            r"user access review"
        ],

        "Investigation": [
            r"\binvestigat",
            r"\bidentified"
        ],

        "Platform Migration": [
            r"openshift",
            r"tpc v3",
            r"cdud"
        ],

        "Patching": [
            r"\bpatch\b"
        ],

        "Testing": [
            r"testing"
        ],

        "Upgrade": [
            r"upgrade"
        ],

        "Decommission": [
            r"decommission"
        ]

    }

    @classmethod
    def extract(cls, text):

        text = (text or "").lower()

        for activity_type, patterns in cls.PATTERNS.items():

            for pattern in patterns:

                if re.search(pattern, text):

                    return activity_type

        return "Other"
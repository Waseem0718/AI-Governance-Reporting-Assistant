import re


class ActivityTypeExtractor:

    PATTERNS = {

        # -----------------------------------------------------
        # Release / Deployment
        # -----------------------------------------------------

        "Release": [

            r"\blicensing_release_\d{8}\b",

            r"\brelease_\d{8}\b",

            r"\brelease\b",

            r"\bdeployed\b",

            r"\bdeployment\b",

            r"\bdeploy\b"
            
            r"\bdeployed\b"

        ],

        # -----------------------------------------------------
        # Migration
        # -----------------------------------------------------

        "Migration": [

            r"\bmigration\b",

            r"\bmigrating\b",

            r"\bmigrated\b",

            r"\bmigrate\b"

        ],

        # -----------------------------------------------------
        # Rollback
        # -----------------------------------------------------

        "Rollback": [

            r"\brollback\b",

            r"\brolled back\b",

            r"\brestore\b",

            r"\brestored\b"

        ],

        # -----------------------------------------------------
        # Decommission
        # -----------------------------------------------------

        "Decommission": [

            r"\bdecommission\b",

            r"\bdecommissioned\b",

            r"\bdecommissioning\b"

        ],

        # -----------------------------------------------------
        # API
        # -----------------------------------------------------

        "API Onboarding": [

            r"\bapi\b",

            r"\bonboarding\b"

        ],

        # -----------------------------------------------------
        # DR
        # -----------------------------------------------------

        "DR Exercise": [

            r"\bdr\b",

            r"\bdisaster recovery\b",

            r"\bexercise\b"

        ],

        # -----------------------------------------------------
        # Provisioning
        # -----------------------------------------------------

        "Provisioning": [

            r"\bprovision\b",

            r"\bprovisioned\b",

            r"\bprovisioning\b"

        ],

        # -----------------------------------------------------
        # Access Review
        # -----------------------------------------------------

        "Access Review": [

            r"user access review"

        ],

        # -----------------------------------------------------
        # Backlog
        # -----------------------------------------------------

        "Backlog": [

            r"\bbacklog\b",

            r"\bbacklog item\b"

        ],

        # -----------------------------------------------------
        # Investigation
        # -----------------------------------------------------

        "Investigation": [

            r"\binvestigat",

            r"\bidentified\b"

        ],

        # -----------------------------------------------------
        # Platform Migration
        # -----------------------------------------------------

        "Platform Migration": [

            r"openshift",

            r"tpc v3",

            r"cdud"

        ],

        # -----------------------------------------------------
        # Patching
        # -----------------------------------------------------

        "Patching": [

            r"\bpatch\b",

            r"\bpatching\b",

            r"\bpatched\b"
            
            r"\bpatches\b"

        ],

        # -----------------------------------------------------
        # Testing
        # -----------------------------------------------------

        "Testing": [

            r"\btesting\b",

            r"\btest\b",

            r"\btested\b"

        ],

        # -----------------------------------------------------
        # Upgrade
        # -----------------------------------------------------

        "Upgrade": [

            r"\bupgrade\b",

            r"\bupgraded\b",

            r"\bupgrading\b"

        ],

        # -----------------------------------------------------
        # Implementation
        # -----------------------------------------------------

        "Implementation": [

            r"\bimplement\b",

            r"\bimplemented\b",

            r"\bimplementation\b",

            r"\bimplementing\b"

        ],

        # -----------------------------------------------------
        # Development
        # -----------------------------------------------------

        "Development": [

            r"\bdevelopment\b",

            r"\bdeveloped\b",

            r"\bdeveloping\b"

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
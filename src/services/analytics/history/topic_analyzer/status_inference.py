import re


class StatusInference:
    """
    Determines a governance status from the actual activity text.

    This is intentionally deterministic.
    We do not use the LLM for basic status classification.
    """

    # ---------------------------------------------------------
    # Status patterns
    # ---------------------------------------------------------

    COMPLETED_PATTERNS = [

        r"\bcompleted\b",
        r"\bcomplete\b",
        r"\bsuccessfully completed\b",
        r"\bcompleted successfully\b",
        r"\bsuccessfully done\b",
        r"\bfinished\b",
        r"\bdone successfully\b",
        r"\bdecommissioned successfully\b",
        r"\bsuccessfully decommissioned\b",
        r"\bsuccessfully migrated\b",
        r"\bmigration is completed\b",
        r"\bmigration completed\b",
        r"\bimplementation completed\b",
        r"\bimplemented successfully\b",

    ]

    DEPLOYED_PATTERNS = [

        r"\bdeployed to prod\b",
        r"\bdeployed in prod\b",
        r"\bdeployed into prod\b",
        r"\bproduction deployment\b",
        r"\breleased to prod\b",
        r"\breleased into prod\b",
        r"\blive in prod\b",
        r"\blive on prod\b",
        r"\bimplemented in prod\b",
        r"\bdeployed successfully to prod\b",

    ]

    IN_PROGRESS_PATTERNS = [

        r"\bin progress\b",
        r"\bstill in progress\b",
        r"\bcurrently in progress\b",
        r"\bwork is ongoing\b",
        r"\bwork ongoing\b",
        r"\bcurrently working\b",
        r"\bongoing\b",
        r"\bstarted\b",
        r"\binitiated\b",
        r"\bhas started\b",
        r"\bhave started\b",
        r"\bunderway\b",

    ]

    TESTING_PATTERNS = [

        r"\btesting\b",
        r"\bunder testing\b",
        r"\bin testing\b",
        r"\btesting is ongoing\b",
        r"\btesting ongoing\b",
        r"\bintegration testing\b",
        r"\bvalidation\b",
        r"\bunder validation\b",
        r"\bbeing tested\b",
        r"\buat\b",
        r"\bsit testing\b",

    ]

    PLANNED_PATTERNS = [

        r"\bplanned\b",
        r"\bplanned for\b",
        r"\bplanned to\b",
        r"\bscheduled\b",
        r"\bscheduled for\b",
        r"\bwill be deployed\b",
        r"\bwill deploy\b",
        r"\bupcoming\b",
        r"\bnext week\b",
        r"\bnext month\b",

    ]

    FAILED_PATTERNS = [

        r"\bfailed\b",
        r"\bfailure\b",
        r"\bunsuccessful\b",
        r"\berror\b",

    ]

    ROLLBACK_PATTERNS = [

        r"\brollback\b",
        r"\brolled back\b",
        r"\brestored\b",
        r"\brestore\b",

    ]

    # ---------------------------------------------------------
    # Public method
    # ---------------------------------------------------------

    @classmethod
    def infer(cls, text, source_status=None):

        if not text:

            return {
                "status": source_status or "Unknown",
                "reason": "No activity text available",
                "confidence": "Low"
            }

        text = text.lower()

        # -----------------------------------------------------
        # Important:
        #
        # Planned must be checked before deployed.
        #
        # Example:
        # "Deployment to PROD is planned next week"
        #
        # must NOT become Deployed.
        # -----------------------------------------------------

        if cls._matches(text, cls.PLANNED_PATTERNS):

            return {
                "status": "Planned",
                "reason": "Activity contains planned/scheduled future activity",
                "confidence": "High"
            }

        # -----------------------------------------------------
        # Failure
        # -----------------------------------------------------

        if cls._matches(text, cls.FAILED_PATTERNS):

            return {
                "status": "Failed",
                "reason": "Activity contains failure/error evidence",
                "confidence": "High"
            }

        # -----------------------------------------------------
        # Rollback
        # -----------------------------------------------------

        if cls._matches(text, cls.ROLLBACK_PATTERNS):

            return {
                "status": "Rollback",
                "reason": "Activity contains rollback/restore evidence",
                "confidence": "High"
            }

        # -----------------------------------------------------
        # Deployed
        # -----------------------------------------------------

        if cls._matches(text, cls.DEPLOYED_PATTERNS):

            return {
                "status": "Deployed",
                "reason": "Activity contains production deployment evidence",
                "confidence": "High"
            }

        # -----------------------------------------------------
        # Completed
        # -----------------------------------------------------

        if cls._matches(text, cls.COMPLETED_PATTERNS):

            return {
                "status": "Completed",
                "reason": "Activity contains completion evidence",
                "confidence": "High"
            }

        # -----------------------------------------------------
        # Testing
        # -----------------------------------------------------

        if cls._matches(text, cls.TESTING_PATTERNS):

            return {
                "status": "Testing",
                "reason": "Activity contains testing/validation evidence",
                "confidence": "High"
            }

        # -----------------------------------------------------
        # In Progress
        # -----------------------------------------------------

        if cls._matches(text, cls.IN_PROGRESS_PATTERNS):

            return {
                "status": "In Progress",
                "reason": "Activity contains ongoing/in-progress evidence",
                "confidence": "High"
            }

        # -----------------------------------------------------
        # Fall back to source status
        # -----------------------------------------------------

        if source_status and source_status != "Unknown":

            return {
                "status": source_status,
                "reason": "Using status supplied by source RAG report",
                "confidence": "Medium"
            }

        # -----------------------------------------------------
        # Unknown
        # -----------------------------------------------------

        return {
            "status": "Unknown",
            "reason": "No reliable status evidence found",
            "confidence": "Low"
        }

    # ---------------------------------------------------------
    # Pattern matching
    # ---------------------------------------------------------

    @staticmethod
    def _matches(text, patterns):

        for pattern in patterns:

            if re.search(pattern, text, flags=re.IGNORECASE):

                return True

        return False
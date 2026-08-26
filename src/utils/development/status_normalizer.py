import re


class StatusNormalizer:

    # ---------------------------------------------------------
    # Explicit source status
    # ---------------------------------------------------------

    @classmethod
    def normalize(cls, status, activity=None):

        source_status = (status or "").strip().lower()

        activity_text = (activity or "").strip().lower()

        text = f"{source_status} {activity_text}"

        # -----------------------------------------------------
        # 1. Cancelled
        # -----------------------------------------------------

        if "cancelled" in text or "canceled" in text:

            return "Cancelled"

        # -----------------------------------------------------
        # 2. Planned deployment / future activity
        # -----------------------------------------------------
        # Must come BEFORE deployed/completed.
        #
        # Example:
        # "deployment to PROD is planned"
        #
        # should NOT become Deployed.
        # -----------------------------------------------------

        planned_patterns = [

            "is planned",

            "are planned",

            "was planned",

            "were planned",

            "planned for",

            "planned next",

            "scheduled",

            "will be deployed",

            "will deploy",

            "upcoming",

            "to be deployed",

            "to be decommissioned",
            
            "planned",
            
            "Backlog",
            
            "future development"
            
            

        ]

        for pattern in planned_patterns:

            if pattern in text:

                return "Planned"

        # -----------------------------------------------------
        # 3. Explicit testing
        # -----------------------------------------------------

        testing_patterns = [

            "under testing",

            "currently under testing",

            "business testing",

            "testing is ongoing",

            "testing ongoing",

            "in testing",

            "testing",

            "tested",

            "uat",

            "validation"

        ]

        for pattern in testing_patterns:

            if pattern in text:

                return "Testing"

        # -----------------------------------------------------
        # 4. In Progress
        # -----------------------------------------------------

        progress_patterns = [

            "in progress",

            "still in progress",

            "ongoing",

            "work is ongoing",

            "currently working",

            "started",

            "initiated",

            "underway",

            "being migrated",

            "being developed",

            "being implemented",
            
             "currently"

        ]

        for pattern in progress_patterns:

            if pattern in text:

                return "In Progress"

        # -----------------------------------------------------
        # 5. Deployed
        # -----------------------------------------------------

        deployment_patterns = [

            "deployed to prod",

            "deployed in prod",

            "deployed on prod",

            "deployment to prod completed",

            "production deployment",

            "live in prod",

            "released to prod",

            "successfully deployed",
            
            "deployed"

        ]

        for pattern in deployment_patterns:

            if pattern in text:

                return "Deployed"

        # -----------------------------------------------------
        # 6. Completed
        # -----------------------------------------------------

        completed_patterns = [

            "completed",

            "complete",

            "successfully completed",

            "completed successfully",

            "decommissioned successfully",

            "successfully decommissioned",

            "finished",

            "done",

            "working as expected",

            "successful",

            "success",

            "implemented successfully",

            "provisioned successfully",
            
            "implemented",
            
            "provisioned",
            
            "successfully implemented",
            
            "successfully provisioned",
            
            "successfully"

        ]

        for pattern in completed_patterns:

            if pattern in text:

                return "Completed"

        # -----------------------------------------------------
        # 7. Failed
        # -----------------------------------------------------

        if "failed" in text or "failure" in text:

            return "Failed"

        # -----------------------------------------------------
        # 8. Rollback
        # -----------------------------------------------------
        #
        # IMPORTANT:
        # Rollback is an ACTIVITY TYPE.
        # It should not automatically become the STATUS.
        #
        # "Rollback was completed successfully"
        # → Completed
        # -----------------------------------------------------

        # -----------------------------------------------------
        # 9. Monitoring
        # -----------------------------------------------------

        if "monitoring" in text or "monitor" in text:

            return "Monitoring"

        # -----------------------------------------------------
        # 10. Pending
        # -----------------------------------------------------

        if "pending" in text:

            return "Pending"

        # -----------------------------------------------------
        # Unknown
        # -----------------------------------------------------

        return "Unknown"

    # ---------------------------------------------------------
    # Activity-based status inference
    # ---------------------------------------------------------

    @classmethod
    def infer_from_activity(cls, activity):

        text = (activity or "").strip().lower()

        if not text:
            return "Unknown"

        # -----------------------------------------------------
        # Planned
        #
        # Check this FIRST.
        #
        # Example:
        # "Deployment to PROD is planned next week"
        #
        # must be Planned, not Deployed.
        # -----------------------------------------------------

        planned_patterns = [

            r"\bplanned\b",
            r"\bplanned for\b",
            r"\bplanned to\b",
            r"\bscheduled\b",
            r"\bscheduled for\b",
            r"\bwill be deployed\b",
            r"\bwill deploy\b",
            r"\bupcoming\b",
            r"\bnext week\b",
            r"\bnext month\b"

        ]

        if cls._matches(text, planned_patterns):

            return "Planned"

        # -----------------------------------------------------
        # Failed
        # -----------------------------------------------------

        failed_patterns = [

            r"\bfailed\b",
            r"\bfailure\b",
            r"\bunsuccessful\b"

        ]

        if cls._matches(text, failed_patterns):

            return "Failed"

        # -----------------------------------------------------
        # Rollback
        # -----------------------------------------------------

        rollback_patterns = [

            r"\brollback\b",
            r"\brolled back\b",
            r"\brestored\b",
            r"\brestore\b"

        ]

        if cls._matches(text, rollback_patterns):

            return "Rollback"

        # -----------------------------------------------------
        # Deployed
        # -----------------------------------------------------

        deployed_patterns = [

            r"\bdeployed to prod\b",
            r"\bdeployed in prod\b",
            r"\bdeployed into prod\b",
            r"\bproduction deployment\b",
            r"\breleased to prod\b",
            r"\breleased into prod\b",
            r"\blive in prod\b",
            r"\blive on prod\b",
            r"\bimplemented in prod\b",
            r"\bdeployed successfully\b"

        ]

        if cls._matches(text, deployed_patterns):

            return "Deployed"

        # -----------------------------------------------------
        # Completed
        # -----------------------------------------------------

        completed_patterns = [

            r"\bcompleted\b",
            r"\bcomplete\b",
            r"\bsuccessfully completed\b",
            r"\bcompleted successfully\b",
            r"\bfinished\b",
            r"\bdone successfully\b",
            r"\bdecommissioned successfully\b",
            r"\bsuccessfully decommissioned\b",
            r"\bsuccessfully migrated\b",
            r"\bmigration is completed\b",
            r"\bmigration completed\b",
            r"\bimplemented successfully\b"

        ]

        if cls._matches(text, completed_patterns):

            return "Completed"

        # -----------------------------------------------------
        # Testing
        # -----------------------------------------------------

        testing_patterns = [

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
            r"\bsit testing\b"

        ]

        if cls._matches(text, testing_patterns):

            return "Testing"

        # -----------------------------------------------------
        # In Progress
        # -----------------------------------------------------

        progress_patterns = [

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
            r"\bunderway\b"

        ]

        if cls._matches(text, progress_patterns):

            return "In Progress"

        return "Unknown"

    # ---------------------------------------------------------
    # Combined classification
    # ---------------------------------------------------------

    @classmethod
    def normalize_with_activity(cls, status, activity):

        # First trust explicit source status
        source_status = cls.normalize(status)

        # If source provides a reliable status,
        # preserve it.
        if source_status != "Unknown":

            return source_status

        # Otherwise derive status from activity text.
        return cls.infer_from_activity(activity)

    # ---------------------------------------------------------
    # Regex helper
    # ---------------------------------------------------------

    @staticmethod
    def _matches(text, patterns):

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                return True

        return False
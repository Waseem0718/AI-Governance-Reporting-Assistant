class StatusNormalizer:

    @classmethod
    def normalize(cls, status):

        status = (status or "").lower()

        if "working as expected" in status:
            return "Completed"

        if "completed" in status:
            return "Completed"

        if "business testing" in status:
            return "Testing"

        if "testing" in status:
            return "Testing"

        if "in progress" in status:
            return "In Progress"

        if "ongoing" in status:
            return "In Progress"

        if "planned" in status:
            return "Planned"

        if "cancel" in status:
            return "Cancelled"

        return "Unknown"
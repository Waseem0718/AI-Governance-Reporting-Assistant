class SystemNormalizer:

    @staticmethod
    def normalize(system):

        if not system:
            return ""

        # Remove new lines and extra spaces
        system = system.replace("\r", " ")
        system = system.replace("\n", " ")

        # Remove duplicate spaces
        system = " ".join(system.split())

        # Standardize known system names
        mapping = {
            "B ig Panda": "Big Panda",
            "New Relic": "New Relic",
            "New  Relic": "New Relic",
            "Big Panda": "Big Panda"
        }

        return mapping.get(system, system)
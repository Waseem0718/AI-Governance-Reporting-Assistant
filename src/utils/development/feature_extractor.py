import re


class FeatureExtractor:

    @classmethod
    def extract(cls, application, activity, status):

        text = f"{application} {activity} {status}"

        patterns = [

            r"[A-Za-z]+_Release_\d+",
            r"Release_\d+",
            r"Phase\s+\d+",
            r"[A-Za-z]+\s+API",
            r"Mainframe-to-[A-Za-z]+",
            r"SFG-to-[A-Za-z]+",
            r"TPC\s*V3",
            r"CDUD",
            r"OpenShift",
            r"Windows\s+2016",
            r"Windows\s+2022",
            r"DB instances?",
            r"User access review"

        ]

        for pattern in patterns:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:

                return match.group()

        return "Unknown"
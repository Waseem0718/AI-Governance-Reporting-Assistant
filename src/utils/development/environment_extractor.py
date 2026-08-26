import re


class EnvironmentExtractor:

    ENVIRONMENTS = [

        "PROD",
        "PPE",
        "DR",
        "UAT",
        "SIT",
        "Windows 2016",
        "Windows 2022",
        "linux"

    ]

    @classmethod
    def extract(cls, application, activity, status):

        text = f"{application} {activity} {status}"

        found = []

        for env in cls.ENVIRONMENTS:

            if re.search(re.escape(env), text, re.IGNORECASE):

                found.append(env)

        return ", ".join(found) if found else "Unknown"
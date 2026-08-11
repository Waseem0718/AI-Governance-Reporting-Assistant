from models.development_activity import DevelopmentActivity
from utils.development.development_activity_classifier import DevelopmentActivityClassifier


class DevelopmentActivitiesParser:

    def parse(self, table):

        activities = []

        for row in table[1:]:

            if len(row) < 4:
                continue

            result = DevelopmentActivityClassifier.classify(

                application=row[1].text,

                activity=row[2].text,

                status=row[3].text

            )  
                

            activities.append(

                DevelopmentActivity(

                    serial_number=row[0].text,

                    application=row[1].text,

                    activity=row[2].text,

                    status=result["status"],

                    activity_type=result["activity_type"],

                    environment=result["environment"]

                )

            )

        return activities
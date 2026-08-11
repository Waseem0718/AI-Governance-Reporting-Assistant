from models.upcoming_change import UpcomingChange


class UpcomingChangesParser:
    """
    Parses the Upcoming Changes table.
    """

    def parse(self, table):

        changes = []

        # Skip header row
        for row in table[1:]:

            if len(row) < 5:
                continue

            changes.append(

                UpcomingChange(

                    area=row[0].text,

                    change_description=row[1].text,

                    planned_date=row[2].text,

                    change_number=row[3].text,

                    status=row[4].text

                )

            )

        return changes
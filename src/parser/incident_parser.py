from models.incident import Incident


class IncidentParser:
    """
    Parses the Open Incidents table.
    """

    def parse(self, table):

        incidents = []

        # Skip header row
        for row in table[1:]:

            if len(row) < 7:
                continue

            incidents.append(

                Incident(

                    serial_number=row[0].text,

                    zendesk=row[1].text,

                    system=row[2].text,

                    date=row[3].text,

                    problem_description=row[4].text,

                    raised_by=row[5].text,

                    next_steps=row[6].text

                )

            )

        return incidents
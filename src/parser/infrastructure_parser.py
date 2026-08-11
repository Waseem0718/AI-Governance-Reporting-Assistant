from models.infrastructure import Infrastructure
from utils.system_normalizer import SystemNormalizer


class InfrastructureParser:
    """
    Parses Infrastructure Health table.
    """

    def parse(self, table):

        infrastructure = []

        # Skip header row
        for row in table[1:]:

            if len(row) < 8:
                continue

            infrastructure.append(

                Infrastructure(

                    system=SystemNormalizer.normalize(row[0].text),

                    talent=row[1].rag,

                    employment_compliance=row[2].rag,

                    licensing=row[3].rag,

                    peach=row[4].rag,

                    dubs_dasp=row[5].rag,

                    ptx=row[6].rag,

                    comments=row[7].text

                )

            )

        return infrastructure
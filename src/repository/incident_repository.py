class IncidentRepository:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = connection.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_id TEXT,

            zendesk TEXT,

            system TEXT,

            incident_date TEXT,

            problem_description TEXT,

            raised_by TEXT,

            next_steps TEXT,

            UNIQUE(report_id, zendesk),

            FOREIGN KEY(report_id)
                REFERENCES reports(report_id)

        )
        """)

        self.connection.commit()

    def save(self, report):

        for item in report.incidents:

            self.cursor.execute("""

            INSERT INTO incidents(

                report_id,
                zendesk,
                system,
                incident_date,
                problem_description,
                raised_by,
                next_steps

            )

            VALUES(?,?,?,?,?,?,?)

            ON CONFLICT(report_id, zendesk)

            DO UPDATE SET

                system=excluded.system,
                incident_date=excluded.incident_date,
                problem_description=excluded.problem_description,
                raised_by=excluded.raised_by,
                next_steps=excluded.next_steps

            """,

            (

                report.report_id,
                item.zendesk,
                item.system,
                item.date,
                item.problem_description,
                item.raised_by,
                item.next_steps

            ))

        self.connection.commit()

    def _fetch_all(self):

        return [dict(row) for row in self.cursor.fetchall()]

    def get_all(self):

        self.cursor.execute("SELECT * FROM incidents ORDER BY incident_date")

        return self._fetch_all()

    def count(self):

        self.cursor.execute("SELECT COUNT(*) total FROM incidents")

        return self.cursor.fetchone()["total"]

    def get_by_report(self, report_id):

        self.cursor.execute(

            "SELECT * FROM incidents WHERE report_id=?",

            (report_id,)
        )

        return self._fetch_all()

    def get_by_system(self, system):

        self.cursor.execute(

            "SELECT * FROM incidents WHERE system=?",

            (system,)
        )

        return self._fetch_all()

    def get_by_zendesk(self, zendesk):

        self.cursor.execute(

            "SELECT * FROM incidents WHERE zendesk=?",

            (zendesk,)
        )

        return self._fetch_all()

    def get_latest(self):

        self.cursor.execute("""

        SELECT i.*

        FROM incidents i

        JOIN reports r

        ON i.report_id=r.report_id

        WHERE r.report_date=(

            SELECT MAX(report_date)

            FROM reports

        )

        """)

        return self._fetch_all()
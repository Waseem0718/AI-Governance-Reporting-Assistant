class UpcomingChangesRepository:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = connection.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS upcoming_changes(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_id TEXT,

            area TEXT,

            description TEXT,

            planned_date TEXT,

            change_number TEXT,

            status TEXT,

            UNIQUE(report_id, change_number),

            FOREIGN KEY(report_id)
                REFERENCES reports(report_id)

        )
        """)

        self.connection.commit()

    def save(self, report):

        for item in report.upcoming_changes:

            self.cursor.execute("""

            INSERT INTO upcoming_changes(

                report_id,
                area,
                description,
                planned_date,
                change_number,
                status

            )

            VALUES(?,?,?,?,?,?)

            ON CONFLICT(report_id, change_number)

            DO UPDATE SET

                area=excluded.area,
                description=excluded.description,
                planned_date=excluded.planned_date,
                status=excluded.status

            """,

            (

                report.report_id,
                item.area,
                item.change_description,
                item.planned_date,
                item.change_number,
                item.status

            ))

        self.connection.commit()

    def _fetch_all(self):

        return [dict(row) for row in self.cursor.fetchall()]

    def get_all(self):

        self.cursor.execute("SELECT * FROM upcoming_changes ORDER BY planned_date")

        return self._fetch_all()

    def count(self):

        self.cursor.execute("SELECT COUNT(*) total FROM upcoming_changes")

        return self.cursor.fetchone()["total"]

    def get_by_report(self, report_id):

        self.cursor.execute(

            "SELECT * FROM upcoming_changes WHERE report_id=?",

            (report_id,)
        )

        return self._fetch_all()

    def get_by_change_number(self, change_number):

        self.cursor.execute(

            "SELECT * FROM upcoming_changes WHERE change_number=?",

            (change_number,)
        )

        return self._fetch_all()

    def get_by_area(self, area):

        self.cursor.execute(

            "SELECT * FROM upcoming_changes WHERE area=?",

            (area,)
        )

        return self._fetch_all()

    def get_latest(self):

        self.cursor.execute("""

        SELECT u.*

        FROM upcoming_changes u

        JOIN reports r

        ON u.report_id=r.report_id

        WHERE r.report_date=(

            SELECT MAX(report_date)

            FROM reports

        )

        """)

        return self._fetch_all()

    def get_by_date(self, planned_date):

        self.cursor.execute(

            "SELECT * FROM upcoming_changes WHERE planned_date=?",

            (planned_date,)
        )

        return self._fetch_all()
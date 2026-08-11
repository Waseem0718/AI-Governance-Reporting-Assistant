from models.development_activity import DevelopmentActivity


class DevelopmentActivityRepository:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = connection.cursor()

        self.create_table()

    # -----------------------------------------------------
    # Table
    # -----------------------------------------------------

    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS development_activities(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_id TEXT,

            application TEXT,

            activity TEXT,

            status TEXT,

            activity_type TEXT,

            environment TEXT,

            UNIQUE(report_id, application, activity),

            FOREIGN KEY(report_id)
                REFERENCES reports(report_id)

        )

        """)

        self.connection.commit()

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    def save(self, report):

        for item in report.development_activities:

            self.cursor.execute("""

            INSERT INTO development_activities(

                report_id,
                application,
                activity,
                status,
                activity_type,
                environment

            )

            VALUES(?,?,?,?,?,?)

            ON CONFLICT(report_id, application, activity)

            DO UPDATE SET

                status=excluded.status,
                activity_type=excluded.activity_type,
                environment=excluded.environment

            """,

            (

                report.report_id,
                item.application,
                item.activity,
                item.status,
                item.activity_type,
                item.environment

            ))

        self.connection.commit()

    # -----------------------------------------------------
    # Internal
    # -----------------------------------------------------

    def _fetch_all(self):

        return [dict(row) for row in self.cursor.fetchall()]

    # -----------------------------------------------------
    # Basic Queries
    # -----------------------------------------------------

    def get_latest(self):

        self.cursor.execute("""

        SELECT d.*

        FROM development_activities d

        JOIN reports r

        ON d.report_id=r.report_id

        WHERE r.report_date=(

            SELECT MAX(report_date)

            FROM reports

        )

        """)

        return self._fetch_all()

    def get_by_report(self, report_id):

        self.cursor.execute("""

        SELECT *

        FROM development_activities

        WHERE report_id=?

        """,

        (report_id,))

        return self._fetch_all()

    def get_by_application(self, application):

        self.cursor.execute("""

        SELECT d.*,
        r.report_date

        FROM development_activities d

        JOIN reports r

        ON d.report_id=r.report_id

        WHERE d.application=?

        ORDER BY r.report_date

        """,

        (application,))

        return self._fetch_all()

    def search_activity(self, keyword):

        self.cursor.execute("""

        SELECT *

        FROM development_activities

        WHERE activity LIKE ?

        ORDER BY application

        """,

        (f"%{keyword}%",))

        return self._fetch_all()

    # -----------------------------------------------------
    # History
    # -----------------------------------------------------

    def get_application_history(self, application):

        self.cursor.execute("""

        SELECT d.*

        FROM development_activities d

        JOIN reports r

        ON d.report_id=r.report_id

        WHERE d.application=?

        ORDER BY r.report_date

        """,

        (application,))

        return self._fetch_all()

    def get_application_by_month(self, application, month):

        self.cursor.execute("""

        SELECT d.*

        FROM development_activities d

        JOIN reports r

        ON d.report_id=r.report_id

        WHERE d.application=?

        AND substr(r.report_date,1,7)=?

        ORDER BY r.report_date

        """,

        (application, month))

        return self._fetch_all()

    def get_latest_by_application(self, application):

        self.cursor.execute("""

        SELECT d.*

        FROM development_activities d

        JOIN reports r

        ON d.report_id=r.report_id

        WHERE d.application=?

        ORDER BY r.report_date DESC

        LIMIT 1

        """,

        (application,))

        row = self.cursor.fetchone()

        return dict(row) if row else None

    # -----------------------------------------------------
    # Filters
    # -----------------------------------------------------

    def get_by_activity_type(self, activity_type):

        self.cursor.execute("""

        SELECT *

        FROM development_activities

        WHERE activity_type=?

        ORDER BY application

        """,

        (activity_type,))

        return self._fetch_all()

    def get_by_environment(self, environment):

        self.cursor.execute("""

        SELECT *

        FROM development_activities

        WHERE environment=?

        ORDER BY application

        """,

        (environment,))

        return self._fetch_all()

    def get_by_status(self, status):

        self.cursor.execute("""

        SELECT *

        FROM development_activities

        WHERE status=?

        ORDER BY application

        """,

        (status,))

        return self._fetch_all()

    # -----------------------------------------------------
    # Lists
    # -----------------------------------------------------

    def get_applications(self):

        self.cursor.execute("""

        SELECT DISTINCT application

        FROM development_activities

        ORDER BY application

        """)

        return [

            row["application"]

            for row in self.cursor.fetchall()

        ]

    def get_activity_types(self):

        self.cursor.execute("""

        SELECT DISTINCT activity_type

        FROM development_activities

        ORDER BY activity_type

        """)

        return [

            row["activity_type"]

            for row in self.cursor.fetchall()

        ]

    def get_environments(self):

        self.cursor.execute("""

        SELECT DISTINCT environment

        FROM development_activities

        ORDER BY environment

        """)

        return [

            row["environment"]

            for row in self.cursor.fetchall()

        ]

    # -----------------------------------------------------
    # Date Queries
    # -----------------------------------------------------

    def get_between_dates(self, start_date, end_date):

        self.cursor.execute("""

        SELECT d.*

        FROM development_activities d

        JOIN reports r

        ON d.report_id=r.report_id

        WHERE r.report_date BETWEEN ? AND ?

        ORDER BY r.report_date

        """,

        (start_date, end_date))

        return self._fetch_all()

    # -----------------------------------------------------
    # Counts
    # -----------------------------------------------------

    def count(self):

        self.cursor.execute("""

        SELECT COUNT(*) total

        FROM development_activities

        """)

        return self.cursor.fetchone()["total"]

    def count_by_application(self, application):

        self.cursor.execute("""

        SELECT COUNT(*) total

        FROM development_activities

        WHERE application=?

        """,

        (application,))

        return self.cursor.fetchone()["total"]

    def count_by_activity_type(self, activity_type):

        self.cursor.execute("""

        SELECT COUNT(*) total

        FROM development_activities

        WHERE activity_type=?

        """,

        (activity_type,))

        return self.cursor.fetchone()["total"]

    def count_by_environment(self, environment):

        self.cursor.execute("""

        SELECT COUNT(*) total

        FROM development_activities

        WHERE environment=?

        """,

        (environment,))

        return self.cursor.fetchone()["total"]
    
    def get_all(self):

        self.cursor.execute("""

        SELECT d.*,
            r.report_date

        FROM development_activities d

        JOIN reports r
        ON d.report_id = r.report_id

        ORDER BY r.report_date,
                d.application

        """)

        return self._fetch_all()
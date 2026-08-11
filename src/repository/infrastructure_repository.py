import sqlite3


class InfrastructureRepository:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = connection.cursor()

        self.create_table()

    # --------------------------------------------------------
    # Create Table
    # --------------------------------------------------------

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS infrastructure(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_id TEXT,

            system TEXT,

            talent TEXT,

            employment_compliance TEXT,

            licensing TEXT,

            peach TEXT,

            dubs_dasp TEXT,

            ptx TEXT,

            comments TEXT,

            UNIQUE(report_id, system),

            FOREIGN KEY(report_id)
                REFERENCES reports(report_id)

        )
        """)

        self.connection.commit()

    # --------------------------------------------------------
    # Save Infrastructure
    # --------------------------------------------------------

    def save(self, report):

        for item in report.infrastructure:

            self.cursor.execute("""
            INSERT INTO infrastructure(

                report_id,
                system,
                talent,
                employment_compliance,
                licensing,
                peach,
                dubs_dasp,
                ptx,
                comments

            )

            VALUES(?,?,?,?,?,?,?,?,?)

            ON CONFLICT(report_id, system)

            DO UPDATE SET

                talent=excluded.talent,
                employment_compliance=excluded.employment_compliance,
                licensing=excluded.licensing,
                peach=excluded.peach,
                dubs_dasp=excluded.dubs_dasp,
                ptx=excluded.ptx,
                comments=excluded.comments

            """,

            (

                report.report_id,
                item.system,
                item.talent,
                item.employment_compliance,
                item.licensing,
                item.peach,
                item.dubs_dasp,
                item.ptx,
                item.comments

            ))

        self.connection.commit()

    # --------------------------------------------------------
    # Helper
    # --------------------------------------------------------

    def _fetch_all(self):

        return [dict(row) for row in self.cursor.fetchall()]

    # --------------------------------------------------------
    # Query Methods
    # --------------------------------------------------------

    def get_all(self):

        self.cursor.execute("""
        SELECT *
        FROM infrastructure
        ORDER BY report_id, system
        """)

        return self._fetch_all()

    def count(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM infrastructure
        """)

        return self.cursor.fetchone()["total"]

    def get_by_report(self, report_id):

        self.cursor.execute("""
        SELECT *
        FROM infrastructure
        WHERE report_id=?
        ORDER BY system
        """, (report_id,))

        return self._fetch_all()

    def get_by_system(self, system):

        self.cursor.execute("""
        SELECT *
        FROM infrastructure
        WHERE system=?
        ORDER BY report_id
        """, (system,))

        return self._fetch_all()

    def get_latest(self):

        self.cursor.execute("""
        SELECT i.*
        FROM infrastructure i

        JOIN reports r
            ON i.report_id = r.report_id

        WHERE r.report_date = (

            SELECT MAX(report_date)
            FROM reports

        )

        ORDER BY i.system
        """)

        return self._fetch_all()

    def get_by_date(self, report_date):

        self.cursor.execute("""
        SELECT i.*

        FROM infrastructure i

        JOIN reports r

            ON i.report_id = r.report_id

        WHERE r.report_date = ?

        ORDER BY i.system
        """, (report_date,))

        return self._fetch_all()

    def get_non_green(self):

        self.cursor.execute("""
        SELECT *

        FROM infrastructure

        WHERE

            talent <> 'GREEN'

            OR employment_compliance <> 'GREEN'

            OR licensing <> 'GREEN'

            OR peach <> 'GREEN'

            OR dubs_dasp <> 'GREEN'

            OR ptx <> 'GREEN'

        ORDER BY report_id
        """)

        return self._fetch_all()

    def get_status_history(self, system):

        self.cursor.execute("""
        SELECT

            r.report_date,

            i.*

        FROM infrastructure i

        JOIN reports r

            ON i.report_id = r.report_id

        WHERE i.system = ?

        ORDER BY r.report_date
        """, (system,))

        return self._fetch_all()

    def get_systems_with_comments(self):

        self.cursor.execute("""
        SELECT *

        FROM infrastructure

        WHERE comments IS NOT NULL

        AND TRIM(comments) <> ''

        AND comments <> 'No Issues Reported'

        ORDER BY report_id
        """)

        return self._fetch_all()

    def get_system_names(self):

        self.cursor.execute("""
        SELECT DISTINCT system

        FROM infrastructure

        ORDER BY system
        """)

        return [row["system"] for row in self.cursor.fetchall()]
    
    def get_latest_infrastructure(self, report_id):

        self.cursor.execute(
            """
            SELECT *
            FROM infrastructure
            WHERE report_id = ?
            ORDER BY system
            """,
            (report_id,)
        )

        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_status_summary(self, report_id):

        rows = self.get_latest_infrastructure(report_id)

        summary = {
            "GREEN": 0,
            "AMBER": 0,
            "RED": 0,
            "GREY": 0,
            "UNKNOWN": 0
        }

        for row in rows:

            statuses = [

                    row["talent"],
                    row["employment_compliance"],
                    row["licensing"],
                    row["peach"],
                    row["dubs_dasp"],
                    row["ptx"]

                ]

            if "RED" in statuses:
                summary["RED"] += 1

            elif "AMBER" in statuses:
                summary["AMBER"] += 1

            elif "UNKNOWN" in statuses:
                summary["UNKNOWN"] += 1

            else:
                summary["GREEN"] += 1

        return summary
    
    def get_overall_status(self, report_id):

        summary = self.get_status_summary(report_id)

        if summary["RED"] > 0:
            return "RED"

        if summary["AMBER"] > 0:
            return "AMBER"

        if summary["GREY"] > 0:
            return "GREY"

        if summary["UNKNOWN"] > 0:
            return "UNKNOWN"

        return "GREEN"
    
    def get_amber_systems(self, report_id):

        rows = self.get_latest_infrastructure(report_id)

        systems = []

        for row in rows:

            statuses = [

                row["talent"],
                row["employment_compliance"],
                row["licensing"],
                row["peach"],
                row["dubs_dasp"],
                row["ptx"]

            ]

            if "AMBER" in statuses:

                systems.append(row["system"])

        return systems
    
    def get_grey_systems(self, report_id):

        rows = self.get_latest_infrastructure(report_id)

        systems = []

        for row in rows:

            statuses = [

                    row["talent"],
                    row["employment_compliance"],
                    row["licensing"],
                    row["peach"],
                    row["dubs_dasp"],
                    row["ptx"]

                ]
            if "GREY" in statuses:

                systems.append(row["system"])

        return systems
    
    
    def get_non_green_systems(self, report_id):

        rows = self.get_latest_infrastructure(report_id)

        issues = []

        for row in rows:

            statuses = [

            row["talent"],
            row["employment_compliance"],
            row["licensing"],
            row["peach"],
            row["dubs_dasp"],
            row["ptx"]

        ]

            overall = "GREEN"

            if "RED" in statuses:
                overall = "RED"

            elif "AMBER" in statuses:
                overall = "AMBER"

            elif "GREY" in statuses:
                overall = "GREY"

            elif "UNKNOWN" in statuses:
                overall = "UNKNOWN"

            if overall != "GREEN":

                issues.append({

                    "system": row["system"],

                    "status": overall,

                    "comments": row["comments"]

                })

        return issues
    
    def _get_overall_system_status(self, row):

        statuses = [

        row["talent"],
        row["employment_compliance"],
        row["licensing"],
        row["peach"],
        row["dubs_dasp"],
        row["ptx"]

    ]

        if "RED" in statuses:
            return "RED"

        if "AMBER" in statuses:
            return "AMBER"

        if "UNKNOWN" in statuses:
            return "UNKNOWN"

        return "GREEN"
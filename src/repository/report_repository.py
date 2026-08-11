import sqlite3


class ReportRepository:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = connection.cursor()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_id TEXT UNIQUE,

            report_date TEXT,

            subject TEXT,

            sender_name TEXT,

            sender_email TEXT,

            generated_at TEXT,

            version TEXT

        )
        """)

    def save(self, report):

        self.cursor.execute("""
        INSERT INTO reports(

            report_id,
            report_date,
            subject,
            sender_name,
            sender_email,
            generated_at,
            version

        )

        VALUES(?,?,?,?,?,?,?)

        ON CONFLICT(report_id)

        DO UPDATE SET

            report_date=excluded.report_date,
            subject=excluded.subject,
            sender_name=excluded.sender_name,
            sender_email=excluded.sender_email,
            generated_at=excluded.generated_at,
            version=excluded.version

        """,

        (

            report.report_id,
            report.report_date,
            report.subject,
            report.sender["name"],
            report.sender["email"],
            report.generated_at,
            report.version

        ))

        self.connection.commit()   
    
    def report_exists(self, report_id):

        self.cursor.execute(
            """
            SELECT 1
            FROM reports
            WHERE report_id = ?
            """,
            (report_id,)
        )

        return self.cursor.fetchone() is not None
    
    def get_latest_report(self):

        self.cursor.execute(
            """
            SELECT *
            FROM reports
            ORDER BY report_date DESC
            LIMIT 1
            """
        )

        row = self.cursor.fetchone()

        return dict(row) if row else None
    
    def get_report(self, report_id):

        self.cursor.execute(
            """
            SELECT *
            FROM reports
            WHERE report_id = ?
            """,
            (report_id,)
        )

        row = self.cursor.fetchone()

        return dict(row) if row else None
    
    def get_all_reports(self):

        self.cursor.execute(
            """
            SELECT *
            FROM reports
            ORDER BY report_date DESC
            """
        )

        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_reports_between(self, start_date, end_date):

        self.cursor.execute(
            """
            SELECT *
            FROM reports
            WHERE report_date BETWEEN ? AND ?
            ORDER BY report_date
            """,
            (start_date, end_date)
        )

        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_reports_by_month(self, month):

        self.cursor.execute(
            """
            SELECT *
            FROM reports
            WHERE substr(report_date,1,7)=?
            ORDER BY report_date
            """,
            (month,)
        )

        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_reports_by_sender(self, sender):

        self.cursor.execute(
            """
            SELECT *
            FROM reports
            WHERE sender_name = ?
            ORDER BY report_date
            """,
            (sender,)
        )

        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_total_reports(self):

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM reports
            """
        )

        return self.cursor.fetchone()[0]
    
    def get_latest_report_date(self):

        self.cursor.execute(
            """
            SELECT MAX(report_date)
            FROM reports
            """
        )

        return self.cursor.fetchone()[0]
    
    def get_oldest_report(self):

        self.cursor.execute(
            """
            SELECT *
            FROM reports
            ORDER BY report_date
            LIMIT 1
            """
        )

        row = self.cursor.fetchone()

        return dict(row) if row else None
    
    def get_by_report_id(self, report_id):

        self.cursor.execute("""

        SELECT *

        FROM reports

        WHERE report_id=?

        """, (report_id,))

        row = self.cursor.fetchone()

        return dict(row) if row else None
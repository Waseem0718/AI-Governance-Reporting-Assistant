from repository.report_repository import ReportRepository
from repository.infrastructure_repository import InfrastructureRepository
from repository.vulnerability_repository import VulnerabilityRepository
from repository.upcoming_changes_repository import UpcomingChangesRepository
from repository.incident_repository import IncidentRepository
from repository.development_repository import DevelopmentActivityRepository
from repository.vulnerability_finding_repository import VulnerabilityFindingRepository

from database.database_manager import DatabaseManager


class RepositoryManager:

    def __init__(self):

        db = DatabaseManager()

        connection = db.get_connection()

        self.db = db

        self.report_repository = ReportRepository(connection)

        self.infrastructure_repository = InfrastructureRepository(connection)

        self.vulnerability_repository = VulnerabilityRepository(connection)

        self.upcoming_changes_repository = UpcomingChangesRepository(connection)

        self.incident_repository = IncidentRepository(connection)

        self.development_repository = DevelopmentActivityRepository(connection)

        self.vulnerability_finding_repository = VulnerabilityFindingRepository(connection)

        self.create_tables()
        
    def create_tables(self):

        self.report_repository.create_table()

        self.infrastructure_repository.create_table()

        self.vulnerability_repository.create_table()

        self.upcoming_changes_repository.create_table()

        self.incident_repository.create_table()

        self.development_repository.create_table()
        
        self.vulnerability_finding_repository.create_table()

        self.db.commit()
        
    def save(self, report):

        self.report_repository.save(report)

        self.infrastructure_repository.save(report)

        self.vulnerability_repository.save(report)

        self.upcoming_changes_repository.save(report)

        self.incident_repository.save(report)

        self.development_repository.save(report)
        
        self.vulnerability_finding_repository.save(report)

        self.db.commit()
        
    
    def get_latest_report(self):
        return self.report_repository.get_latest_report()


    def get_latest_infrastructure(self):
        return self.infrastructure_repository.get_latest()


    def get_open_incidents(self):
        return self.incident_repository.get_open_incidents()


    def get_highest_risk(self):
        return self.vulnerability_repository.get_highest_risk()
    
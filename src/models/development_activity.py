from dataclasses import dataclass

@dataclass
class DevelopmentActivity:

    serial_number: str

    application: str

    activity: str

    status: str

    activity_type: str

    environment: str
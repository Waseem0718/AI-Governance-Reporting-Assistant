class ReportPrinter:
    """
    Prints a RagReport in a readable format.
    """

    def print(self, report):

        print("\n" + "=" * 80)
        print(report.subject)
        print("=" * 80)

        print(f"Sender         : {report.sender['email']}")
        print(f"Received Date  : {report.received_date}")

        self._print_infrastructure(report)

        self._print_vulnerabilities(report)

        self._print_changes(report)

        self._print_incidents(report)

        self._print_development(report)

    # -----------------------------------------------------

    def _print_infrastructure(self, report):

        print("\nInfrastructure Health")

        for row in report.infrastructure:

            print("-" * 60)

            print(f"System       : {row.system}")
            print(f"Talent       : {row.talent}")
            print(f"Compliance   : {row.employment_compliance}")
            print(f"Licensing    : {row.licensing}")
            print(f"PEACH        : {row.peach}")
            print(f"DUBS & DASP  : {row.dubs_dasp}")
            print(f"PTX          : {row.ptx}")
            print(f"Comments     : {row.comments}")

    # -----------------------------------------------------

    def _print_vulnerabilities(self, report):

        print("\nVulnerability Queue Status")

        for item in report.vulnerabilities:

            print("-" * 60)

            print(f"Queue Name : {item.queue_name}")
            print(f"Risk Meter : {item.risk_meter}")
            print(f"Top Fixes  : {item.top_fixes}")

    # -----------------------------------------------------

    def _print_changes(self, report):

        print("\nUpcoming Changes")

        for item in report.upcoming_changes:

            print("-" * 60)

            print(f"Area             : {item.area}")
            print(f"Description      : {item.change_description}")
            print(f"Planned Date     : {item.planned_date}")
            print(f"Change Number    : {item.change_number}")
            print(f"Status           : {item.status}")

    # -----------------------------------------------------

    def _print_incidents(self, report):

        print("\nOpen Incidents")

        for item in report.incidents:

            print("-" * 60)

            print(f"S.No            : {item.serial_number}")
            print(f"Zendesk         : {item.zendesk}")
            print(f"System          : {item.system}")
            print(f"Date            : {item.date}")
            print(f"Problem         : {item.problem_description}")
            print(f"Raised By       : {item.raised_by}")
            print(f"Next Steps      : {item.next_steps}")

    # -----------------------------------------------------

    def _print_development(self, report):

        print("\nDevelopment Activities")

        for item in report.development_activities:

            print("-" * 60)

            print(f"S.No            : {item.serial_number}")
            print(f"Application     : {item.application}")
            print(f"Activity        : {item.activity}")
            print(f"Status          : {item.status}")
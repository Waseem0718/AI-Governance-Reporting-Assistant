from collections import Counter


class SectionSummarizer:
    """
    Generates section-wise summaries from a RAG report.
    """

    def summarize_infrastructure(self, infrastructure):

        summary = []

        summary.extend(self._summarize_rag_status(infrastructure))
        summary.extend(self._summarize_comments(infrastructure))

        return summary

    def _summarize_rag_status(self, infrastructure):
        """
        Summarizes the overall RAG health.
        """

        summary = []

        counter = Counter()

        applications = [
            "Talent",
            "Employment Compliance",
            "Licensing",
            "PEACH",
            "DUBS & DASP",
            "PTX"
        ]

        for row in infrastructure:

            statuses = [
                row.talent,
                row.employment_compliance,
                row.licensing,
                row.peach,
                row.dubs_dasp,
                row.ptx
            ]

            for app, status in zip(applications, statuses):

                if status:
                    counter[status] += 1

        if counter.get("RED", 0) == 0 and counter.get("AMBER", 0) == 0:

            summary.append("All monitored applications are GREEN.")

        else:

            if counter.get("RED", 0):

                summary.append(
                    f"{counter['RED']} RED status(s) detected across monitored applications."
                )

            if counter.get("AMBER", 0):

                summary.append(
                    f"{counter['AMBER']} AMBER status(s) detected across monitored applications."
                )

        return summary

    def _summarize_comments(self, infrastructure):
        """
        Summarizes infrastructure comments.
        """
        
        summary = []

        for row in infrastructure:

            if not row.comments:
                continue

            comment = row.comments.strip()

            if comment.lower() == "no issues reported":
                continue

            if comment.lower() == "expire dates were mentioned.":
                continue

            summary.append(
                f"{row.system}: {comment}"
            )

        return summary
    
    def summarize_vulnerabilities(self, vulnerabilities):

        summary = []

        if not vulnerabilities:
            summary.append("No vulnerability queues found.")
            return summary

        summary.append(
            f"{len(vulnerabilities)} vulnerability queue(s) currently being tracked."
        )

        highest = max(
            vulnerabilities,
            key=lambda x: int(x.risk_meter)
        )

        summary.append(
            f"Highest Risk Meter: {highest.risk_meter} ({highest.queue_name})."
        )

        openssl = 0
        defender = 0
        dotnet = 0

        for item in vulnerabilities:

            fixes = item.top_fixes.lower()

            if "openssl" in fixes:
                openssl += 1

            if "defender" in fixes:
                defender += 1

            if ".net" in fixes:
                dotnet += 1

        if openssl:
            summary.append("OpenSSL vulnerabilities are still under remediation.")

        if defender:
            summary.append("Microsoft Defender vulnerabilities are present.")

        if dotnet:
            summary.append(".NET package vulnerabilities are being addressed.")

        return summary
    
    def summarize_changes(self, changes):

        summary = []

        if not changes:

            summary.append("No upcoming infrastructure changes.")

            return summary

        summary.append(
            f"{len(changes)} planned change(s) scheduled."
        )

        for item in changes:

            summary.append(
                f"{item.area} ({item.change_number}) scheduled for {item.planned_date}."
            )

        return summary
    
    def summarize_incidents(self, incidents):

        summary = []

        if not incidents:

            summary.append("No open incidents.")

            return summary

        summary.append(
            f"{len(incidents)} active incident(s)."
        )

        systems = sorted(
            set(
                incident.system
                for incident in incidents
            )
        )

        summary.append(
            "Affected systems: " + ", ".join(systems)
        )

        oldest = min(
            incidents,
            key=lambda x: x.date
        )

        summary.append(
            f"Oldest incident: {oldest.zendesk} ({oldest.system})."
        )

        return summary
    
    def summarize_development(self, activities):

        summary = []

        if not activities:

            summary.append("No development activities.")

            return summary

        summary.append(
            f"{len(activities)} active development initiative(s)."
        )

        deployed = 0
        testing = 0
        waiting = 0

        for item in activities:

            status = item.status.lower()

            if "prod" in status or "successfully" in status:

                deployed += 1

            if "testing" in status:

                testing += 1

            if "waiting" in status or "sign-off" in status:

                waiting += 1

        if deployed:

            summary.append(
                f"{deployed} deployment(s) completed."
            )

        if testing:

            summary.append(
                f"{testing} release(s) under business testing."
            )

        if waiting:

            summary.append(
                f"{waiting} release(s) awaiting approval or sign-off."
            )

        return summary
    
    def print_summary(self, title, summary):

        print()

        print(title)

        print("-" * 60)

        for line in summary:

            print(f"• {line}")

from utils.development.development_activity_classifier import (
    DevelopmentActivityClassifier
)


TEST_CASES = [

    # ---------------------------------------------------------
    # Migration
    # ---------------------------------------------------------

    {
        "application": "DASP",
        "activity": "Migration is still in progress for DASP.",
        "source_status": "Unknown",
        "expected_type": "Migration",
        "expected_status": "In Progress",
        "expected_environment": "Unknown"
    },

    {
        "application": "DUBS",
        "activity": "Migration is completed for DUBS.",
        "source_status": "Unknown",
        "expected_type": "Migration",
        "expected_status": "Completed",
        "expected_environment": "Unknown"
    },

    # ---------------------------------------------------------
    # Decommission
    # ---------------------------------------------------------

    {
        "application": "DUBS",
        "activity": "Old 2016 DUBS servers are decommissioned successfully.",
        "source_status": "Unknown",
        "expected_type": "Decommission",
        "expected_status": "Completed",
        "expected_environment": "Unknown"
    },

    {
        "application": "BACS/PTX",
        "activity": "Old servers are planned to be decommissioned next week.",
        "source_status": "Unknown",
        "expected_type": "Decommission",
        "expected_status": "Planned",
        "expected_environment": "Unknown"
    },

    # ---------------------------------------------------------
    # Licensing Release
    # ---------------------------------------------------------

    {
        "application": "Licensing",
        "activity": "Licensing_Release_20260708 is under testing.",
        "source_status": "Unknown",
        "expected_type": "Release",
        "expected_status": "Testing",
        "expected_environment": "Unknown"
    },

    {
        "application": "Licensing",
        "activity": "Licensing_Release_20260708 was deployed to PROD.",
        "source_status": "Unknown",
        "expected_type": "Release",
        "expected_status": "Deployed",
        "expected_environment": "PROD"
    },

    {
        "application": "Licensing",
        "activity": "Deployment to PROD is planned next week.",
        "source_status": "Unknown",
        "expected_type": "Release",
        "expected_status": "Planned",
        "expected_environment": "PROD"
    },

    {
        "application": "Licensing",
        "activity": "Testing completed, deployment to PROD is planned.",
        "source_status": "Unknown",
        "expected_type": "Release",
        "expected_status": "Planned",
        "expected_environment": "PROD"
    },

    {
        "application": "Licensing",
        "activity": "Licensing_Release_20260708",
        "source_status": "Testing",
        "expected_type": "Release",
        "expected_status": "Testing",
        "expected_environment": "Unknown"
    },

    # ---------------------------------------------------------
    # Licensing API
    # ---------------------------------------------------------

    {
        "application": "Licensing",
        "activity": "We have initiated the OpenShift migration for the Licensing API.",
        "source_status": "Unknown",
        "expected_type": "Migration",
        "expected_status": "In Progress",
        "expected_environment": "Unknown"
    },

    # ---------------------------------------------------------
    # Rollback
    # ---------------------------------------------------------

    {
        "application": "Licensing",
        "activity": "Rollback was completed successfully.",
        "source_status": "Unknown",
        "expected_type": "Rollback",
        "expected_status": "Completed",
        "expected_environment": "Unknown"
    },

    # ---------------------------------------------------------
    # Cluster
    # ---------------------------------------------------------

    {
        "application": "Licensing",
        "activity": "New cluster infrastructure has been provisioned in PROD.",
        "source_status": "Unknown",
        "expected_type": "Provisioning",
        "expected_status": "Completed",
        "expected_environment": "PROD"
    },

    # ---------------------------------------------------------
    # TLR
    # ---------------------------------------------------------

    {
        "application": "Licensing",
        "activity": "TLR health check has been implemented in PROD.",
        "source_status": "Unknown",
        "expected_type": "Implementation",
        "expected_status": "Completed",
        "expected_environment": "PROD"
    },

    {
        "application": "PTX",
        "activity": "TLR health check is currently under testing in PPE.",
        "source_status": "Unknown",
        "expected_type": "Testing",
        "expected_status": "Testing",
        "expected_environment": "PPE"
    },

    # ---------------------------------------------------------
    # Backlog
    # ---------------------------------------------------------

    {
        "application": "Licensing",
        "activity": "Backlog item identified for future development.",
        "source_status": "Unknown",
        "expected_type": "Backlog",
        "expected_status": "Planned",
        "expected_environment": "Unknown"
    },

    # ---------------------------------------------------------
    # Arthaus
    # ---------------------------------------------------------

    {
        "application": "Arthaus",
        "activity": "Arthaus development has started using Kubernetes.",
        "source_status": "Unknown",
        "expected_type": "Development",
        "expected_status": "In Progress",
        "expected_environment": "Unknown"
    },

    # ---------------------------------------------------------
    # Employment Compliance
    # ---------------------------------------------------------

    {
        "application": "Employment Compliance",
        "activity": "Employment Compliance release has been deployed to PROD.",
        "source_status": "Unknown",
        "expected_type": "Release",
        "expected_status": "Deployed",
        "expected_environment": "PROD"
    },

    # ---------------------------------------------------------
    # PEACH
    # ---------------------------------------------------------

    {
        "application": "PEACH",
        "activity": "Phase 10 release is currently under testing in PPE.",
        "source_status": "Unknown",
        "expected_type": "Release",
        "expected_status": "Testing",
        "expected_environment": "PPE"
    },

    # ---------------------------------------------------------
    # Talent
    # ---------------------------------------------------------

    {
        "application": "Talent",
        "activity": "Release_20260617 has been deployed to PROD.",
        "source_status": "Unknown",
        "expected_type": "Release",
        "expected_status": "Deployed",
        "expected_environment": "PROD"
    }
]


def main():

    print("=" * 80)
    print("AGRA DEVELOPMENT CLASSIFICATION TEST")
    print("=" * 80)

    passed = 0
    failed = 0

    for index, case in enumerate(TEST_CASES, start=1):

        result = DevelopmentActivityClassifier.classify(
            application=case["application"],
            activity=case["activity"],
            status=case["source_status"]
        )

        actual_type = result["activity_type"]
        actual_status = result["status"]
        actual_environment = result["environment"]

        type_ok = actual_type == case["expected_type"]
        status_ok = actual_status == case["expected_status"]
        environment_ok = (
            actual_environment == case["expected_environment"]
        )

        success = (
            type_ok
            and status_ok
            and environment_ok
        )

        print("\n" + "-" * 80)

        print(f"Test #{index}")
        print(f"Application : {case['application']}")
        print(f"Activity    : {case['activity']}")
        print(f"Source      : {case['source_status']}")

        print()
        print(f"Expected Type        : {case['expected_type']}")
        print(f"Actual Type          : {actual_type}")

        print(f"Expected Status      : {case['expected_status']}")
        print(f"Actual Status        : {actual_status}")

        print(f"Expected Environment : {case['expected_environment']}")
        print(f"Actual Environment   : {actual_environment}")

        if success:

            print("\nRESULT : PASS")
            passed += 1

        else:

            print("\nRESULT : FAIL")
            failed += 1

    print("\n" + "=" * 80)
    print("CLASSIFICATION TEST SUMMARY")
    print("=" * 80)

    print(f"Total Tests : {len(TEST_CASES)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    if failed == 0:

        print("\nALL CLASSIFICATION TESTS PASSED.")

    else:

        print(
            f"\n{failed} classification test(s) need attention."
        )


if __name__ == "__main__":
    main()
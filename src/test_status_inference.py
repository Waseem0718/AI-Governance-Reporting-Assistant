from services.analytics.history.topic_analyzer.status_inference import StatusInference


tests = [

    "Migration is still in progress for DASP.",

    "Migration is completed for DUBS.",

    "Old 2016 DUBS servers are decommissioned successfully.",

    "Deployment to PROD is planned next week.",

    "The release is currently under testing.",

    "Licensing_Release_20260708 was deployed to PROD.",

    "We have initiated the OpenShift migration.",

    "Testing completed, deployment to PROD is planned.",

]


for text in tests:

    result = StatusInference.infer(text)

    print()
    print("=" * 70)
    print("Activity :", text)
    print("Status   :", result["status"])
    print("Reason   :", result["reason"])
    print("Confidence:", result["confidence"])
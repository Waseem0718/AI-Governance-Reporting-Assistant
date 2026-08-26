
from parser.msg_loader import MsgLoader
from builder.report_builder import ReportBuilder
from repository.repository_manager import RepositoryManager

from services.analytics.history.topic_analyzer.development_topic_analyzer import DevelopmentTopicAnalyzer
from services.ai.prompt_builder import PromptBuilder
from services.ai.ollama_client import OllamaClient


def main():

    # ----------------------------------------------------
    # Load Emails
    # ----------------------------------------------------

    loader = MsgLoader("samples/rag_reports_july")

    emails = loader.load_messages()

    print(f"\nSuccessfully Loaded : {len(emails)} Email(s)")

    # ----------------------------------------------------
    # Repository
    # ----------------------------------------------------

    repository = RepositoryManager()

    # ----------------------------------------------------
    # Import Reports
    # ----------------------------------------------------
    IMPORT_REPORTS = True

    if IMPORT_REPORTS:

        builder = ReportBuilder()

        for email in emails:

            report = builder.build(email)

            repository.save(report)

    # ----------------------------------------------------
    # Development Topic Analyzer
    # ----------------------------------------------------

    REPORTING_MONTH = "2026-07"

    analyzer = DevelopmentTopicAnalyzer(repository)

    contexts = analyzer.analyze_all(REPORTING_MONTH)
    print("\n========== GENERATED AI CONTEXT ==========")

    for context in contexts:

        print("\n----------------------------------------")
        print("TOPIC:", context["topic"])

        print("\nTIMELINE:")
        print(context["timeline_summary"])

        print("\nBUSINESS STORY:")
        for story in context["business_story"]:
            print(" -", story)

        print("\nCURRENT STATE:")
        print(context["current_state"])

        print("\nMILESTONES:")
        for milestone in context["business_milestones"]:
            print(" -", milestone)
    
    
    # ----------------------------------------------------
    # Prompt Builder
    # ----------------------------------------------------

    prompt = PromptBuilder.build_governance_prompt(contexts)

    # ----------------------------------------------------
    # LLM
    # ----------------------------------------------------

    client = OllamaClient()

    summary = client.generate(
        system_prompt=prompt["system"],
        user_prompt=prompt["user"]
    )

    print("\n========== MONTHLY GOVERNANCE SUMMARY ==========\n")

    print(summary)

if __name__ == "__main__":

    main()
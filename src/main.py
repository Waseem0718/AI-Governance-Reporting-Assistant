
from parser.msg_loader import MsgLoader
from builder.report_builder import ReportBuilder
from repository.repository_manager import RepositoryManager

from services.analytics.history.topic_analyzer.development_topic_analyzer import DevelopmentTopicAnalyzer
from services.ai.prompt_builder import PromptBuilder
from services.ai.ollama_client import OllamaClient
IMPORT_REPORTS = True


def main():

    # ----------------------------------------------------
    # Load Emails
    # ----------------------------------------------------

    loader = MsgLoader("samples/rag_reports")

    emails = loader.load_messages()

    print(f"\nSuccessfully Loaded : {len(emails)} Email(s)")

    # ----------------------------------------------------
    # Repository
    # ----------------------------------------------------

    repository = RepositoryManager()

    # ----------------------------------------------------
    # Import Reports
    # ----------------------------------------------------

    if IMPORT_REPORTS:

        builder = ReportBuilder()

        for email in emails:

            report = builder.build(email)

            repository.save(report)

    # ----------------------------------------------------
    # Development Topic Analyzer
    # ----------------------------------------------------

    analyzer = DevelopmentTopicAnalyzer(repository)

    contexts = analyzer.analyze_all()
    """print("\n========== AI CONTEXT ==========\n")
    
        for context in contexts:
    
            print("--------------------------------------")
    
            print("Topic :", context["topic"])
    
            print()
    
            print("Timeline Summary")
    
            for key, value in context["timeline_summary"].items():
    
                print(f"{key:20}: {value}")
    
            print()
    
            print("Business Story")
    
            for story in context["business_story"]:
    
                print(" •", story)
    
            print()
    
            print("Current State")
    
            for key, value in context["current_state"].items():
    
                print(f"{key:20}: {value}")
    
            print()
    
            print("Business Milestones")
    
            for milestone in context["business_milestones"]:
    
                print(" •", milestone)
    
    """
    
    
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
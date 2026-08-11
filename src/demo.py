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
    # BUSINESS EVOLUTION (For Demo / Screenshot)
    # ----------------------------------------------------

    analyzer = DevelopmentTopicAnalyzer(repository)

    # Analyze only Licensing for demo
    result = analyzer.analyze_with_pipeline("Licensing")

    topics = result["topics"]
    timelines = result["timelines"]
    states = result["states"]
    evolutions = result["evolutions"]
    contexts = result["contexts"]

    print("\n========== PARSED DEVELOPMENT ACTIVITIES ==========\n")

    activities = analyzer.get_development_activities("Licensing")

    print("\n========== BUSINESS EVOLUTION ==========\n")

    for topic in evolutions:

        print("--------------------------------------")

        print("Topic :", topic["topic"])

        print()

        for item in topic["evolution"]:

            if item["type"] == "Stable":

                print(
                    f"Stable : {item['start_date']}  →  {item['end_date']}"
                )

            else:

                print()

                print(f"Business Change : {item['date']}")

                for change in item["changes"]:

                    print("   •", change)

        print()

        
            
if __name__ == "__main__":

    main()
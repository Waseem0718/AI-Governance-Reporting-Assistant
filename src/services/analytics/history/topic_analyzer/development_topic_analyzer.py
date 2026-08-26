from services.analytics.history.topic_analyzer.text_normalizer import TextNormalizer
from services.analytics.history.topic_analyzer.entity_extractor import EntityExtractor
from services.analytics.history.topic_analyzer.topic_merger import TopicMerger
from services.analytics.history.topic_analyzer.timeline_builder import TimelineBuilder
from services.analytics.history.topic_analyzer.business_state_builder import BusinessStateBuilder
from services.analytics.history.topic_analyzer.development_evolution_builder import DevelopmentEvolutionBuilder
from services.analytics.history.topic_analyzer.ai_context_builder import AIContextBuilder

class DevelopmentTopicAnalyzer:

    def __init__(self, repository):

        self.repository = repository
        
        self.state_builder = BusinessStateBuilder()
        self.timeline_builder = TimelineBuilder(repository)
        self.evolution_builder = DevelopmentEvolutionBuilder()
        self.context_builder = AIContextBuilder()
        

    # -------------------------------------------------------
    # Analyze One Application
    # -------------------------------------------------------

    def analyze(self, application):

        activities = self.repository.development_repository.get_by_application(
            application
        )

        extracted = []

        for row in activities:

            normalized = TextNormalizer.normalize(
                row["activity"]
            )

            entity = EntityExtractor.extract(normalized)

            entity["report_date"] = row["report_date"]
            entity["report_id"] = row["report_id"]
            entity["application"] = row["application"]
            entity["activity"] = row["activity"]
            entity["status"] = row["status"]
            entity["activity_type"] = row["activity_type"]
            entity["environment"] = row["environment"]

            extracted.append(entity)

        merged = TopicMerger.merge(extracted)

        timelines = self.timeline_builder.build(merged)
        states = self.state_builder.build(timelines)
        evolution = self.evolution_builder.build(states)

        contexts = self.context_builder.build(evolution)

        return contexts
    
        # -------------------------------------------------------
    # Analyze All Development Activities
    # -------------------------------------------------------

    def analyze_all(self, month):

        activities = self.repository.development_repository.get_by_month(month)

        extracted = []

        for row in activities:

            normalized = TextNormalizer.normalize(
                row["activity"]
            )

            entity = EntityExtractor.extract(normalized)

            entity["report_id"] = row["report_id"]
            entity["report_date"] = row["report_date"]
            entity["application"] = row["application"]
            entity["activity"] = row["activity"]
            entity["status"] = row["status"]
            entity["activity_type"] = row["activity_type"]
            entity["environment"] = row["environment"]

            extracted.append(entity)

        merged = TopicMerger.merge(extracted)

        timelines = self.timeline_builder.build(merged)

        states = self.state_builder.build(timelines)

        evolutions = self.evolution_builder.build(states)

        contexts = self.context_builder.build(evolutions)

        return contexts
        
    def get_development_activities(self, application):

        activities = self.repository.development_repository.get_by_application(
            application
        )

        return activities
    
    def analyze_with_pipeline(self, application):

        activities = self.repository.development_repository.get_by_application(
            application
        )

        extracted = []

        for row in activities:

            normalized = TextNormalizer.normalize(row["activity"])

            entity = EntityExtractor.extract(normalized)

            entity["report_date"] = row["report_date"]
            entity["report_id"] = row["report_id"]
            entity["application"] = row["application"]
            entity["activity"] = row["activity"]
            entity["status"] = row["status"]
            entity["activity_type"] = row["activity_type"]
            entity["environment"] = row["environment"]

            extracted.append(entity)

        merged = TopicMerger.merge(extracted)

        timelines = self.timeline_builder.build(merged)

        states = self.state_builder.build(timelines)

        evolutions = self.evolution_builder.build(states)

        contexts = self.context_builder.build(evolutions)

        return {
            "topics": merged,
            "timelines": timelines,
            "states": states,
            "evolutions": evolutions,
            "contexts": contexts
        }
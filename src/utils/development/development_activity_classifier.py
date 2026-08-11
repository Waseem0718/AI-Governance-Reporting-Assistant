from utils.development.activity_type_extractor import ActivityTypeExtractor
from utils.development.environment_extractor import EnvironmentExtractor
from utils.development.feature_extractor import FeatureExtractor
from utils.development.status_normalizer import StatusNormalizer


class DevelopmentActivityClassifier:

    @classmethod
    def classify(cls, application, activity, status):

        return {

            "activity_type":
                ActivityTypeExtractor.extract(activity),

            "environment":
                EnvironmentExtractor.extract(
                    application,
                    activity,
                    status
                ),

            "status":
                StatusNormalizer.normalize(status)

        }
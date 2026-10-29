from fusion import FusionEngine
from engagement import classify_engagement
from agent import get_recommendation


fusion = FusionEngine()

# Sample values

attention = 80
movement = 75
activity = 90
audio_score = 70

engagement_score = fusion.calculate_engagement(
    attention,
    movement,
    activity,
    audio_score
)

engagement_level = classify_engagement(
    engagement_score
)

recommendation = get_recommendation(
    engagement_level,
    audio_score
)

print("\n===== ENGAGEMENT ANALYSIS =====")

print(
    f"Engagement Score : {engagement_score}"
)

print(
    f"Engagement Level : {engagement_level}"
)

print(
    f"Recommendation   : {recommendation}"
)

print("===============================")
from audio import AudioModule
from audio_score import get_audio_engagement

audio_module = AudioModule()

result = audio_module.analyze_audio()

engagement = get_audio_engagement(
    result["speech_ratio"]
)

print("\n========== AUDIO ANALYSIS ==========")
print(f"Volume           : {result['volume']}")
print(f"Speech Detected  : {result['speech_detected']}")
print(f"Speech Ratio     : {result['speech_ratio']}%")
print(f"Noise Level      : {result['noise_level']}%")
print(f"Engagement Level : {engagement}")
print("====================================")
import sounddevice as sd
import numpy as np


class AudioModule:

    def __init__(self,
                 duration=5,
                 sample_rate=44100):

        self.duration = duration
        self.sample_rate = sample_rate

    def record_audio(self):

        print("Recording Audio...")

        audio = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='float64'
        )

        sd.wait()

        print("Recording Complete")

        return audio.flatten()

    def analyze_audio(self):

        audio = self.record_audio()

        threshold = 0.02

        speech_frames = np.sum(np.abs(audio) > threshold)

        total_frames = len(audio)

        speech_ratio = (
            speech_frames / total_frames
        ) * 100

        noise_level = np.mean(
            np.abs(audio)
        ) * 100

        return {
            "speech_ratio": round(speech_ratio, 2),
            "noise_level": round(noise_level, 2)
        }
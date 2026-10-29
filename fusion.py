class FusionEngine:

    def calculate_engagement(
        self,
        attention,
        movement,
        activity,
        audio_score
    ):

        visual_score = (
            0.5 * attention +
            0.2 * movement +
            0.3 * activity
        )

        final_score = (
            0.8 * visual_score +
            0.2 * audio_score
        )

        return round(final_score, 2)
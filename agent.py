def get_recommendation(
    engagement_level,
    speech_ratio
):

    if engagement_level == "Low":

        return (
            "Low engagement detected. "
            "Start a Q&A session or interactive poll."
        )

    elif engagement_level == "Medium":

        return (
            "Moderate engagement. "
            "Encourage more classroom participation."
        )

    elif speech_ratio < 20:

        return (
            "Audio participation is low. "
            "Try group discussion activities."
        )

    else:

        return (
            "High engagement detected. "
            "Continue current teaching pace."
        )

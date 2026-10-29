def generate_report(
    engagement_score,
    engagement_level,
    recommendation
):

    report = f"""
    ============================
    CLASSROOM SESSION REPORT
    ============================

    Engagement Score : {engagement_score}

    Engagement Level : {engagement_level}

    Recommendation :

    {recommendation}

    ============================
    """

    return report
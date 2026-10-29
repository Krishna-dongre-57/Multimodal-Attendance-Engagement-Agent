def classify_engagement(score):

    if score < 40:
        return "Low"

    elif score < 70:
        return "Medium"

    else:
        return "High"
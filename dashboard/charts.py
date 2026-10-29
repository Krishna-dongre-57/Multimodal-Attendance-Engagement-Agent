import pandas as pd
import plotly.express as px


def attendance_chart(present_count, remaining_count):
    data = {
        "Status": ["Detected", "Not yet detected"],
        "Count": [present_count, remaining_count]
    }

    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        values="Count",
        names="Status",
        hole=0.62,
        color="Status",
        color_discrete_map={
            "Detected": "#087F73",
            "Not yet detected": "#DCE5E2"
        }
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=True,
        margin=dict(t=16, r=12, b=16, l=12),
        legend=dict(orientation="h", y=-0.08)
    )

    return fig


def engagement_chart(history):
    df = pd.DataFrame(history)

    fig = px.line(
        df,
        x="timestamp",
        y="score",
        markers=True,
        labels={
            "timestamp": "Session time",
            "score": "Engagement score"
        }
    )

    fig.update_layout(
        template="plotly_white",
        yaxis=dict(range=[0, 100]),
        margin=dict(t=16, r=12, b=16, l=12),
        showlegend=False
    )

    return fig
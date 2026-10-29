import pandas as pd
import plotly.express as px


def attendance_chart():

    data = {
        "Status": ["Present", "Absent"],
        "Count": [25, 5]
    }

    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        values="Count",
        names="Status",
        title="Attendance Distribution"
    )

    return fig
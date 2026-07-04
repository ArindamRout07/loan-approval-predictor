"""
plot_utils.py
-------------
Plotly chart builders: feature importance bar chart and the
approval/rejection probability donut gauge.
"""

import pandas as pd
import plotly.graph_objects as go

FEATURE_IMPORTANCE = {
    "Credit_History": 0.253852,
    "TotalIncome": 0.134921,
    "Income_Loan_Ratio": 0.132879,
    "LoanAmount": 0.116666,
    "ApplicantIncome": 0.110472,
    "CoapplicantIncome": 0.071379,
    "Loan_Amount_Term": 0.039353,
    "Property_Area_Semiurban": 0.024557,
    "Married_Yes": 0.019613,
    "Education_Not Graduate": 0.018342,
}

BRAND_GRADIENT = ["#6C5CE7", "#7D6FF0", "#8E82F4", "#A095F7", "#B2A8FA",
                  "#C4BBFC", "#D6CEFF", "#E3DEFF", "#EFEAFF", "#F6F3FF"]


def render_feature_importance_chart():
    """Return a horizontal Plotly bar chart of the top-10 feature importances."""
    df = (
        pd.DataFrame(
            {"feature": list(FEATURE_IMPORTANCE.keys()),
             "importance": list(FEATURE_IMPORTANCE.values())}
        )
        .sort_values("importance", ascending=True)
    )

    fig = go.Figure(
        go.Bar(
            x=df["importance"],
            y=df["feature"],
            orientation="h",
            marker=dict(
                color=df["importance"],
                colorscale="Purples",
                line=dict(color="rgba(255,255,255,0.4)", width=1),
            ),
            text=[f"{v:.1%}" for v in df["importance"]],
            textposition="outside",
            hovertemplate="%{y}: %{x:.2%}<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", size=13, color="#EDEDF7"),
        margin=dict(l=10, r=30, t=20, b=10),
        height=420,
        xaxis=dict(title="Importance", tickformat=".0%", showgrid=False),
        yaxis=dict(title=""),
    )
    return fig


def render_probability_donut(approval_prob: float, rejection_prob: float):
    """Return a donut chart comparing approval vs rejection probability."""
    fig = go.Figure(
        go.Pie(
            labels=["Approval", "Rejection"],
            values=[approval_prob, rejection_prob],
            hole=0.68,
            marker=dict(colors=["#00C896", "#FF5C5C"]),
            textinfo="none",
            sort=False,
            direction="clockwise",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, x=0.22),
        margin=dict(l=0, r=0, t=10, b=0),
        height=260,
        annotations=[
            dict(
                text=f"<b>{approval_prob:.0%}</b><br><span style='font-size:12px'>Approval</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=26, color="#EDEDF7", family="Poppins, sans-serif"),
            )
        ],
    )
    return fig

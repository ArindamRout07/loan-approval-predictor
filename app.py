"""
app.py
------
Loan Approval Predictor — a premium, SaaS-style Streamlit application.

Run with:
    streamlit run app.py
"""

import streamlit as st

from modules.model_utils import build_feature_row, load_artifacts, predict_loan_approval
from modules.plot_utils import render_feature_importance_chart, render_probability_donut
from modules.report_utils import generate_report_csv
from modules.ui_components import (
    load_css,
    render_footer,
    render_hero,
    render_model_info,
    render_probability_bars,
    render_project_highlights,
    render_result_card,
    render_risk_meter,
    render_sidebar_inputs,
    render_summary_cards,
)


def configure_page():
    st.set_page_config(
        page_title="Loan Approval Predictor",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_prediction_section(model, model_columns, inputs):
    """Build features, predict, and render every result section."""
    feature_df, total_income, income_loan_ratio = build_feature_row(inputs, model_columns)

    try:
        approved, approval_prob, rejection_prob = predict_loan_approval(model, feature_df)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Something went wrong while generating the prediction: {exc}")
        return

    render_result_card(approved)

    col_left, col_right = st.columns([1.1, 1])
    with col_left:
        st.markdown('<div class="section-header">Prediction confidence</div>', unsafe_allow_html=True)
        st.plotly_chart(
            render_probability_donut(approval_prob, rejection_prob),
            use_container_width=True,
        )
        render_probability_bars(approval_prob, rejection_prob)

    with col_right:
        st.markdown('<div class="section-header">Risk meter</div>', unsafe_allow_html=True)
        render_risk_meter(approval_prob)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Download report</div>', unsafe_allow_html=True)
        report_bytes = generate_report_csv(
            inputs, approved, approval_prob, rejection_prob, total_income, income_loan_ratio
        )
        st.download_button(
            label="Download prediction report",
            data=report_bytes,
            file_name="loan_prediction_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown('<div class="section-header">Applicant summary</div>', unsafe_allow_html=True)
    render_summary_cards(inputs, total_income, income_loan_ratio)

    st.markdown('<div class="section-header">Top feature importances</div>', unsafe_allow_html=True)
    st.plotly_chart(render_feature_importance_chart(), use_container_width=True)


def main():
    configure_page()
    load_css()

    render_hero()

    inputs, predict_clicked = render_sidebar_inputs()

    model, model_columns, error_message = load_artifacts()

    if error_message:
        st.error(error_message)
        st.info(
            "Once the trained model files are placed inside the `artifacts/` "
            "folder, this app will work immediately without any code changes."
        )
    elif predict_clicked:
        if inputs["loan_amount"] <= 0:
            st.warning("Loan amount must be greater than 0 to generate a prediction.")
        else:
            render_prediction_section(model, model_columns, inputs)
    else:
        st.info("Fill in the applicant details in the sidebar and click **Predict Loan Approval** to get started.")

    st.markdown('<div class="section-header">Model & project details</div>', unsafe_allow_html=True)
    render_model_info()
    render_project_highlights()

    render_footer()


if __name__ == "__main__":
    main()

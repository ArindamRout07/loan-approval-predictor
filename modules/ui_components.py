"""
ui_components.py
-----------------
Reusable, presentation-only Streamlit UI pieces: CSS loader, sidebar
inputs, hero section, result card, risk meter, summary cards, model
info panel, project highlights, and footer.
"""

import os

import streamlit as st

CSS_PATH = os.path.join("style", "custom.css")


def load_css():
    """Inject the custom stylesheet into the Streamlit app."""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_hero():
    """Top hero / header section for the main page."""
    st.markdown(
        """
        <div class="hero fade-in">
            <h1 class="hero-title">Loan Approval Predictor</h1>
            <p class="hero-subtitle">
                A modern decision assistant that estimates loan approval outcomes in real time.
            </p>
            <p class="hero-description">
                Complete the applicant details in the sidebar and click <strong>Predict Loan Approval</strong> to review the decision, confidence, and model insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_inputs() -> dict:
    """Render all sidebar input widgets and return the collected values."""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Applicant details</div>', unsafe_allow_html=True)

        st.markdown("##### Income")
        applicant_income = st.number_input(
            "Applicant Income (monthly)", min_value=0, value=5000, step=500
        )
        coapplicant_income = st.number_input(
            "Coapplicant Income (monthly)", min_value=0, value=0, step=500
        )

        st.markdown("##### Loan details")
        loan_amount = st.number_input(
            "Loan Amount (in thousands)", min_value=1, value=150, step=10
        )
        loan_term = st.selectbox(
            "Loan Term (days)",
            options=[360, 180, 120, 84, 60, 36, 12],
            index=0,
        )
        credit_history = st.selectbox(
            "Credit History",
            options=["Good (1)", "Bad (0)"],
        )
        credit_history_value = 1 if credit_history.startswith("Good") else 0

        st.markdown("##### Personal info")
        gender = st.radio("Gender", options=["Male", "Female"], horizontal=True)
        married = st.radio("Married", options=["Yes", "No"], horizontal=True)
        dependents = st.selectbox("Dependents", options=["0", "1", "2", "3+"])
        education = st.radio(
            "Education", options=["Graduate", "Not Graduate"], horizontal=True
        )
        self_employed = st.radio(
            "Self Employed", options=["No", "Yes"], horizontal=True
        )
        property_area = st.selectbox(
            "Property Area", options=["Urban", "Semiurban", "Rural"]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        predict_clicked = st.button("Predict Loan Approval", use_container_width=True)

    return {
        "applicant_income": applicant_income,
        "coapplicant_income": coapplicant_income,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "credit_history": credit_history_value,
        "gender": gender,
        "married": married,
        "dependents": dependents,
        "education": education,
        "self_employed": self_employed,
        "property_area": property_area,
    }, predict_clicked


def render_result_card(approved: bool):
    """Big approve/reject result card."""
    if approved:
        st.markdown(
            """
            <div class="result-card result-approved">
                <div class="result-title">Loan approved</div>
                <div class="result-subtitle">The applicant meets the model's approval criteria.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="result-card result-rejected">
                <div class="result-title">Loan rejected</div>
                <div class="result-subtitle">The applicant does not meet the model's approval criteria.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_probability_bars(approval_prob: float, rejection_prob: float):
    """Two labeled progress bars for approval / rejection probability."""
    st.markdown("**Approval Probability**")
    st.progress(min(max(approval_prob, 0.0), 1.0), text=f"{approval_prob:.1%}")
    st.markdown("**Rejection Probability**")
    st.progress(min(max(rejection_prob, 0.0), 1.0), text=f"{rejection_prob:.1%}")


def render_risk_meter(approval_prob: float):
    """Risk meter based on approval probability."""
    if approval_prob >= 0.70:
        label, css_class = "Low risk", "risk-low"
    elif approval_prob >= 0.40:
        label, css_class = "Medium risk", "risk-medium"
    else:
        label, css_class = "High risk", "risk-high"

    st.markdown(
        f"""
        <div class="risk-meter {css_class}">
            <span class="risk-label">{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_cards(inputs: dict, total_income: float, income_loan_ratio: float):
    """Row of metric cards summarizing the key figures."""
    cards = [
        ("Total income", f"{total_income:,.0f}"),
        ("Income / loan ratio", f"{income_loan_ratio:.2f}"),
        ("Credit history", "Good" if inputs["credit_history"] == 1 else "Bad"),
        ("Property area", inputs["property_area"]),
        ("Loan amount", f"{inputs['loan_amount']:,.0f}K"),
    ]

    cols = st.columns(len(cards))
    for col, (label, value) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card fade-in">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_model_info():
    """Expandable panel with model performance details."""
    with st.expander("Model information", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
                - **Algorithm:** Random Forest Classifier
                - **Accuracy:** 80.49%
                - **Precision:** 79%
                """
            )
        with col2:
            st.markdown(
                """
                - **Recall:** 95%
                - **F1 Score:** 86%
                - **Dataset:** 614 samples, 16 engineered features
                """
            )


def render_project_highlights():
    """Expandable section describing the project's technical highlights."""
    with st.expander("Project highlights", expanded=False):
        st.markdown(
            """
            - **Feature engineering** — derived `TotalIncome` and `Income_Loan_Ratio`
            - **Random Forest** classifier trained on cleaned applicant data
            - **Hyperparameter tuning** for better accuracy and recall balance
            - **Feature importance** analysis to explain model decisions
            - **Exploratory data analysis (EDA)** to understand approval patterns
            - **Binary classification** — approved vs rejected outcome
            """
        )


def render_footer():
    """Footer with project attribution and links."""
    st.markdown(
        """
        <div class="footer fade-in">
            <p>Built by <b>Arindam Rout</b></p>
            <div class="footer-links">
                <a href="https://github.com/" target="_blank">GitHub</a>
                <a href="https://www.linkedin.com/" target="_blank">LinkedIn</a>
                <a href="mailto:arindam@example.com">Email</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

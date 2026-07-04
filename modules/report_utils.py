"""
report_utils.py
----------------
Builds a downloadable CSV report summarizing a single prediction run.
"""

from datetime import datetime
import io

import pandas as pd


def generate_report_csv(
    inputs: dict,
    approved: bool,
    approval_prob: float,
    rejection_prob: float,
    total_income: float,
    income_loan_ratio: float,
) -> bytes:
    """Build a one-row CSV report (as bytes) for the user to download."""
    record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Prediction": "Approved" if approved else "Rejected",
        "Approval Probability (%)": round(approval_prob * 100, 2),
        "Rejection Probability (%)": round(rejection_prob * 100, 2),
        "Applicant Income": inputs["applicant_income"],
        "Coapplicant Income": inputs["coapplicant_income"],
        "Total Income": round(total_income, 2),
        "Loan Amount": inputs["loan_amount"],
        "Loan Amount Term": inputs["loan_term"],
        "Income to Loan Ratio": round(income_loan_ratio, 4),
        "Credit History": inputs["credit_history"],
        "Gender": inputs["gender"],
        "Married": inputs["married"],
        "Dependents": inputs["dependents"],
        "Education": inputs["education"],
        "Self Employed": inputs["self_employed"],
        "Property Area": inputs["property_area"],
    }

    df = pd.DataFrame([record])
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")

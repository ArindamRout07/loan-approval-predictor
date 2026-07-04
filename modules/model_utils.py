"""
model_utils.py
--------------
Handles loading the trained model + column artifacts, building the
engineered feature row from raw user inputs, and running predictions.
"""

import os
import pickle

import joblib
import pandas as pd
import streamlit as st

ARTIFACTS_DIR = "artifacts"
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "loan_approval_model.pkl")
COLUMNS_PATH = os.path.join(ARTIFACTS_DIR, "model_columns.pkl")


def _load_pickle_any(path):
    """Try joblib first (common for sklearn models), fall back to pickle."""
    try:
        return joblib.load(path)
    except Exception:
        with open(path, "rb") as f:
            return pickle.load(f)


@st.cache_resource(show_spinner=False)
def load_artifacts():
    """
    Load the trained model and expected column order.

    Returns
    -------
    (model, columns, error_message)
        error_message is None on success, otherwise a human readable string.
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(COLUMNS_PATH):
        return None, None, (
            f"Model artifacts not found.\n\n"
            f"Expected files:\n- `{MODEL_PATH}`\n- `{COLUMNS_PATH}`\n\n"
            f"Please make sure both files exist before running the app."
        )

    try:
        model = _load_pickle_any(MODEL_PATH)
        columns = list(_load_pickle_any(COLUMNS_PATH))
        return model, columns, None
    except Exception as exc:  # noqa: BLE001
        return None, None, f"Failed to load model artifacts: {exc}"


def build_feature_row(inputs: dict, model_columns: list):
    """
    Convert raw sidebar inputs into a single-row DataFrame that exactly
    matches the model's expected column order. TotalIncome and
    Income_Loan_Ratio are engineered automatically here.

    Returns
    -------
    (feature_df, total_income, income_loan_ratio)
    """
    applicant_income = float(inputs["applicant_income"])
    coapplicant_income = float(inputs["coapplicant_income"])
    loan_amount = float(inputs["loan_amount"])
    loan_term = float(inputs["loan_term"])
    credit_history = float(inputs["credit_history"])

    total_income = applicant_income + coapplicant_income
    safe_loan_amount = loan_amount if loan_amount > 0 else 1e-6
    income_loan_ratio = total_income / safe_loan_amount

    dependents = inputs["dependents"]
    property_area = inputs["property_area"]

    row = {
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "TotalIncome": total_income,
        "Income_Loan_Ratio": income_loan_ratio,
        "Gender_Male": 1 if inputs["gender"] == "Male" else 0,
        "Married_Yes": 1 if inputs["married"] == "Yes" else 0,
        "Dependents_1": 1 if dependents == "1" else 0,
        "Dependents_2": 1 if dependents == "2" else 0,
        "Dependents_3+": 1 if dependents == "3+" else 0,
        "Education_Not Graduate": 1 if inputs["education"] == "Not Graduate" else 0,
        "Self_Employed_Yes": 1 if inputs["self_employed"] == "Yes" else 0,
        "Property_Area_Semiurban": 1 if property_area == "Semiurban" else 0,
        "Property_Area_Urban": 1 if property_area == "Urban" else 0,
    }

    feature_df = pd.DataFrame([row])
    feature_df = feature_df.reindex(columns=model_columns, fill_value=0)
    return feature_df, total_income, income_loan_ratio


def predict_loan_approval(model, feature_df: pd.DataFrame):
    """
    Run the model on a single-row feature DataFrame.

    Returns
    -------
    (approved: bool, approval_prob: float, rejection_prob: float)
    """
    prediction = model.predict(feature_df)[0]

    approval_prob = None
    rejection_prob = None

    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(feature_df)[0]
            classes = list(model.classes_)

            if 1 in classes:
                approval_idx = classes.index(1)
            elif "Y" in classes:
                approval_idx = classes.index("Y")
            elif True in classes:
                approval_idx = classes.index(True)
            else:
                approval_idx = int(len(classes) - 1)

            approval_prob = float(proba[approval_idx])
            rejection_prob = float(1 - approval_prob)
        except Exception:
            approval_prob = None

    approved = prediction in (1, "Y", True)

    if approval_prob is None:
        approval_prob = 1.0 if approved else 0.0
        rejection_prob = 1.0 - approval_prob

    return approved, approval_prob, rejection_prob

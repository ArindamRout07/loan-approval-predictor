# 🏦 Loan Approval Predictor

An end-to-end Machine Learning application that predicts whether a loan application is likely to be **Approved** or **Rejected** based on an applicant's financial and demographic information.

Built using **Python, Scikit-learn, Random Forest, Streamlit**, and deployed as an interactive web application.

---

## 📌 Project Overview

Financial institutions process thousands of loan applications every day. Evaluating every application manually is time-consuming and susceptible to inconsistencies.

This project leverages Machine Learning to automate the loan approval prediction process by analyzing applicant information such as income, loan amount, credit history, employment status, education, and property area.

The application predicts loan approval in real time and provides an intuitive dashboard for users.

---

## 🚀 Features

- 📊 Interactive Streamlit Dashboard
- 🤖 Random Forest Classification Model
- 📈 Prediction Probability
- 📋 Applicant Summary
- 🎨 Modern Responsive UI
- 📊 Feature Importance Visualization
- 📄 Downloadable Prediction Report
- ⚡ Real-Time Predictions
- 💻 Fully Deployable Web Application

---

## 📂 Project Structure

```
loan-approval-predictor/
│
├── artifacts/
│   ├── loan_approval_model.pkl
│   ├── model_columns.pkl
│   └── scaler.pkl
│
├── data/
│   ├── train.csv
│   └── test.csv
│
├── modules/
│   ├── model_utils.py
│   ├── plot_utils.py
│   ├── report_utils.py
│   ├── ui_components.py
│   └── __init__.py
│
├── notebooks/
│   └── EDA.ipynb
│
├── style/
│   └── custom.css
│
├── screenshots/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 Dataset

- **Source:** Kaggle Loan Prediction Dataset
- **Rows:** 614
- **Features:** 13 Original Features
- **Target Variable:** Loan_Status

---

# 🔍 Exploratory Data Analysis

The following analyses were performed:

- Missing Value Analysis
- Class Distribution
- Univariate Analysis
- Bivariate Analysis
- Correlation Analysis
- Feature Engineering
- Outlier Inspection

---

# 🧠 Feature Engineering

To improve model performance, additional features were created.

### ✅ Total Income

```
TotalIncome = ApplicantIncome + CoapplicantIncome
```

---

### ✅ Income Loan Ratio

```
Income_Loan_Ratio = TotalIncome / LoanAmount
```

These engineered features significantly improved model performance by capturing an applicant's repayment capacity more effectively.

---

# ⚙️ Data Preprocessing

- Missing Value Imputation
- Median Imputation
- Mode Imputation
- One-Hot Encoding
- Feature Scaling (for KNN)
- Train-Test Split

---

# 🤖 Models Evaluated

The following classification algorithms were compared:

| Model | Accuracy |
|--------|----------|
| Logistic Regression | 78.86% |
| Decision Tree | 66.67% |
| K-Nearest Neighbors | 75.61% |
| **Random Forest** | **80.49%** ✅ |

Random Forest achieved the highest overall performance and was selected as the final model.

---

# 📈 Final Model Performance

**Algorithm**

```
Random Forest Classifier
```

### Accuracy

```
80.49%
```

### Precision

```
79%
```

### Recall

```
95%
```

### F1 Score

```
86%
```

---

# 📊 Top Feature Importance

| Feature | Importance |
|----------|-----------:|
| Credit History | 0.254 |
| Total Income | 0.135 |
| Income Loan Ratio | 0.133 |
| Loan Amount | 0.117 |
| Applicant Income | 0.110 |
| Coapplicant Income | 0.071 |
| Loan Amount Term | 0.039 |
| Property Area (Semiurban) | 0.025 |
| Married | 0.020 |
| Education | 0.018 |

The analysis shows that **Credit History** is the single most influential factor affecting loan approval.

---

# 💻 Streamlit Application

The application allows users to:

- Enter applicant information
- Predict loan approval instantly
- View prediction confidence
- View feature importance
- Download prediction reports

---

# 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Plotly
- Matplotlib
- Joblib

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/loan-approval-predictor.git
```

Move into the project

```bash
cd loan-approval-predictor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 📷 Application Preview

> Add screenshots of the Streamlit application here.

```
screenshots/
```

---

# 🎯 Future Improvements

- SHAP Explainability
- XGBoost Classifier
- LightGBM
- Hyperparameter Optimization
- Model Monitoring
- Docker Deployment
- CI/CD Pipeline

---

# 📚 Key Learnings

During this project I learned:

- End-to-End Machine Learning Workflow
- Feature Engineering
- Classification Algorithms
- Model Evaluation
- Hyperparameter Tuning
- Feature Importance Analysis
- Streamlit Application Development
- Machine Learning Deployment

---

# 👨‍💻 Author

**Arindam Rout**

B.Tech CSE (Artificial Intelligence & Machine Learning)

---

## ⭐ If you found this project useful, consider giving it a star!
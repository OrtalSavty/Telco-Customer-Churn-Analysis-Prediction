# Telco Customer Churn — Analysis & Prediction

## Overview

This project analyzes telecom customer data to identify churn drivers and predict at-risk customers using machine learning.  
The goal is to give retention teams actionable insights early enough to intervene and improve customer LTV (Life Time Value).

---

## Dataset

**File:** `Customer_Data.csv` — 7,043 rows, 21 columns.

| Column | Description |
|---|---|
| `customerID` | Unique customer identifier |
| `tenure` | Months the customer has been with the company |
| `MonthlyCharges` | Current monthly charge |
| `TotalCharges` | Total amount charged |
| `Contract` | Contract type (Month-to-month / One year / Two year) |
| `InternetService` | Internet service type (DSL / Fiber optic / No) |
| `Churn` | Whether the customer left (Yes / No) |

---

## Architecture

```
CSV → Python (pandas) → SQL Server (ChurnDB) → Cleaned View → Python → ML Models
```

- **Database:** SQL Server, managed via SSMS
- **Logic layer:** Python 3.x
- **Key libraries:** `pandas`, `sqlalchemy`, `scikit-learn`, `matplotlib`, `seaborn`

---

## Project Structure

| File | Description |
|---|---|
| `load_data.py` | Reads the CSV and loads it into a SQL Server staging table |
| `eda_analysis.py` | Exploratory Data Analysis with visualizations |
| `model_training.py` | Model training, evaluation, and comparison |

---

## Pipeline

### 1. Data Loading (`load_data.py`)
Reads `Customer_Data.csv` and pushes it to the `raw_data_staging` table in SQL Server.

### 2. Data Cleaning (SQL)
Raw data is cleaned and transformed inside SQL Server, exposed as a view called `v_clean_data`.

### 3. Exploratory Analysis (`eda_analysis.py`)
Generates the following charts:
- Pie chart — churn vs. retained customers
- Histogram — monthly charges by churn group
- Bar chart — churn rate by contract type
- KDE plot — customer tenure distribution by churn
- Bar chart — churn rate by internet service type

### 4. Model Training (`model_training.py`)
Two models are trained and compared:

| Model | Notes |
|---|---|
| **Logistic Regression** | Linear, interpretable, good baseline |
| **Random Forest** | Ensemble model, stronger on complex patterns |

Evaluation metrics: Accuracy, Recall, Confusion Matrix, ROC-AUC curve.

---

## Usage

```bash
# Step 1 — Load data into SQL Server
python load_data.py

# Step 2 — Run exploratory analysis
python eda_analysis.py

# Step 3 — Train and evaluate models
python model_training.py
```

> **Prerequisites:** A local SQL Server instance with a database named `ChurnDB` and ODBC Driver 17 installed.

---

## Installation

```bash
pip install pandas sqlalchemy pyodbc scikit-learn matplotlib seaborn
```

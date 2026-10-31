"""
SaiKet Systems - Business Analysis Internship
Project : Customer Segmentation Visualization & Advanced Analysis
Task 1  : Data Overview and Simple Sorting

Steps covered
  1. Open the dataset and explore its structure
  2. Sort the data by tenure (shortest and longest tenures)
  3. Filter the data to show only customers who have churned

Outputs (saved in ./output):
  task1_sorted_by_tenure.xlsx   - full data sorted by tenure (ascending)
  task1_churned_customers.xlsx  - only the churned customers
"""

import os
import pandas as pd

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "Telco_Customer_Churn_Dataset.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ----------------------------------------------------------------------------
# 1. Load and explore the dataset structure
# ----------------------------------------------------------------------------
df = pd.read_csv(DATA_FILE)

section("1. DATASET STRUCTURE")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

section("First 5 rows")
print(df.head())

section("Column names and data types")
print(df.dtypes)

# TotalCharges is stored as text because 11 rows contain blank spaces
# (these are customers with tenure = 0). Convert it to numeric.
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

section("Missing values per column (after converting TotalCharges to numeric)")
print(df.isnull().sum())

section("Statistical summary of numeric columns")
print(df.describe())

section("Churn distribution")
print(df["Churn"].value_counts())
print((df["Churn"].value_counts(normalize=True) * 100).round(2).astype(str) + " %")

# ----------------------------------------------------------------------------
# 2. Sort by tenure
# ----------------------------------------------------------------------------
df_sorted = df.sort_values(by="tenure", ascending=True).reset_index(drop=True)

section("2. SORTED BY TENURE - 10 SHORTEST TENURES")
print(df_sorted[["customerID", "tenure", "MonthlyCharges", "Churn"]].head(10))

section("2. SORTED BY TENURE - 10 LONGEST TENURES")
print(df_sorted[["customerID", "tenure", "MonthlyCharges", "Churn"]].tail(10))

# ----------------------------------------------------------------------------
# 3. Filter churned customers only
# ----------------------------------------------------------------------------
df_churned = df[df["Churn"] == "Yes"].sort_values("tenure").reset_index(drop=True)

section("3. CHURNED CUSTOMERS ONLY")
print(f"Total churned customers: {len(df_churned)}")
print(df_churned[["customerID", "tenure", "MonthlyCharges", "Contract", "Churn"]].head(10))
print(f"\nAverage tenure of churned customers : {df_churned['tenure'].mean():.1f} months")
print(f"Average tenure of retained customers: {df[df['Churn'] == 'No']['tenure'].mean():.1f} months")

# ----------------------------------------------------------------------------
# Save results
# ----------------------------------------------------------------------------
sorted_path = os.path.join(OUTPUT_DIR, "task1_sorted_by_tenure.xlsx")
churned_path = os.path.join(OUTPUT_DIR, "task1_churned_customers.xlsx")

df_sorted.to_excel(sorted_path, index=False)
df_churned.to_excel(churned_path, index=False)

section("FILES SAVED")
print(sorted_path)
print(churned_path)

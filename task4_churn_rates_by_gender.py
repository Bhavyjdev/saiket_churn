"""
SaiKet Systems - Business Analysis Internship
Project : Customer Segmentation Visualization & Advanced Analysis
Task 4  : Churn Rates by Gender

Steps covered
  1. Pivot table with churn counts for each gender
  2. Clustered bar chart of churned and non-churned counts per gender
  3. Distinct colours for churned and non-churned categories

Outputs (saved in ./output):
  task4_gender_churn_pivot.xlsx
  task4_churn_by_gender_chart.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "Telco_Customer_Churn_Dataset.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------------
df = pd.read_csv(DATA_FILE)

# ----------------------------------------------------------------------------
# 1. Pivot table: churn counts for each gender
# ----------------------------------------------------------------------------
pivot = pd.pivot_table(df, index="gender", columns="Churn",
                       values="customerID", aggfunc="count", margins=True,
                       margins_name="Total")

print("Pivot table (customer counts):")
print(pivot)

# Churn rate per gender
pivot_core = pivot.drop(index="Total")
churn_rate = (pivot_core["Yes"] / pivot_core["Total"] * 100).round(2)
print("\nChurn rate by gender (%):")
print(churn_rate.to_string())

# ----------------------------------------------------------------------------
# 2. Clustered bar chart (churned vs non-churned for each gender)
# ----------------------------------------------------------------------------
plot_data = pivot_core[["No", "Yes"]]

ax = plot_data.plot(kind="bar", figsize=(9, 6), width=0.7,
                    color={"No": "#4C9F70", "Yes": "#E4572E"},
                    edgecolor="black")

# Labels with exact counts on every bar
for container in ax.containers:
    ax.bar_label(container, fmt="%d", padding=3, fontsize=11, fontweight="bold")

ax.set_title("Churned vs. Non-Churned Customers by Gender",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Gender", fontsize=12)
ax.set_ylabel("Number of Customers", fontsize=12)
ax.set_xticklabels(plot_data.index, rotation=0)
ax.set_ylim(0, plot_data.values.max() * 1.15)
ax.legend(["Not Churned (No)", "Churned (Yes)"], title="Churn Status")
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()
chart_path = os.path.join(OUTPUT_DIR, "task4_churn_by_gender_chart.png")
plt.savefig(chart_path, dpi=200)
print(f"\nChart saved to: {chart_path}")

# ----------------------------------------------------------------------------
# Save the pivot table (with churn rate) to Excel
# ----------------------------------------------------------------------------
pivot_out = pivot.copy()
pivot_out["Churn Rate (%)"] = (pivot_out["Yes"] / pivot_out["Total"] * 100).round(2)
pivot_path = os.path.join(OUTPUT_DIR, "task4_gender_churn_pivot.xlsx")
pivot_out.to_excel(pivot_path)
print(f"Pivot table saved to: {pivot_path}")

plt.show()

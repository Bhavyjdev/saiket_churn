"""
SaiKet Systems - Business Analysis Internship
Project : Customer Segmentation Visualization & Advanced Analysis
Task 5  : Heatmap for Monthly Charges and Tenure Interaction

Visualises how MonthlyCharges and Tenure interact with churn behaviour.
  - Data cleaning: TotalCharges blanks converted to numeric (not used here, but
    checked), Churn encoded as 1/0.
  - Tenure and MonthlyCharges are grouped into bands (bins).
  - Left heatmap : number of customers in each band combination
  - Right heatmap: churn rate (%) in each band combination

Outputs (saved in ./output):
  task5_tenure_charges_heatmap.png
  task5_churn_rate_matrix.xlsx
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "Telco_Customer_Churn_Dataset.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# Load and clean data
# ----------------------------------------------------------------------------
df = pd.read_csv(DATA_FILE)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
print("Missing values after cleaning:")
print(df[["tenure", "MonthlyCharges", "TotalCharges", "Churn"]].isnull().sum())

df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

# ----------------------------------------------------------------------------
# Create bands for tenure (months) and monthly charges ($)
# ----------------------------------------------------------------------------
tenure_bins = [-1, 12, 24, 36, 48, 60, 72]
tenure_labels = ["0-12", "13-24", "25-36", "37-48", "49-60", "61-72"]
df["TenureBand"] = pd.cut(df["tenure"], bins=tenure_bins, labels=tenure_labels)

charge_bins = [0, 30, 50, 70, 90, 110, 130]
charge_labels = ["$0-30", "$30-50", "$50-70", "$70-90", "$90-110", "$110+"]
df["ChargeBand"] = pd.cut(df["MonthlyCharges"], bins=charge_bins, labels=charge_labels)

# ----------------------------------------------------------------------------
# Matrices: churn rate (%) and customer count
# ----------------------------------------------------------------------------
churn_rate = (df.pivot_table(index="ChargeBand", columns="TenureBand",
                             values="ChurnFlag", aggfunc="mean", observed=False) * 100).round(1)
customer_count = df.pivot_table(index="ChargeBand", columns="TenureBand",
                                values="ChurnFlag", aggfunc="count", observed=False)

# Put the highest charge band at the top of the heatmap
churn_rate = churn_rate.sort_index(ascending=False)
customer_count = customer_count.sort_index(ascending=False)

print("\nChurn rate (%) by monthly-charge band (rows) and tenure band (columns):")
print(churn_rate)
print("\nNumber of customers in each cell:")
print(customer_count)

# ----------------------------------------------------------------------------
# Heatmaps
# ----------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(17, 7))

sns.heatmap(customer_count, annot=True, fmt=".0f", cmap="Blues",
            linewidths=0.5, linecolor="white", cbar_kws={"label": "Customers"},
            ax=axes[0])
axes[0].set_title("Number of Customers\n(Monthly Charges vs. Tenure)",
                  fontsize=13, fontweight="bold")

sns.heatmap(churn_rate, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=70,
            linewidths=0.5, linecolor="white", cbar_kws={"label": "Churn Rate (%)"},
            ax=axes[1])
axes[1].set_title("Churn Rate (%)\n(Monthly Charges vs. Tenure)",
                  fontsize=13, fontweight="bold")

for ax in axes:
    ax.set_xlabel("Tenure (months)", fontsize=11)
    ax.set_ylabel("Monthly Charges", fontsize=11)
    ax.tick_params(axis="y", rotation=0)

fig.suptitle("Interaction of Monthly Charges, Tenure and Churn Behaviour",
             fontsize=16, fontweight="bold")
plt.tight_layout()

chart_path = os.path.join(OUTPUT_DIR, "task5_tenure_charges_heatmap.png")
plt.savefig(chart_path, dpi=200)
print(f"\nHeatmap saved to: {chart_path}")

# ----------------------------------------------------------------------------
# Save the matrices to Excel
# ----------------------------------------------------------------------------
excel_path = os.path.join(OUTPUT_DIR, "task5_churn_rate_matrix.xlsx")
with pd.ExcelWriter(excel_path) as writer:
    churn_rate.to_excel(writer, sheet_name="Churn Rate (%)")
    customer_count.to_excel(writer, sheet_name="Customer Count")
print(f"Matrices saved to: {excel_path}")

# ----------------------------------------------------------------------------
# Quick interpretation
# ----------------------------------------------------------------------------
stacked = churn_rate.stack()
print(f"\nHighest churn cell: {stacked.idxmax()} -> {stacked.max():.1f} %")
print(f"Lowest churn cell : {stacked.idxmin()} -> {stacked.min():.1f} %")

plt.show()

"""
SaiKet Systems - Business Analysis Internship
Project : Customer Segmentation Visualization & Advanced Analysis
Task 2  : Churn Count Visualization

Steps covered
  1. Column chart of customer counts in the Churn column
  2. Labels showing the exact count for each category
  3. Chart title and axis labels

Output (saved in ./output):
  task2_churn_count_chart.png
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
# Load data and count churn categories
# ----------------------------------------------------------------------------
df = pd.read_csv(DATA_FILE)

churn_counts = df["Churn"].value_counts().reindex(["No", "Yes"])
labels = ["Not Churned (No)", "Churned (Yes)"]
total = churn_counts.sum()

print("Churn counts:")
print(churn_counts)
print(f"Churn rate: {churn_counts['Yes'] / total * 100:.2f} %")

# ----------------------------------------------------------------------------
# Column chart
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(labels, churn_counts.values, color=["#4C9F70", "#E4572E"],
              edgecolor="black", width=0.55)

# Data labels: exact count (and share of total) above each column
for bar, value in zip(bars, churn_counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 60,
            f"{value:,}\n({value / total * 100:.1f}%)",
            ha="center", va="bottom", fontsize=12, fontweight="bold")

# Title and axis labels
ax.set_title("Customer Churn Count: Churned vs. Non-Churned Customers",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Churn Status", fontsize=12)
ax.set_ylabel("Number of Customers", fontsize=12)
ax.set_ylim(0, churn_counts.max() * 1.18)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()
out_path = os.path.join(OUTPUT_DIR, "task2_churn_count_chart.png")
plt.savefig(out_path, dpi=200)
print(f"\nChart saved to: {out_path}")
plt.show()

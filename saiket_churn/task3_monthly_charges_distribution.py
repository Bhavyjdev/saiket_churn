"""
SaiKet Systems - Business Analysis Internship
Project : Customer Segmentation Visualization & Advanced Analysis
Task 3  : Monthly Charges Distribution

Steps covered
  1. Histogram of the MonthlyCharges column
  2. Bin size of 10 (intervals of 10)
  3. Descriptive title and axis labels

Output (saved in ./output):
  task3_monthly_charges_histogram.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "Telco_Customer_Churn_Dataset.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BIN_SIZE = 10

# ----------------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------------
df = pd.read_csv(DATA_FILE)
charges = df["MonthlyCharges"]

print("MonthlyCharges summary:")
print(charges.describe().round(2))

# Bin edges in intervals of 10 covering the whole range (e.g. 10, 20, ..., 120)
bin_start = int(np.floor(charges.min() / BIN_SIZE) * BIN_SIZE)
bin_end = int(np.ceil(charges.max() / BIN_SIZE) * BIN_SIZE)
bins = np.arange(bin_start, bin_end + BIN_SIZE, BIN_SIZE)

# ----------------------------------------------------------------------------
# Histogram
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6))
counts, edges, patches = ax.hist(charges, bins=bins, color="#3A86FF",
                                 edgecolor="black", alpha=0.9)

# Count label above every bar
for count, left in zip(counts, edges[:-1]):
    if count > 0:
        ax.text(left + BIN_SIZE / 2, count + 12, f"{int(count)}",
                ha="center", va="bottom", fontsize=9)

# Mean and median reference lines
ax.axvline(charges.mean(), color="red", linestyle="--", linewidth=1.5,
           label=f"Mean = ${charges.mean():.2f}")
ax.axvline(charges.median(), color="green", linestyle="--", linewidth=1.5,
           label=f"Median = ${charges.median():.2f}")

ax.set_title("Distribution of Monthly Charges (Bin Size = $10)",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Monthly Charges ($)", fontsize=12)
ax.set_ylabel("Number of Customers", fontsize=12)
ax.set_xticks(bins)
ax.set_ylim(0, counts.max() * 1.12)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()
out_path = os.path.join(OUTPUT_DIR, "task3_monthly_charges_histogram.png")
plt.savefig(out_path, dpi=200)
print(f"\nChart saved to: {out_path}")
plt.show()

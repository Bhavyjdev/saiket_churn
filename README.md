# SaiKet Systems - Business Analysis Internship
## Customer Segmentation Visualization & Advanced Analysis (Telco Churn)

Each task is a separate, self-contained Python script.

| File | Task |
|------|------|
| task1_data_overview_and_sorting.py | Data overview, sort by tenure, filter churned customers |
| task2_churn_count_visualization.py | Column chart of churned vs. non-churned counts |
| task3_monthly_charges_distribution.py | Histogram of MonthlyCharges (bin size 10) |
| task4_churn_rates_by_gender.py | Pivot table + clustered bar chart by gender |
| task5_tenure_charges_heatmap.py | Heatmap of MonthlyCharges x Tenure x Churn |

## Run
```
pip install -r requirements.txt
python task1_data_overview_and_sorting.py
```
Keep `Telco_Customer_Churn_Dataset.csv` in the same folder as the scripts.
Results are written to an `output/` folder.

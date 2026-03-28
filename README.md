# Electricity Revenue Analytics Pipeline

**End-to-end Python data analysis pipeline + Power BI dashboard for electricity consumer billing data**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)](https://powerbi.microsoft.com)
[![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

This project demonstrates a complete **data analysis and business intelligence pipeline** applied to **138,509 electricity consumer billing records** across 12 account categories.

It mirrors real-world revenue operations analytics — the kind used by power distribution utilities to track billing performance, identify revenue leakage, flag high-risk defaulters, and drive targeted collection campaigns.

**Built by:** Shaik Abdullah — Data Analyst with 10+ years in electricity billing & revenue operations
**Live profile:** [linkedin.com/in/skbhd1-abdullah](https://linkedin.com/in/skbhd1-abdullah)

---

## Power BI Dashboard

### Page 1 — Executive Overview
![Executive Overview](page1_executive_overview.png)

> 4 KPI cards showing Total Accounts (139K), Total Billing (1.49bn), Bad Debt Rate (46.19%) and Collection Rate (87.82%) — with billing breakdown by category and account share donut chart.

---

### Page 2 — Category Analysis
![Category Analysis](page2_category_analysis.png)

> Interactive slicer to filter by any account category. Stacked bar chart comparing Billing, 90-Day Debt and Receipting side by side. Pie chart showing bad debt distribution across categories.

---

### Page 3 — Risk & Defaulters
![Risk & Defaulters](page3_risk_defaulters.png)

> 3 KPI cards: 35K high-risk accounts, 1bn at-risk debt, 854M recoverable revenue. Column chart showing High/Medium/Low risk by category. Debt tier donut showing 71.56% of debt is Critical tier.

---

## Key Findings

| Metric | Value |
|---|---|
| Total consumer accounts | 138,509 |
| Total billing | 1,494,244,373 |
| Collection rate | 87.8% |
| Revenue leakage | 182M |
| 90-day debt / billing ratio | 89.7% |
| Bad debt rate | 46.2% |
| High-risk accounts flagged | 34,624 |
| Recoverable revenue (with ID) | 854M |
| Critical debt tier | 71.56% of all 90-day debt |

---

## What This Project Includes

### 1. Python Analysis Pipeline (`electricity_revenue_analysis.py`)
- Loads and validates 138,509 rows from Excel
- Feature engineering: Revenue Leakage, Risk Segmentation, Debt Tiers, Collection Status
- Anomaly detection on collection ratios (±3 SD)
- Generates 5 charts automatically
- Exports 4-sheet Excel report with 34,624 flagged high-risk accounts

### 2. Power BI Dashboard (3 pages)
| Page | Visuals |
|---|---|
| Executive Overview | 4 KPI cards, billing bar chart, accounts donut |
| Category Analysis | Slicer, stacked bar chart, bad debt pie chart |
| Risk & Defaulters | 3 KPI cards, risk column chart, debt tier donut |

### 3. Auto-Generated Charts (Python)
| Chart | Description |
|---|---|
| `01_revenue_overview.png` | Revenue metrics bar + risk pie |
| `02_bad_debt_by_category.png` | Bad debt rate by category |
| `03_billing_vs_debt_by_category.png` | Billing vs 90-day debt |
| `04_collection_ratio_distribution.png` | Collection ratio distribution |
| `05_risk_heatmap.png` | Risk heatmap across categories |

### 4. Excel Report (4 sheets)
| Sheet | Contents |
|---|---|
| Executive Summary | Top-level KPIs |
| Category Analysis | Full breakdown by account type |
| High-Risk Defaulters | 34,624 accounts with priority scores |
| Full Dataset (Cleaned) | Enriched dataset with new features |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| pandas | Data loading, cleaning, transformation |
| NumPy | Feature engineering, anomaly detection |
| matplotlib | Chart generation |
| seaborn | Heatmap visualisation |
| openpyxl | Multi-sheet Excel export |
| Power BI Desktop | Interactive 3-page dashboard |
| DAX | Custom measures and KPI calculations |

---

## How to Run the Python Pipeline

```bash
# 1. Clone the repo
git clone https://github.com/skbhd1/electricity-revenue-analytics.git
cd electricity-revenue-analytics

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl

# 3. Place your dataset in the root folder
# File: Project_Data_Set_-_27_03_2026.xlsx

# 4. Run the pipeline
python electricity_revenue_analysis.py
```

Outputs are saved to the `outputs/` folder automatically.

---

## Project Structure

```
electricity-revenue-analytics/
│
├── electricity_revenue_analysis.py   # Main Python pipeline
├── PowerBI_Dataset.xlsx              # Power BI ready dataset (4 sheets)
├── README.md                         # This file
│
├── screenshots/                      # Dashboard screenshots
│   ├── page1_executive_overview.png
│   ├── page2_category_analysis.png
│   └── page3_risk_defaulters.png
│
└── outputs/                          # Generated by Python pipeline
    ├── 01_revenue_overview.png
    ├── 02_bad_debt_by_category.png
    ├── 03_billing_vs_debt_by_category.png
    ├── 04_collection_ratio_distribution.png
    ├── 05_risk_heatmap.png
    └── Revenue_Analysis_Report.xlsx
```

---

## Dataset

**Source:** Public electricity consumer billing dataset
**Size:** 138,509 rows × 16 columns
**Domain:** Electricity distribution / Revenue operations

**Columns:** Account Category, Property Value, Property Size, Total Billing, Avg Billing, Total Receipting, Avg Receipting, Total 90 Debt, Total Write Off, Collection Ratio, Debt Billing Ratio, Total Elec Bill, Has ID No, Bad Debt

> The dataset does not contain personally identifiable information (PII).

---

## Author

**Shaik Abdullah**
Data Analyst | Revenue Operations | Python & Power BI
10+ years in electricity billing analytics at TGSPDCL/TSSPDCL, Telangana

- LinkedIn: [linkedin.com/in/skbhd1-abdullah](https://linkedin.com/in/skbhd1-abdullah)
- GitHub: [github.com/skbhd1](https://github.com/skbhd1)
- Email: skbhd1@gmail.com

---

*ML-based bad debt risk predictor — coming soon (Project 3)*

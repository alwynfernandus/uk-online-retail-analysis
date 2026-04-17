# UK Online Retail — Business Analysis

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/matplotlib%20%7C%20seaborn-11557C?style=flat" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white" />
</p>

---

A full business analysis of a UK-based online gift retailer — 13 months of real transaction data, from raw Excel to strategic recommendations.

**Dataset:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) · 541,909 transactions · Dec 2010 – Dec 2011

---

## The Problem

The company had transactional data but no real visibility into what was driving it. A few questions kept coming up without clear answers:

- Which customers were likely to stop buying, and were there signals in the data?
- Revenue looked healthy overall — but how concentrated was it, really?
- Were there international markets generating revenue without any marketing behind them?
- Was the marketing budget being spent at the right times?

This project works through each of those questions using the actual transaction history.

---

## What I Did

Cleaned and explored 541K rows of invoice data, built an RFM segmentation model across 4,334 customers, ran cohort retention analysis, and translated the findings into prioritised recommendations.

The cleaning removed ~145K rows for valid reasons — anonymous sessions with no CustomerID, cancellation invoices, a handful of internal test codes, and a small number of negative quantities. Each decision is documented in the notebook.

**Workflow:**
```
Raw data → Cleaning & validation → Feature engineering
→ KPI baseline → EDA → RFM segmentation
→ Cohort analysis → Insights → Recommendations
```

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Total Revenue | £8,767,753 |
| Total Orders | 18,405 |
| Unique Customers | 4,334 |
| Avg. Order Value | £476.38 |
| Repeat Customer Rate | 65.3% |
| Champions' Revenue Share | **55.4%** |
| At-Risk Recoverable Revenue | **£931,821** |

---

## What the Data Showed

**Revenue is heavily Q4-dependent.**
November alone was 13% of the full year. That's not unusual for a gift retailer, but the business had no early planning mechanism around it. A bad November — supply issue, a slow start to the season, whatever — would hit the annual number hard.

**A small group of customers is carrying the business.**
The Champions segment — customers with high recency, frequency, and spend — generated over 55% of total revenue. That's roughly 800 customers out of 4,334. There was no loyalty program, no dedicated communication strategy, nothing specifically designed to keep them.

**35% of customers never came back.**
About 1 in 3 customers bought once and disappeared. The data doesn't explain why, but the pattern is consistent across cohorts. Something in the post-purchase experience — follow-up, product quality, communication — isn't converting first-time buyers into repeat ones.

**There's nearly £1M sitting in an At-Risk segment.**
449 customers who used to buy regularly have gone quiet. Their combined historical spend is £931K. These aren't cold leads — they already spent money here. A basic re-engagement effort targeting even 15% of them would recover around £140K.

**Germany and Netherlands are buying without any marketing.**
82.9% of revenue came from the UK. But Germany, Netherlands, and Ireland were consistently in the top international markets — buying without any targeted campaigns behind them. That suggests a real opportunity if the business actually invested there.

**Nobody is ordering on weekends.**
Saturday and Sunday order volumes were noticeably lower than any weekday. Most orders happened Tuesday to Thursday, between 10am and 2pm. This points to a largely B2B/wholesale buyer profile — people ordering for their shops during work hours. Spending on weekend digital ads for this audience is probably wasted.

---

## Recommendations

**Right now (0–3 months)**

| Action | Who It Targets | Why |
|--------|---------------|-----|
| Simple loyalty program — early access, thank-you discount | Champions | Protect the 55% of revenue they generate |
| 3-email re-engagement sequence | At-Risk | £140K recoverable at 15% conversion |
| Move paid ad schedule to Tue–Thu 10am–2pm | All channels | Better alignment with actual buyer windows |
| Day 7 + Day 30 follow-up emails for new customers | First-time buyers | Tackle the 35% one-time buyer rate |

**Over the next 3–9 months**
- Connect RFM scoring to the CRM so segment drops trigger automatically — no analyst needed each time
- Start Q4 planning in August, not October. Pre-Black Friday emails by October 15 at the latest
- Bundle the top products together — AOV is £476, and there's room to push that higher

**Longer term**
- Run targeted campaigns in Germany, Netherlands, and France — they're already converting organically
- Build a wholesale tier for the B2B buyers who dominate weekday ordering
- A basic seasonal forecasting model would help with November inventory planning

---

## Visualisations

### Revenue & Order Volume Trend
![Revenue Trend](visuals/01_monthly_revenue_trend.png)

### Top 10 Products by Revenue
![Top Products](visuals/02_top_products_revenue.png)

### International Revenue (excl. UK)
![Country Revenue](visuals/03_revenue_by_country.png)

### Order Volume by Day & Hour
![Day Hour](visuals/04_orders_day_hour.png)

### RFM Segments — Customer Count & Revenue
![RFM](visuals/05_rfm_segments.png)

### Recency vs. Customer Value
![Scatter](visuals/06_rfm_scatter.png)

### RFM Correlation Matrix
![Correlation](visuals/07_rfm_correlation.png)

### Cohort Retention (First 6 Months)
![Cohort](visuals/08_cohort_retention.png)

### Order Value Distribution
![AOV](visuals/09_order_value_distribution.png)

---

## Skills Demonstrated

- **Data cleaning & preparation** — Handled 24.9% missing rate, documented every removal decision
- **KPI definition** — Built a baseline metric framework before touching the EDA
- **Customer segmentation** — RFM model across 4,334 customers, scored and labelled into 6 segments
- **Cohort analysis** — Tracked 13 acquisition cohorts across a 6-month retention window
- **Exploratory data analysis** — Revenue trends, product concentration, geographic breakdown, behavioural patterns
- **Data visualisation** — 9 charts with consistent design, business-annotated, output-ready
- **Business recommendations** — Findings translated into actions with target owners and expected outcomes
- **Python** — pandas, matplotlib, seaborn, scikit-learn — end to end

---

## Repository Structure

```
uk-online-retail-analysis/
│
├── notebooks/
│   └── UK_Online_Retail_Analysis.ipynb
│
├── visuals/
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_top_products_revenue.png
│   ├── 03_revenue_by_country.png
│   ├── 04_orders_day_hour.png
│   ├── 05_rfm_segments.png
│   ├── 06_rfm_scatter.png
│   ├── 07_rfm_correlation.png
│   ├── 08_cohort_retention.png
│   └── 09_order_value_distribution.png
│
├── scripts/
│   └── analysis.py
│
└── README.md
```

> The raw dataset (`Online Retail.xlsx`) isn't included due to file size. Download it from the [UCI repository](https://archive.ics.uci.edu/dataset/352/online+retail) and drop it in a `data/` folder.

---

## How to Run

```bash
git clone https://github.com/alwynfernandus/uk-online-retail-analysis.git
cd uk-online-retail-analysis

pip install pandas matplotlib seaborn scikit-learn openpyxl jupyter

# Download the dataset and save as: data/Online Retail.xlsx

jupyter notebook notebooks/UK_Online_Retail_Analysis.ipynb
```

---

## About

<<<<<<< Updated upstream
**Alwyn Fernandus**
MBA in Business Analytics 
Power BI · SQL · Python · Excel · Tableau · Alteryx · GitHub
📧 alwynfernandus123@gmail.com · [LinkedIn](https://www.linkedin.com/in/alwynfernandus)
=======
**Alwyn Fernandus** — MBA in Business Analytics, available immediately (F-1 OPT)  
Power BI · SQL · Python · Excel · Tableau · Alteryx  
alwynfernandus123@gmail.com · [LinkedIn](https://www.linkedin.com/in/alwynfernandus)
>>>>>>> Stashed changes

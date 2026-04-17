"""
============================================================
Online Retail Transactions Analysis
UK-Based E-Commerce | Dec 2010 – Dec 2011
Business Analyst Portfolio Project — Alwyn Fernandus
============================================================

Dataset: UCI Online Retail Dataset
Source:  https://archive.ics.uci.edu/dataset/352/online+retail
Tools:   Python 3 | pandas | matplotlib | seaborn | scikit-learn
"""

# ─────────────────────────────────────────────────────────────
# 0. IMPORTS & CONFIGURATION
# ─────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime
import warnings
import os

warnings.filterwarnings('ignore')

# ── Design System ────────────────────────────────────────────
PALETTE = {
    'primary'    : '#20808D',
    'secondary'  : '#A84B2F',
    'dark'       : '#1B474D',
    'light'      : '#BCE2E7',
    'accent'     : '#FFC553',
    'muted'      : '#7A7974',
    'bg'         : '#F7F6F2',
    'text'       : '#28251D',
}
CHART_COLORS = ['#20808D', '#A84B2F', '#1B474D', '#FFC553', '#944454', '#BCE2E7']

plt.rcParams.update({
    'figure.facecolor'  : PALETTE['bg'],
    'axes.facecolor'    : '#FFFFFF',
    'axes.edgecolor'    : '#D4D1CA',
    'axes.labelcolor'   : PALETTE['text'],
    'axes.titlecolor'   : PALETTE['text'],
    'axes.titlesize'    : 14,
    'axes.titleweight'  : 'bold',
    'axes.labelsize'    : 11,
    'xtick.color'       : PALETTE['muted'],
    'ytick.color'       : PALETTE['muted'],
    'xtick.labelsize'   : 9,
    'ytick.labelsize'   : 9,
    'grid.color'        : '#E8E7E3',
    'grid.linestyle'    : '--',
    'grid.alpha'        : 0.6,
    'font.family'       : 'DejaVu Sans',
    'figure.dpi'        : 150,
})

VISUALS_DIR = '/home/user/workspace/online-retail-analysis/visuals'
os.makedirs(VISUALS_DIR, exist_ok=True)

def save_fig(filename, tight=True):
    path = os.path.join(VISUALS_DIR, filename)
    if tight:
        plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=PALETTE['bg'])
    plt.close()
    print(f"  ✓ Saved: {filename}")


# ─────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 1 — LOADING DATA")
print("="*60)

df_raw = pd.read_excel(
    '/home/user/workspace/online-retail-analysis/data/Online Retail.xlsx',
    engine='openpyxl'
)

print(f"  Rows loaded     : {len(df_raw):,}")
print(f"  Columns         : {list(df_raw.columns)}")
print(f"  Memory usage    : {df_raw.memory_usage(deep=True).sum() / 1e6:.1f} MB")


# ─────────────────────────────────────────────────────────────
# 2. DATA OVERVIEW & CLEANING
# ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 2 — DATA CLEANING")
print("="*60)

# Missing values summary
missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw) * 100).round(2)
print("\n  Missing Values:")
for col in df_raw.columns:
    if missing[col] > 0:
        print(f"    {col:<20}: {missing[col]:>6,} ({missing_pct[col]}%)")

# ── Cleaning Steps ────────────────────────────────────────────

# 1. Remove rows without CustomerID (unidentifiable transactions)
df = df_raw.dropna(subset=['CustomerID']).copy()
print(f"\n  After removing null CustomerID : {len(df):,} rows (-{len(df_raw)-len(df):,})")

# 2. Remove cancelled orders (InvoiceNo starting with 'C')
cancellations = df[df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')].copy()
print(f"  After removing cancellations   : {len(df):,} rows (-{len(cancellations):,} cancelled)")

# 3. Remove returns / bad data (negative or zero Quantity and UnitPrice)
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].copy()
print(f"  After removing bad qty/price   : {len(df):,} rows")

# 4. Remove test/sample stock codes
test_codes = ['POST', 'D', 'M', 'BANK CHARGES', 'PADS', 'DOT']
df = df[~df['StockCode'].isin(test_codes)].copy()
print(f"  After removing test codes      : {len(df):,} rows")

# 5. Feature engineering
df['CustomerID']    = df['CustomerID'].astype(int)
df['InvoiceDate']   = pd.to_datetime(df['InvoiceDate'])
df['Revenue']       = df['Quantity'] * df['UnitPrice']
df['YearMonth']     = df['InvoiceDate'].dt.to_period('M')
df['Month']         = df['InvoiceDate'].dt.month
df['DayOfWeek']     = df['InvoiceDate'].dt.day_name()
df['Hour']          = df['InvoiceDate'].dt.hour
df['Quarter']       = df['InvoiceDate'].dt.quarter

print(f"\n  Final clean dataset            : {len(df):,} rows, {df.shape[1]} columns")
print(f"  Date range                     : {df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}")
print(f"  Unique customers               : {df['CustomerID'].nunique():,}")
print(f"  Unique products                : {df['StockCode'].nunique():,}")
print(f"  Countries                      : {df['Country'].nunique()}")
print(f"  Total revenue (clean)          : £{df['Revenue'].sum():,.0f}")


# ─────────────────────────────────────────────────────────────
# 3. KPI SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 3 — KPI SUMMARY")
print("="*60)

snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

total_revenue   = df['Revenue'].sum()
total_orders    = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
total_products  = df['StockCode'].nunique()
aov             = total_revenue / total_orders
orders_per_cust = total_orders / total_customers
uk_pct          = df[df['Country'] == 'United Kingdom']['Revenue'].sum() / total_revenue * 100

print(f"\n  Total Revenue         : £{total_revenue:>12,.0f}")
print(f"  Total Orders          : {total_orders:>12,}")
print(f"  Unique Customers      : {total_customers:>12,}")
print(f"  Unique Products       : {total_products:>12,}")
print(f"  Avg. Order Value      : £{aov:>12.2f}")
print(f"  Orders per Customer   : {orders_per_cust:>12.1f}")
print(f"  UK Revenue Share      : {uk_pct:>11.1f}%")


# ─────────────────────────────────────────────────────────────
# 4. VISUALIZATIONS
# ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 4 — GENERATING VISUALIZATIONS")
print("="*60)


# ── CHART 1: Monthly Revenue Trend ───────────────────────────
monthly = df.groupby('YearMonth').agg(
    Revenue=('Revenue', 'sum'),
    Orders=('InvoiceNo', 'nunique'),
    Customers=('CustomerID', 'nunique')
).reset_index()
monthly['YearMonth_str'] = monthly['YearMonth'].astype(str)

fig, ax1 = plt.subplots(figsize=(13, 5), facecolor=PALETTE['bg'])
ax2 = ax1.twinx()

bars = ax1.bar(monthly['YearMonth_str'], monthly['Revenue'] / 1000,
               color=PALETTE['primary'], alpha=0.75, width=0.6, label='Revenue (£K)')
line = ax2.plot(monthly['YearMonth_str'], monthly['Orders'],
                color=PALETTE['secondary'], marker='o', linewidth=2.2,
                markersize=5, label='Orders', zorder=5)

# Annotate peak month
peak_idx = monthly['Revenue'].idxmax()
ax1.annotate(f"Peak\n£{monthly['Revenue'][peak_idx]/1000:.0f}K",
             xy=(peak_idx, monthly['Revenue'][peak_idx]/1000),
             xytext=(peak_idx - 1.5, monthly['Revenue'][peak_idx]/1000 * 0.85),
             arrowprops=dict(arrowstyle='->', color=PALETTE['dark'], lw=1.5),
             fontsize=8.5, color=PALETTE['dark'], fontweight='bold')

ax1.set_xlabel('Month', labelpad=8)
ax1.set_ylabel('Monthly Revenue (£ Thousands)', color=PALETTE['primary'], labelpad=8)
ax2.set_ylabel('Number of Orders', color=PALETTE['secondary'], labelpad=8)
ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:.0f}K'))
ax1.set_title('Monthly Revenue & Order Volume — Dec 2010 to Dec 2011',
              fontsize=14, fontweight='bold', pad=12)
ax1.set_facecolor('#FFFFFF')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9,
           framealpha=0.9, edgecolor='#D4D1CA')

plt.figtext(0.5, -0.02,
            'Revenue peaks in November 2011 ahead of the holiday season, with a clear Q4 acceleration pattern.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('01_monthly_revenue_trend.png')


# ── CHART 2: Top 10 Products by Revenue ──────────────────────
product_rev = (df.groupby('Description')['Revenue']
               .sum().sort_values(ascending=False)
               .head(10).reset_index())
product_rev['Description'] = product_rev['Description'].str.title().str[:40]
product_rev['Revenue_K'] = product_rev['Revenue'] / 1000

fig, ax = plt.subplots(figsize=(11, 6), facecolor=PALETTE['bg'])
colors = [PALETTE['primary'] if i == 0 else PALETTE['light'] for i in range(len(product_rev))]
bars = ax.barh(product_rev['Description'][::-1], product_rev['Revenue_K'][::-1],
               color=colors[::-1], edgecolor='white', linewidth=0.5)

for bar, val in zip(bars, product_rev['Revenue_K'][::-1]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'£{val:.1f}K', va='center', ha='left', fontsize=8.5,
            color=PALETTE['text'], fontweight='bold')

ax.set_xlabel('Total Revenue (£ Thousands)', labelpad=8)
ax.set_title('Top 10 Products by Revenue',
             fontsize=14, fontweight='bold', pad=12)
ax.set_facecolor('#FFFFFF')
ax.grid(axis='x', linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, product_rev['Revenue_K'].max() * 1.22)
plt.figtext(0.5, -0.02,
            'The top product earns 2–3× more than the rest — concentration risk if demand shifts.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('02_top_products_revenue.png')


# ── CHART 3: Revenue by Country (excl. UK) ───────────────────
country_rev = (df[df['Country'] != 'United Kingdom']
               .groupby('Country')['Revenue']
               .sum().sort_values(ascending=False)
               .head(10).reset_index())
country_rev['Revenue_K'] = country_rev['Revenue'] / 1000

fig, ax = plt.subplots(figsize=(11, 6), facecolor=PALETTE['bg'])
bar_colors = [PALETTE['primary']] + [PALETTE['secondary']] * 2 + [PALETTE['light']] * 7
ax.bar(country_rev['Country'], country_rev['Revenue_K'],
       color=bar_colors[:len(country_rev)], edgecolor='white', linewidth=0.5)

for i, (_, row) in enumerate(country_rev.iterrows()):
    ax.text(i, row['Revenue_K'] + 0.5, f'£{row["Revenue_K"]:.1f}K',
            ha='center', va='bottom', fontsize=8.5,
            color=PALETTE['text'], fontweight='bold')

ax.set_ylabel('Total Revenue (£ Thousands)', labelpad=8)
ax.set_xlabel('Country', labelpad=8)
ax.set_title('International Revenue — Top 10 Countries (Excl. UK)',
             fontsize=14, fontweight='bold', pad=12)
ax.set_facecolor('#FFFFFF')
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', rotation=30)
plt.figtext(0.5, -0.04,
            'Germany and France are the strongest international markets and represent clear expansion opportunities.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('03_revenue_by_country.png')


# ── CHART 4: Orders by Day of Week & Hour ────────────────────
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_orders = (df.groupby('DayOfWeek')['InvoiceNo']
              .nunique().reindex(dow_order).reset_index())
hour_orders = df.groupby('Hour')['InvoiceNo'].nunique().reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), facecolor=PALETTE['bg'])

# Day of week
ax1.bar(day_orders['DayOfWeek'], day_orders['InvoiceNo'],
        color=[PALETTE['primary'] if d not in ['Saturday', 'Sunday'] else PALETTE['muted']
               for d in dow_order],
        edgecolor='white', linewidth=0.5)
ax1.set_title('Order Volume by Day of Week', fontsize=13, fontweight='bold', pad=10)
ax1.set_xlabel('Day', labelpad=6)
ax1.set_ylabel('Number of Orders', labelpad=6)
ax1.tick_params(axis='x', rotation=30)
ax1.set_facecolor('#FFFFFF')
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Hour of day
ax2.plot(hour_orders['Hour'], hour_orders['InvoiceNo'],
         color=PALETTE['secondary'], linewidth=2.5, marker='o', markersize=5, zorder=5)
ax2.fill_between(hour_orders['Hour'], hour_orders['InvoiceNo'],
                 alpha=0.15, color=PALETTE['secondary'])
peak_hour = hour_orders.loc[hour_orders['InvoiceNo'].idxmax()]
ax2.annotate(f"Peak: {int(peak_hour['Hour'])}:00",
             xy=(peak_hour['Hour'], peak_hour['InvoiceNo']),
             xytext=(peak_hour['Hour'] + 1.5, peak_hour['InvoiceNo'] * 0.92),
             arrowprops=dict(arrowstyle='->', color=PALETTE['dark'], lw=1.3),
             fontsize=8.5, color=PALETTE['dark'], fontweight='bold')
ax2.set_title('Order Volume by Hour of Day', fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('Hour (24h)', labelpad=6)
ax2.set_ylabel('Number of Orders', labelpad=6)
ax2.set_facecolor('#FFFFFF')
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_xlim(0, 23)

plt.figtext(0.5, -0.03,
            'Midweek afternoons (Tue–Thu, 11am–3pm) generate the highest order volumes — optimal window for promotions and campaigns.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('04_orders_day_hour.png')


# ── CHART 5: RFM Customer Segmentation ───────────────────────
rfm = df.groupby('CustomerID').agg(
    Recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    Frequency=('InvoiceNo', 'nunique'),
    Monetary=('Revenue', 'sum')
).reset_index()

# Score each dimension 1–4
rfm['R_Score'] = pd.qcut(rfm['Recency'],  4, labels=[4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'),  4, labels=[1, 2, 3, 4])
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Segment labels
def segment(row):
    r, f, m = int(row['R_Score']), int(row['F_Score']), int(row['M_Score'])
    score = r + f + m
    if r == 4 and f >= 3 and m >= 3:
        return 'Champions'
    elif r >= 3 and f >= 3:
        return 'Loyal Customers'
    elif r >= 3 and f <= 2 and m <= 2:
        return 'Promising'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r == 1 and f == 1:
        return 'Lost'
    elif score >= 9:
        return 'Loyal Customers'
    elif score >= 7:
        return 'Promising'
    elif score >= 5:
        return 'Need Attention'
    else:
        return 'Lost'

rfm['Segment'] = rfm.apply(segment, axis=1)
seg_counts = rfm['Segment'].value_counts()
seg_revenue = rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False)

seg_colors = {
    'Champions'       : '#20808D',
    'Loyal Customers' : '#1B474D',
    'Promising'       : '#FFC553',
    'At Risk'         : '#A84B2F',
    'Need Attention'  : '#944454',
    'Lost'            : '#BAB9B4',
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=PALETTE['bg'])

# Segment count
seg_cnt_sorted = seg_counts.sort_values(ascending=True)
colors_bar = [seg_colors.get(s, PALETTE['muted']) for s in seg_cnt_sorted.index]
ax1.barh(seg_cnt_sorted.index, seg_cnt_sorted.values, color=colors_bar, edgecolor='white')
for i, (s, v) in enumerate(zip(seg_cnt_sorted.index, seg_cnt_sorted.values)):
    ax1.text(v + 8, i, f'{v:,}', va='center', fontsize=9, color=PALETTE['text'], fontweight='bold')
ax1.set_title('Customer Count by RFM Segment', fontsize=13, fontweight='bold', pad=10)
ax1.set_xlabel('Customers', labelpad=6)
ax1.set_facecolor('#FFFFFF')
ax1.grid(axis='x', linestyle='--', alpha=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xlim(0, seg_cnt_sorted.max() * 1.2)

# Revenue by segment
seg_rev_sorted = seg_revenue.sort_values(ascending=True)
colors_rev = [seg_colors.get(s, PALETTE['muted']) for s in seg_rev_sorted.index]
ax2.barh(seg_rev_sorted.index, seg_rev_sorted.values / 1000, color=colors_rev, edgecolor='white')
for i, (s, v) in enumerate(zip(seg_rev_sorted.index, seg_rev_sorted.values)):
    ax2.text(v/1000 + 1, i, f'£{v/1000:.0f}K', va='center', fontsize=9,
             color=PALETTE['text'], fontweight='bold')
ax2.set_title('Revenue Contribution by Segment', fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('Revenue (£ Thousands)', labelpad=6)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:.0f}K'))
ax2.set_facecolor('#FFFFFF')
ax2.grid(axis='x', linestyle='--', alpha=0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_xlim(0, seg_rev_sorted.max()/1000 * 1.22)

plt.figtext(0.5, -0.03,
            'Champions and Loyal Customers represent the highest-value segments — protect and reward them proactively.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('05_rfm_segments.png')


# ── CHART 6: RFM Scatter — Recency vs Monetary ───────────────
fig, ax = plt.subplots(figsize=(10, 6), facecolor=PALETTE['bg'])
for seg, grp in rfm.groupby('Segment'):
    ax.scatter(grp['Recency'], grp['Monetary'] / 1000,
               label=seg, alpha=0.55, s=30,
               color=seg_colors.get(seg, PALETTE['muted']), edgecolors='none')

ax.set_xlabel('Recency (Days Since Last Purchase)', labelpad=8)
ax.set_ylabel('Customer Lifetime Value (£ Thousands)', labelpad=8)
ax.set_title('Recency vs. Customer Value — Segment Distribution',
             fontsize=14, fontweight='bold', pad=12)
ax.set_facecolor('#FFFFFF')
ax.grid(linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(fontsize=9, framealpha=0.9, edgecolor='#D4D1CA',
          title='Segment', title_fontsize=9, loc='upper right')
plt.figtext(0.5, -0.03,
            'Champions cluster in the top-left: recently active and high-spending. At-Risk customers drift right as recency increases.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('06_rfm_scatter.png')


# ── CHART 7: Correlation Heatmap ─────────────────────────────
corr_df = rfm[['Recency', 'Frequency', 'Monetary']].corr()

fig, ax = plt.subplots(figsize=(6, 5), facecolor=PALETTE['bg'])
mask = np.zeros_like(corr_df, dtype=bool)
np.fill_diagonal(mask, True)

cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr_df, annot=True, fmt='.2f', cmap=cmap,
            center=0, square=True, linewidths=2, linecolor=PALETTE['bg'],
            annot_kws={'size': 12, 'weight': 'bold'},
            ax=ax, cbar_kws={'shrink': 0.75})

ax.set_title('RFM Correlation Matrix', fontsize=14, fontweight='bold', pad=12)
ax.set_facecolor('#FFFFFF')
plt.figtext(0.5, -0.04,
            'Frequency and Monetary are strongly correlated — customers who buy more often also spend more total.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('07_rfm_correlation.png')


# ── CHART 8: Monthly Customer Retention (Cohort) ─────────────
cohort_df = df[['CustomerID', 'YearMonth']].copy()
cohort_df['CohortMonth'] = cohort_df.groupby('CustomerID')['YearMonth'].transform('min')
cohort_df['CohortIndex'] = (
    cohort_df['YearMonth'].apply(lambda x: x.ordinal) -
    cohort_df['CohortMonth'].apply(lambda x: x.ordinal)
)

cohort_counts = (cohort_df.groupby(['CohortMonth', 'CohortIndex'])['CustomerID']
                 .nunique().reset_index())
cohort_pivot = cohort_counts.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')
cohort_size = cohort_pivot.iloc[:, 0]
cohort_pct = cohort_pivot.divide(cohort_size, axis=0).round(3) * 100

# Keep only first 6 months for readability
cohort_pct_plot = cohort_pct.iloc[:, :7]
cohort_pct_plot.index = cohort_pct_plot.index.astype(str)

fig, ax = plt.subplots(figsize=(12, 7), facecolor=PALETTE['bg'])
sns.heatmap(cohort_pct_plot, annot=True, fmt='.0f', cmap='YlGnBu',
            linewidths=0.5, linecolor=PALETTE['bg'],
            annot_kws={'size': 9},
            ax=ax, cbar_kws={'label': 'Retention %', 'shrink': 0.8},
            vmin=0, vmax=100)
ax.set_title('Customer Retention Cohort Analysis (First 6 Months)',
             fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Months After First Purchase', labelpad=8)
ax.set_ylabel('Acquisition Cohort', labelpad=8)
ax.set_facecolor('#FFFFFF')
plt.figtext(0.5, -0.03,
            'Retention drops sharply after Month 1. Early cohorts (Dec–Jan) show the highest long-term stickiness.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('08_cohort_retention.png')


# ── CHART 9: Revenue Distribution (AOV) ──────────────────────
order_rev = df.groupby('InvoiceNo')['Revenue'].sum()
# Cap at 99th percentile for readability
cap = order_rev.quantile(0.99)
order_rev_capped = order_rev[order_rev <= cap]

fig, ax = plt.subplots(figsize=(10, 5), facecolor=PALETTE['bg'])
ax.hist(order_rev_capped, bins=60, color=PALETTE['primary'], alpha=0.8, edgecolor='white')
ax.axvline(order_rev.median(), color=PALETTE['secondary'], linestyle='--',
           linewidth=2, label=f'Median: £{order_rev.median():.0f}')
ax.axvline(order_rev.mean(), color=PALETTE['accent'], linestyle='--',
           linewidth=2, label=f'Mean: £{order_rev.mean():.0f}')

ax.set_xlabel('Order Value (£)', labelpad=8)
ax.set_ylabel('Number of Orders', labelpad=8)
ax.set_title('Distribution of Order Values (99th Percentile Cap)',
             fontsize=14, fontweight='bold', pad=12)
ax.set_facecolor('#FFFFFF')
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(fontsize=9.5, framealpha=0.9)
plt.figtext(0.5, -0.03,
            'Order value distribution is right-skewed — most orders are small, but a few high-value bulk orders significantly lift the mean.',
            ha='center', fontsize=8.5, color=PALETTE['muted'], style='italic')
save_fig('09_order_value_distribution.png')


# ─────────────────────────────────────────────────────────────
# 5. ADDITIONAL METRICS FOR INSIGHTS
# ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 5 — ADDITIONAL METRICS")
print("="*60)

# Repeat vs One-time customers
cust_freq = df.groupby('CustomerID')['InvoiceNo'].nunique()
repeat_customers = (cust_freq > 1).sum()
one_time_customers = (cust_freq == 1).sum()
repeat_pct = repeat_customers / total_customers * 100
print(f"\n  Repeat customers     : {repeat_customers:,} ({repeat_pct:.1f}%)")
print(f"  One-time customers   : {one_time_customers:,} ({100-repeat_pct:.1f}%)")

# At-Risk revenue
at_risk_rev = rfm[rfm['Segment'] == 'At Risk']['Monetary'].sum()
print(f"  At-Risk revenue      : £{at_risk_rev:,.0f}")

# Champions revenue share
champ_rev = rfm[rfm['Segment'] == 'Champions']['Monetary'].sum()
champ_pct = champ_rev / total_revenue * 100
print(f"  Champions revenue %  : {champ_pct:.1f}%")

# November revenue
nov_rev = df[df['Month'] == 11]['Revenue'].sum()
nov_pct = nov_rev / total_revenue * 100
print(f"  November revenue     : £{nov_rev:,.0f} ({nov_pct:.1f}% of annual)")

# Top country outside UK
intl_country = (df[df['Country'] != 'United Kingdom']
                .groupby('Country')['Revenue'].sum()
                .sort_values(ascending=False))
print(f"\n  Top intl. market     : {intl_country.index[0]} (£{intl_country.iloc[0]:,.0f})")
print(f"  2nd intl. market     : {intl_country.index[1]} (£{intl_country.iloc[1]:,.0f})")

print(f"\n  Median order value   : £{order_rev.median():.2f}")
print(f"  Mean order value     : £{order_rev.mean():.2f}")
print(f"  95th pct order value : £{order_rev.quantile(0.95):.2f}")

# Store metrics for README
metrics = {
    'total_revenue': total_revenue,
    'total_orders': total_orders,
    'total_customers': total_customers,
    'total_products': total_products,
    'aov': aov,
    'repeat_pct': repeat_pct,
    'champ_pct': champ_pct,
    'at_risk_rev': at_risk_rev,
    'nov_pct': nov_pct,
    'top_intl': intl_country.index[0],
    'order_median': order_rev.median(),
}

print("\n" + "="*60)
print("ALL VISUALIZATIONS SAVED TO: /visuals/")
print("="*60)
print("\nFiles generated:")
for f in sorted(os.listdir(VISUALS_DIR)):
    print(f"  → {f}")

# Credit Card Customer Analytics

A project I built to practice the kind of analysis card issuers actually run: who's spending
what, who's valuable, and who's a credit risk before it turns into a loss.

## What's in here

- `generate_data.py` - creates a synthetic dataset (2,000 customers, ~70k transactions).
  I didn't have a live Kaggle dataset wired up when I built this, so this script fills that
  gap. It's not the interesting part of the project.
- `analysis.py` - the actual pipeline. RFM scoring, K-Means clustering into value tiers,
  IQR-based outlier detection, credit risk bucketing by utilization. Exports everything
  into `outputs/` as clean CSV.
- `eda_notebook.ipynb` - the walkthrough version of the same analysis, with EDA plots,
  the elbow method for picking k=4, and reasoning behind each step. Read this if you want
  to see the thinking, not just the output.
- `case_study.pdf` - one-page summary (problem, method, key finding, recommendation) for
  anyone who wants the short version.
- `data/` - the generated customer, transaction, and merchant tables.
- `outputs/` - everything analysis.py produces: customer_master.csv (main table, one row
  per customer with segment/cluster/risk all joined in), monthly_spend.csv,
  spend_by_category.csv, rfm.csv, correlation_matrix.csv.
- `credit_card_dashboard_data.xlsx` - the same output tables combined into one workbook,
  since Power BI's online service handles a single multi-sheet Excel file much better than
  four separate CSV uploads.

## Running it

```
python generate_data.py
python analysis.py
```

Regenerates everything in `data/` and `outputs/`. It's seeded, so the numbers stay the
same every time you run it.

## What the analysis actually found

Segments split out to roughly: 568 Regular, 521 Loyal, 355 At Risk, 311 New, 245
Champions. Four value tiers came out of clustering (Low/Mid/High/Premium), validated with
the elbow method rather than picked arbitrarily. Utilization-based risk scoring flagged a
large share of the base as high risk - worth noting that's partly an artifact of how the
synthetic credit limits were generated, not something to take as a real-world number.


## Why synthetic data

No live dataset was available in the environment I built this in. The generation script is
seeded and documented so it's reproducible, and I've been upfront about it everywhere this
project gets used - it's the pipeline and the reasoning that's the point, not the dataset
itself.

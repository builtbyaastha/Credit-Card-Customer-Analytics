import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

cust = pd.read_csv("data/customers.csv")
txn = pd.read_csv("data/transactions.csv", parse_dates=["transaction_date"])

txn["month"] = txn.transaction_date.dt.to_period("M").astype(str)

monthly_spend = txn.groupby(["customer_id","month"]).amount.sum().reset_index()
monthly_spend.to_csv("outputs/monthly_spend.csv", index=False)

cat_spend = txn.groupby(["customer_id","merchant_category"]).amount.sum().reset_index()
cat_spend.to_csv("outputs/spend_by_category.csv", index=False)

snapshot_date = txn.transaction_date.max() + pd.Timedelta(days=1)

rfm = txn.groupby("customer_id").agg(
    recency=("transaction_date", lambda x: (snapshot_date - x.max()).days),
    frequency=("transaction_id", "count"),
    monetary=("amount", "sum")
).reset_index()

rfm["r_score"] = pd.qcut(rfm.recency, 5, labels=[5,4,3,2,1]).astype(int)
rfm["f_score"] = pd.qcut(rfm.frequency.rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["m_score"] = pd.qcut(rfm.monetary, 5, labels=[1,2,3,4,5]).astype(int)
rfm["rfm_score"] = rfm.r_score.astype(str) + rfm.f_score.astype(str) + rfm.m_score.astype(str)

def segment(row):
    if row.r_score >= 4 and row.f_score >= 4 and row.m_score >= 4:
        return "Champions"
    if row.r_score >= 3 and row.f_score >= 3:
        return "Loyal"
    if row.r_score <= 2 and row.f_score <= 2:
        return "At Risk"
    if row.r_score >= 4 and row.f_score <= 2:
        return "New"
    return "Regular"

rfm["segment"] = rfm.apply(segment, axis=1)
rfm.to_csv("outputs/rfm.csv", index=False)

avg_txn = txn.groupby("customer_id").amount.mean().rename("avg_txn_value")
total_spend = txn.groupby("customer_id").amount.sum().rename("total_spend")

merged = cust.merge(rfm, on="customer_id").merge(avg_txn, on="customer_id").merge(total_spend, on="customer_id")
merged["credit_utilization"] = (merged.total_spend / merged.credit_limit).clip(upper=1)
merged["clv_simple"] = merged.avg_txn_value * merged.frequency * 2

q1 = merged.total_spend.quantile(0.25)
q3 = merged.total_spend.quantile(0.75)
iqr = q3 - q1
merged["is_outlier_spend"] = (merged.total_spend > q3 + 1.5*iqr) | (merged.total_spend < q1 - 1.5*iqr)

features = merged[["recency","frequency","monetary","avg_txn_value","credit_utilization"]]
scaled = StandardScaler().fit_transform(features)

km = KMeans(n_clusters=4, random_state=42, n_init=10)
merged["cluster"] = km.fit_predict(scaled)

cluster_names = {}
cluster_avg = merged.groupby("cluster").monetary.mean().sort_values()
labels = ["Low Value","Mid Value","High Value","Premium"]
for i, cl in enumerate(cluster_avg.index):
    cluster_names[cl] = labels[i]
merged["cluster_label"] = merged.cluster.map(cluster_names)

merged["credit_risk"] = np.where(merged.credit_utilization > 0.8, "High Risk",
                          np.where(merged.credit_utilization > 0.5, "Medium Risk", "Low Risk"))

merged.to_csv("outputs/customer_master.csv", index=False)

corr_cols = ["age","annual_income","credit_limit","recency","frequency","monetary","avg_txn_value","credit_utilization"]
corr = merged[corr_cols].corr()
corr.to_csv("outputs/correlation_matrix.csv")

print("segments:\n", rfm.segment.value_counts())
print("\nclusters:\n", merged.cluster_label.value_counts())
print("\nhigh risk customers:", (merged.credit_risk=="High Risk").sum())
print("\noutliers:", merged.is_outlier_spend.sum())

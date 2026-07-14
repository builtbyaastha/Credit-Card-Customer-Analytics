import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

n_customers = 2000
cities = ["Delhi","Mumbai","Bangalore","Chennai","Kolkata","Pune","Hyderabad","Ahmedabad","Jaipur","Lucknow"]
occupations = ["Salaried","Business Owner","Self Employed","Student","Retired"]
card_types = ["Silver","Gold","Platinum","Signature"]

customers = []
for i in range(1, n_customers+1):
    age = np.random.randint(21, 65)
    income = np.random.normal(70000, 30000)
    income = max(15000, income)
    card = np.random.choice(card_types, p=[0.35,0.35,0.2,0.1])
    limit = {"Silver":100000,"Gold":250000,"Platinum":500000,"Signature":1000000}[card]
    join_date = datetime(2019,1,1) + timedelta(days=int(np.random.randint(0, 2000)))
    customers.append({
        "customer_id": f"C{i:05d}",
        "age": age,
        "gender": np.random.choice(["M","F"], p=[0.55,0.45]),
        "city": np.random.choice(cities),
        "occupation": np.random.choice(occupations, p=[0.45,0.2,0.15,0.1,0.1]),
        "annual_income": round(income,2),
        "card_type": card,
        "credit_limit": limit,
        "join_date": join_date.strftime("%Y-%m-%d")
    })

cust_df = pd.DataFrame(customers)
cust_df.to_csv("data/customers.csv", index=False)

merchant_categories = {
    "Groceries": (200, 3000),
    "Dining": (150, 2500),
    "Fuel": (500, 4000),
    "Travel": (2000, 40000),
    "Electronics": (1000, 60000),
    "Fashion": (500, 15000),
    "Bills & Utilities": (300, 8000),
    "Healthcare": (300, 20000),
    "Entertainment": (200, 3000),
    "Online Shopping": (200, 20000)
}

merchants = []
mid = 1
for cat in merchant_categories:
    for j in range(15):
        merchants.append({"merchant_id": f"M{mid:04d}", "merchant_category": cat})
        mid += 1
merch_df = pd.DataFrame(merchants)
merch_df.to_csv("data/merchant_categories.csv", index=False)

start = datetime(2024,1,1)
end = datetime(2025,12,31)
days_range = (end-start).days

txns = []
tid = 1
for _, c in cust_df.iterrows():
    n_txn = np.random.poisson(35)
    n_txn = max(1, n_txn)
    for _ in range(n_txn):
        cat = np.random.choice(list(merchant_categories.keys()))
        low, high = merchant_categories[cat]
        amt = round(np.random.uniform(low, high), 2)
        merch_row = merch_df[merch_df.merchant_category==cat].sample(1).iloc[0]
        txn_date = start + timedelta(days=int(np.random.randint(0, days_range)))
        txns.append({
            "transaction_id": f"T{tid:07d}",
            "customer_id": c.customer_id,
            "merchant_id": merch_row.merchant_id,
            "merchant_category": cat,
            "transaction_date": txn_date.strftime("%Y-%m-%d"),
            "amount": amt
        })
        tid += 1

txn_df = pd.DataFrame(txns)
txn_df.to_csv("data/transactions.csv", index=False)

print("customers:", len(cust_df))
print("merchants:", len(merch_df))
print("transactions:", len(txn_df))

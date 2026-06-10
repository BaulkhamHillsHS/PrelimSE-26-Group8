import csv

with open("real/accounts.csv","w",newline="") as f:
    writer=csv.DictWriter(f, fieldnames=["name", "email", "password", "subscription_plan", "payment_info", "profiles"])
    writer.writeheader()
import os
import csv
from pathlib import Path

def save_to_csv(fields, data, fp):
    with open(fp, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    
def load_from_csv(fp):
    data = []
    with open(fp, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


root = Path(__file__).resolve().parent
data_path = os.path.join(root, "data.csv")

data = load_from_csv(data_path)
print(data)
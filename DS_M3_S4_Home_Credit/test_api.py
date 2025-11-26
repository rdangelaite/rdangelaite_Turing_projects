import dill
import random
import pandas as pd
import numpy as np
import requests
import json
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

df = pd.read_csv("home-credit-default-risk/application_test.csv")

# Pick one sample row
a = None
try:
    print('Pick a sample row.')
    a = int(input('Choose an integer from 0 to 48743: '))
except ValueError:
    print("Not a valid integer value...")
    print("Picking sample row randomly!")
    a = random.randint(0, 48743)
    print(f"Row index: {a}")

sample = df.iloc[[a]]

# === Prepare JSON payload ===
features = sample.to_numpy().flatten().tolist()

payload = {"features": features}

# === Send request to FastAPI endpoint ===
url = "https://fastapi-models-166989861873.europe-central2.run.app/predict/xgboost"
url2 = "https://fastapi-models-166989861873.europe-central2.run.app/predict/lightgbm"
headers = {"Content-Type": "application/json"}

print(f"\nSending request to: {url}")

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Status code: {response.status_code}")
    print("Response:", response.text)
    print(f"\nSending request to: {url2}")
    response = requests.post(url2, headers=headers, data=json.dumps(payload))
    print(f"Status code: {response.status_code}")
    print("Response:", response.text)
except Exception as e:
    print("Request failed:", e)

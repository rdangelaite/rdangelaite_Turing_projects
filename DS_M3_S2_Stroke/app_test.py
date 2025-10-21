from flask import Flask, jsonify, request
import requests

# Example
test = {
    "gender": 0,
    "age": 53.0,
    "hypertension": 1,
    "heart_disease": 0,
    "ever_married": 1,
    "Residence_type": 0,
    "avg_glucose_level": 77.94,
    "bmi": 33.0,
    "work_type_Govt_job": 0.0,
    "work_type_Private": 1.0,
    "work_type_Self-employed": 0.0,
    "work_type_children": 0.0,
    "smoking_status_formerly smoked": 0.0,
    "smoking_status_never smoked": 1.0,
    "smoking_status_smokes": 0.0,
}

# Location of my server
url = "http://127.0.0.1:8989/predict"

# Send request
resp = requests.post(url, json=test)
resp.raise_for_status()

# Print result
print(resp.json())

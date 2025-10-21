from flask import Flask, jsonify, request
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load('best_model.pkl')


@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the request
    data = request.get_json()

    # Validate the input data
    required_fields = [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "ever_married",
        "Residence_type",
        "avg_glucose_level",
        "bmi",
        "work_type_Govt_job",
        "work_type_Private",
        "work_type_Self-employed",
        "work_type_children",
        "smoking_status_formerly smoked",
        "smoking_status_never smoked",
        "smoking_status_smokes",
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields in the request data"}), 400

    preds = model.predict_proba(pd.DataFrame(data, index=[0]))[0, 1]

    # Convert the prediction result to a standard Python float
    result = {"default_proba": float(preds)}

    response = {"status": "success", "data": data, "prediction": result}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8989, debug=True)

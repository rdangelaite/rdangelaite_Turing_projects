import builtins
import pandas as pd
import duckdb as db
import numpy as np
import traceback
import json
import dill
from fastapi import FastAPI
from pydantic import BaseModel
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from app_scripts import *

bureau_balance = pd.read_csv('data/bureau_balance.csv')
bureau = pd.read_csv('data/bureau.csv')
credit_card_balance = pd.read_csv('data/credit_card_balance.csv')
installments_payments = pd.read_csv('data/installments_payments.csv')
pos_cash = pd.read_csv('data/POS_CASH_balance.csv')
previous_application = pd.read_csv('data/previous_application.csv')

builtins.np = np
builtins.pd = pd
builtins.db = db
builtins.remove_outliers_iqr = remove_outliers_iqr
builtins.OneHotEncoder = OneHotEncoder
builtins.choosing_params = choosing_params
builtins.preprocess_bureau_feat = preprocess_bureau_feat
builtins.preprocess_credit_card_balance = preprocess_credit_card_balance
builtins.preprocess_installments_payments = preprocess_installments_payments
builtins.preprocess_pos_cash = preprocess_pos_cash
builtins.preprocess_previous_application = preprocess_previous_application

builtins.bureau_balance = bureau_balance
builtins.bureau = bureau
builtins.credit_card_balance = credit_card_balance
builtins.installments_payments = installments_payments
builtins.pos_cash = pos_cash
builtins.previous_application = previous_application

app = FastAPI()

try:
    template_df = pd.read_csv('template.csv')

    with open("list_to_remove.txt", "r") as f:
        list_to_remove = [line.strip() for line in f]
    builtins.list_to_remove = list_to_remove

    with open("building_param_xgb.txt", "r") as f:
        building_param_xgb = f.read()
    builtins.building_param_xgb = building_param_xgb

    with open("building_param_lgbm.txt", "r") as f:
        building_param_lgbm = f.read()
    builtins.building_param_lgbm = building_param_lgbm

    with open("outlier_factor_xgb.txt", "r") as f:
        outlier_factor_xgb = float(f.read())
    builtins.outlier_factor_xgb = outlier_factor_xgb

    with open("outlier_factor_lgbm.txt", "r") as f:
        outlier_factor_lgbm = float(f.read())
    builtins.outlier_factor_lgbm = outlier_factor_lgbm

    with open("impute_strategy_lgbm.txt", "r") as f:
        impute_strategy_lgbm = f.read()
    builtins.impute_strategy_lgbm = impute_strategy_lgbm

    with open("feature_names.json", "r") as f:
        feature_names = json.load(f)

    # Load models
    with open("light_model.pkl", "rb") as f:
        light_model = dill.load(f)

    with open("xgb_model.pkl", "rb") as f:
        xgb_model = dill.load(f)

    print("✅ Models loaded successfully")
except Exception as e:
    print("❌ Error during model loading:", e)
    print(traceback.format_exc())


@app.get("/")
def read_root():
    return {"message": "FastAPI model API is running successfully 🚀"}


# Request schema
class InputData(BaseModel):
    features: list


@app.post("/predict/lightgbm")
def predict_light(data: InputData):
    """
    Expects "features": list in the same order as training columns.
    Example: [SK_ID_CURR, NAME_CONTRACT_TYPE, CODE_GENDER, FLAG_OWN_CAR, ...].
    """
    try:
        X = pd.DataFrame([data.features], columns=feature_names)
        sample_extended = pd.concat([X, template_df])
        prob = light_model.predict_proba(sample_extended)[0, 1]
        return {"model": "LightGBM", "probability": float(prob)}
    except Exception as e:
        print("❌ LightGBM prediction error:", e)
        print(traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/predict/xgboost")
def predict_xgb(data: InputData):
    '''
    Expects "features": list in the same order as training columns.
    Example: [SK_ID_CURR, NAME_CONTRACT_TYPE, CODE_GENDER, FLAG_OWN_CAR, ...].
    '''
    try:
        X = pd.DataFrame([data.features], columns=feature_names)
        sample_extended = pd.concat([X, template_df])
        prob = xgb_model.predict_proba(sample_extended)[0, 1]
        return {"model": "XGBoost", "probability": float(prob)}
    except Exception as e:
        import traceback

        print("❌ Prediction error:", e)
        print(traceback.format_exc())
        return {"error": str(e)}

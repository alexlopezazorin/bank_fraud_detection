"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
from .utils import is_night, time_to_cyclic_features
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ML" / "model.pkl"

model = joblib.load(MODEL_PATH)  # se carga al importar

THRESHOLD = 0.5 #0.5 is the default threshold, but it can be manually changed

def model_analyzes_transaction(Amount, Concept, Local_Time):
    
    time_sin, time_cos = time_to_cyclic_features(Local_Time)
    Is_Night = is_night(Local_Time)
    
    X = pd.DataFrame([{
        "Amount": Amount,
        "Concept": Concept,
        "time_sin": time_sin,
        "time_cos": time_cos,
        "Is_Night": Is_Night
    }])
    
    p_fraud = model.predict_proba(X)[0, 1]
    
    if p_fraud >= THRESHOLD:
        is_fraud = 1
    else:
        is_fraud = 0
    
    return p_fraud, is_fraud

    

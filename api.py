"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import time
from bank_system.analyst import Analyst
from bank_system.bank import Bank

app = FastAPI(title="Bank Fraud Detection API", description="API for predicting fraudulent bank transactions", version="1.0.0")

analyst = Analyst()
bank = Bank(analyst)


class TransactionRequest(BaseModel):
    amount: float
    concept: str
    local_time: str 


class TransactionResponse(BaseModel):
    is_fraud: int
    p_fraud: float


@app.post("/predict", response_model=TransactionResponse)

def predict_transaction(data: TransactionRequest):
    # Convertimos la hora
    h, m, s = map(int, data.local_time.split(":"))
    local_time = time(hour=h, minute=m, second=s)
    
    p_fraud, is_fraud = analyst.model_predict_only(data.amount, data.concept, local_time)
    return {"is_fraud": is_fraud, "p_fraud": p_fraud}



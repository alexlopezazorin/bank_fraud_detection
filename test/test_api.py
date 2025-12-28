"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
from fastapi.testclient import TestClient
from api import app

class Test_API():

    def test_predict_safe_transaction(self):
        
        client = TestClient(app)
        response = client.post("/predict", json={
            "amount": 1000,
            "concept": "grocery shopping",
            "local_time": "14:30:00"
        })
        assert response.status_code == 200
        data = response.json()
        assert "is_fraud" in data
        assert "p_fraud" in data

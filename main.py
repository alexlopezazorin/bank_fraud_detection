"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import requests

def run_demo():

    data = {
        "amount": 51000,
        "concept": "urgent crypto investment",
        "local_time": "22:30:00"
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)
    print(response.json())

if __name__ == "__main__":
    run_demo()

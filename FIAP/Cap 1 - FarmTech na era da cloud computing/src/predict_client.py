import requests

API_URL = "http://localhost:5000/predict"
sample = {
    "features": {
        "precipitacao": 2.5,
        "umidade_especifica_a_2_m": 7.2,
        "umidade_relativa_a_2_m": 65.0,
        "temperatura_a_2_m": 24.5,
    }
}

r = requests.post(API_URL, json=sample)
print(r.status_code, r.json())

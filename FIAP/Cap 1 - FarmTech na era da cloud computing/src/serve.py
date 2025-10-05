from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = os.getenv("MODEL_PATH", "../models/rf_model.joblib")
SCALER_PATH = os.getenv("SCALER_PATH", "../models/scaler.joblib")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.json
    try:
        features = payload.get("features")

        x = np.array(list(features.values())).reshape(1, -1)
        x_scaled = scaler.transform(x)
        pred = model.predict(x_scaled)
        return jsonify({"prediction_ton_per_ha": float(pred[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

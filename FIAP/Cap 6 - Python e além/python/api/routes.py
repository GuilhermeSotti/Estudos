from flask import Blueprint, request, jsonify
from .schemas import YieldRequest, LossRequest
from modeling.yield_prediction import predict_yield
from modeling.harvest_loss import predict_harvest_loss

bp = Blueprint("api", __name__, url_prefix="/api/v1")

@bp.route("/predict/yield", methods=["POST"])
def predict_yield_route():
    body = YieldRequest(**request.json)
    # converter lista em DataFrame de 1 linha
    import pandas as pd
    df = pd.DataFrame([body.features])
    preds = predict_yield("artefacts/yield_model.pkl", df)
    return jsonify({"predictions": preds.tolist()})

@bp.route("/predict/loss", methods=["POST"])
def predict_loss_route():
    body = LossRequest(**request.json)
    import pandas as pd
    df = pd.DataFrame([body.features])
    probs = predict_harvest_loss("artefacts/loss_model.pkl", df)
    return jsonify({"loss_risk": probs.tolist()})

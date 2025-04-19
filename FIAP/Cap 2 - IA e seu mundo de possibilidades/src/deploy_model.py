import os
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

from utils import get_logger

app = Flask(__name__)
logger = get_logger()

MODEL_PATH = os.environ.get("MODEL_PATH", "models/modelo_utensilios.h5")
model = load_model(MODEL_PATH)
IMG_SIZE = (224, 224)
CLASSES = ['talheres', 'panelas', 'utensilios_preparo']

def preprocess_image(image, target_size):
    """
    Pré-processa a imagem para ser compatível com o modelo.
    """
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400
    file = request.files["file"]
    try:
        image = Image.open(file.stream)
        processed_image = preprocess_image(image, IMG_SIZE)
        predictions = model.predict(processed_image)
        predicted_index = int(np.argmax(predictions, axis=1)[0])
        confidence = float(np.max(predictions))
        label = CLASSES[predicted_index]
        response = {"label": label, "confidence": confidence}
        return jsonify(response)
    except Exception as e:
        logger.error(f"Erro ao processar a imagem: {e}")
        return jsonify({"error": "Erro ao processar a imagem."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

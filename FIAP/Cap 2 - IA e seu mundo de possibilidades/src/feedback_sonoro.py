import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from gtts import gTTS
import playsound

def predict_and_feedback(image_path, model_path="models/modelo_utensilios.h5",
                         img_size=(224, 224), classes=['talheres', 'panelas', 'utensilios_preparo']):
    """
    Carrega o modelo, realiza a predição em uma imagem e fornece feedback sonoro usando gTTS.
    
    :param image_path: Caminho para a imagem de teste.
    :param model_path: Caminho para o modelo salvo.
    :param img_size: Tamanho alvo para redimensionamento.
    :param classes: Lista de classes.
    :return: rótulo predito e confiança.
    """
    model = load_model(model_path)
    img = image.load_img(image_path, target_size=img_size)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    predicted_index = int(np.argmax(predictions, axis=1)[0])
    confidence = float(np.max(predictions))
    label = classes[predicted_index]
    
    message = f"Utensílio detectado: {label} com {confidence*100:.1f} por cento de confiança."
    print(message)
    
    # Converte o texto em áudio e reproduz
    tts = gTTS(message, lang='pt')
    audio_file = "feedback.mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    
    return label, confidence

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python feedback_sonoro.py caminho/para/imagem.jpg")
    else:
        image_path = sys.argv[1]
        label, conf = predict_and_feedback(image_path)
        print(f"Predição: {label} com {conf*100:.1f}% de confiança")

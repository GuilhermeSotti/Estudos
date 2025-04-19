import os
import argparse
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

from data_preprocessing import get_data_generators
from utils import get_logger

def build_model(input_shape, num_classes):
    """
    Constrói uma arquitetura CNN simples.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    return model

def train(args):
    logger = get_logger()

    train_dir = args.train_dir
    test_dir = args.test_dir
    img_size = (args.img_width, args.img_height)
    batch_size = args.batch_size
    epochs = args.epochs
    learning_rate = args.learning_rate
    classes = args.classes.split(',') if args.classes else None

    logger.info("Criando geradores de dados...")
    train_gen, test_gen = get_data_generators(train_dir, test_dir, img_size, batch_size, classes)
    
    input_shape = (args.img_width, args.img_height, 3)
    num_classes = len(classes) if classes else train_gen.num_classes
    model = build_model(input_shape, num_classes)
    
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
    logger.info("Iniciando treinamento...")
    history = model.fit(train_gen, epochs=epochs, validation_data=test_gen)
    
    model_dir = args.model_dir
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "modelo_utensilios.h5")
    model.save(model_path)
    logger.info(f"Modelo salvo em: {model_path}")
    
    history_path = os.path.join(model_dir, "history.npy")
    import numpy as np
    np.save(history_path, history.history)
    logger.info(f"Histórico de treinamento salvo em: {history_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Treinamento do modelo de utensílios de cozinha")
    parser.add_argument('--train_dir', type=str, default='data/train', help='Diretório dos dados de treinamento')
    parser.add_argument('--test_dir', type=str, default='data/test', help='Diretório dos dados de teste')
    parser.add_argument('--img_width', type=int, default=224, help='Largura da imagem')
    parser.add_argument('--img_height', type=int, default=224, help='Altura da imagem')
    parser.add_argument('--batch_size', type=int, default=32, help='Tamanho do batch')
    parser.add_argument('--epochs', type=int, default=20, help='Número de épocas')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Taxa de aprendizado')
    parser.add_argument('--classes', type=str, default='talheres,panelas,utensilios_preparo', help='Classes separadas por vírgula')
    parser.add_argument('--model_dir', type=str, default='models', help='Diretório para salvar o modelo')
    args = parser.parse_args()
    train(args)

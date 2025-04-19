import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model

from data_preprocessing import get_test_generator
from utils import get_logger
from fpdf import FPDF
from datetime import datetime

def generate_evaluation_report(model_path, test_dir, img_size, batch_size, classes, output_pdf):
    logger = get_logger()
    
    # Carrega o gerador de teste
    test_gen = get_test_generator(test_dir, img_size, batch_size, classes)
    
    # Carrega o modelo treinado
    model = load_model(model_path)
    
    # Avaliação no conjunto de teste
    loss, accuracy = model.evaluate(test_gen)
    
    # Previsões e métricas de avaliação
    test_gen.reset()
    predictions = model.predict(test_gen)
    predicted_classes = predictions.argmax(axis=1)
    true_classes = test_gen.classes
    
    report_text = classification_report(true_classes, predicted_classes, target_names=classes)
    
    cm = confusion_matrix(true_classes, predicted_classes)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Matriz de Confusão')
    plt.xlabel('Classe Predita')
    plt.ylabel('Classe Verdadeira')
    cm_plot_path = 'cm_plot.png'
    plt.savefig(cm_plot_path)
    plt.close()
    
    history_path = os.path.join(os.path.dirname(model_path), "history.npy")
    acc_plot_path = None
    loss_plot_path = None
    if os.path.exists(history_path):
        history = np.load(history_path, allow_pickle=True).item()
        plt.figure(figsize=(8, 4))
        plt.plot(history['accuracy'], label='Acurácia Treino')
        plt.plot(history['val_accuracy'], label='Acurácia Validação')
        plt.title('Acurácia durante o Treinamento')
        plt.xlabel('Época')
        plt.ylabel('Acurácia')
        plt.legend()
        acc_plot_path = 'acc_plot.png'
        plt.savefig(acc_plot_path)
        plt.close()
        
        # Gráfico de perda
        plt.figure(figsize=(8, 4))
        plt.plot(history['loss'], label='Perda Treino')
        plt.plot(history['val_loss'], label='Perda Validação')
        plt.title('Perda durante o Treinamento')
        plt.xlabel('Época')
        plt.ylabel('Perda')
        plt.legend()
        loss_plot_path = 'loss_plot.png'
        plt.savefig(loss_plot_path)
        plt.close()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relatório de Avaliação do Modelo", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Acurácia no conjunto de teste: {accuracy*100:.2f}%\n\n")
    pdf.multi_cell(0, 10, report_text)
    
    pdf.ln(10)
    if acc_plot_path:
        pdf.image(acc_plot_path, w=pdf.epw)
        pdf.ln(5)
    if loss_plot_path:
        pdf.image(loss_plot_path, w=pdf.epw)
        pdf.ln(5)
    pdf.image(cm_plot_path, w=pdf.epw)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
    
    pdf.output(output_pdf)
    logger.info(f"Relatório PDF gerado: {output_pdf}")
    
def main():
    parser = argparse.ArgumentParser(description="Avaliação do modelo de utensílios de cozinha")
    parser.add_argument('--model_path', type=str, default='models/modelo_utensilios.h5', help='Caminho do modelo salvo')
    parser.add_argument('--test_dir', type=str, default='data/test', help='Diretório dos dados de teste')
    parser.add_argument('--img_width', type=int, default=224, help='Largura da imagem')
    parser.add_argument('--img_height', type=int, default=224, help='Altura da imagem')
    parser.add_argument('--batch_size', type=int, default=32, help='Tamanho do batch')
    parser.add_argument('--classes', type=str, default='talheres,panelas,utensilios_preparo', help='Classes separadas por vírgula')
    parser.add_argument('--output_pdf', type=str, default='reports/Relatorio_Modelo.pdf', help='Caminho de saída para o relatório PDF')
    args = parser.parse_args()
    
    classes = args.classes.split(',')
    img_size = (args.img_width, args.img_height)
    os.makedirs(os.path.dirname(args.output_pdf), exist_ok=True)
    generate_evaluation_report(args.model_path, args.test_dir, img_size, args.batch_size, classes, args.output_pdf)

if __name__ == '__main__':
    main()

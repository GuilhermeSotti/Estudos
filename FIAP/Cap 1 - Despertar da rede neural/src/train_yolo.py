"""
Treina YOLO (via pacote ultralytics) usando dataset/data.yaml local.
Gera duas execuções: 30 e 60 epochs e salva em results/yolo/
Requisitos: 'ultralytics' instalado (pip install ultralytics)
Uso:
    python src/train_yolo.py --epochs1 30 --epochs2 60 --img 640 --batch 8
"""
import argparse
from pathlib import Path
from ultralytics import YOLO

BASE = Path(__file__).resolve().parents[1]
DATA_YAML = BASE / "dataset" / "data.yaml"
RESULTS_DIR = BASE / "results" / "yolo"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def run_training(epochs, name, imgsz=640, batch=8, weights="yolov8n.pt"):
    print(f"[YOLO] Treinando {name}: epochs={epochs}, img={imgsz}, batch={batch}, weights={weights}")
    model = YOLO(weights)

    model.train(data=str(DATA_YAML), epochs=epochs, imgsz=imgsz, batch=batch, project=str(RESULTS_DIR), name=name)
    print(f"[YOLO] Finalizado {name}")

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs1", type=int, default=30)
    p.add_argument("--epochs2", type=int, default=60)
    p.add_argument("--img", type=int, default=640)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--weights", type=str, default="yolov8n.pt")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run_training(args.epochs1, name=f"yolo_exp_{args.epochs1}", imgsz=args.img, batch=args.batch, weights=args.weights)
    run_training(args.epochs2, name=f"yolo_exp_{args.epochs2}", imgsz=args.img, batch=args.batch, weights=args.weights)
    print("✅ Treinos YOLO concluídos. Ver resultados em:", RESULTS_DIR)

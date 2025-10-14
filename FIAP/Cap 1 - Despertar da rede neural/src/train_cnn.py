"""
Treina uma CNN do zero para classificação (vaca vs cerca) usando imagens
em dataset/train, dataset/val, dataset/test.

Salva resultados em results/cnn/
"""
import random
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms, datasets
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

BASE = Path(__file__).resolve().parents[1]
DATA_ROOT = BASE / "dataset"
RESULTS_DIR = BASE / "results" / "cnn"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

class SimpleCNN(nn.Module):
    def __init__(self, n_classes=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(inplace=True), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(inplace=True), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(inplace=True), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.BatchNorm2d(256), nn.ReLU(inplace=True), nn.AdaptiveAvgPool2d((4,4))
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256*4*4, 512), nn.ReLU(inplace=True), nn.Dropout(0.5),
            nn.Linear(512, n_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

IMG_SIZE = 224
BATCH = 16
EPOCHS = 30
LR = 1e-4

train_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE,IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(0.08,0.08,0.08,0.02),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])
val_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE,IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

train_ds = datasets.ImageFolder(DATA_ROOT / "train", transform=train_tf)
val_ds = datasets.ImageFolder(DATA_ROOT / "val", transform=val_tf)
test_ds = datasets.ImageFolder(DATA_ROOT / "test", transform=val_tf)

train_loader = DataLoader(train_ds, batch_size=BATCH, shuffle=True, num_workers=2)
val_loader = DataLoader(val_ds, batch_size=BATCH, shuffle=False, num_workers=2)
test_loader = DataLoader(test_ds, batch_size=1, shuffle=False, num_workers=2)

def train_model(model, epochs=EPOCHS, lr=LR):
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_val = 0.0
    history = []
    for ep in range(1, epochs+1):
        t0 = time.time()
        model.train()
        running_loss = 0.0; correct=0; total=0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            out = model(imgs)
            loss = criterion(out, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()*imgs.size(0)
            _, preds = out.max(1)
            correct += (preds==labels).sum().item()
            total += labels.size(0)
        train_loss = running_loss/total
        train_acc = correct/total

        model.eval()
        v_loss = 0.0; v_corr = 0; v_tot = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                out = model(imgs)
                loss = criterion(out, labels)
                v_loss += loss.item()*imgs.size(0)
                _, preds = out.max(1)
                v_corr += (preds==labels).sum().item()
                v_tot += labels.size(0)
        val_loss = v_loss / v_tot if v_tot else 0
        val_acc = v_corr / v_tot if v_tot else 0
        elapsed = time.time() - t0
        history.append((ep, train_loss, val_loss, train_acc, val_acc, elapsed))
        print(f"Epoch {ep}/{epochs} - tr_loss {train_loss:.4f} val_loss {val_loss:.4f} tr_acc {train_acc:.4f} val_acc {val_acc:.4f} time {elapsed:.1f}s")

        torch.save({'epoch':ep,'model_state':model.state_dict(),'optimizer':optimizer.state_dict()}, RESULTS_DIR / f"ckpt_ep{ep}.pth")
        if val_acc > best_val:
            best_val = val_acc
            torch.save(model.state_dict(), RESULTS_DIR / "best_model.pth")
    df = pd.DataFrame(history, columns=['epoch','train_loss','val_loss','train_acc','val_acc','epoch_time_s'])
    df.to_csv(RESULTS_DIR / "cnn_metrics.csv", index=False)
    return model, df

def main():
    model = SimpleCNN(n_classes=len(train_ds.classes))
    model, df = train_model(model, epochs=EPOCHS, lr=LR)
    print("Treino finalizado. Métricas salvas em", RESULTS_DIR)

if __name__ == "__main__":
    main()

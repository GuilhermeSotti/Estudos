#!/usr/bin/env python3
"""
Treino de CNN do zero (classificador binário)
- Salva checkpoints em results/cnn/
- Metrics saved to results/cnn_metrics.csv
"""
import os
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

# Reprodutibilidade
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

ROOT = Path("/content/drive/MyDrive/FarmTech_Fase6/Cap1_Despertar_RedeNeural/dataset")
RESULTS_DIR = Path("/content/drive/MyDrive/FarmTech_Fase6/Cap1_Despertar_RedeNeural/results/cnn")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------- Arquitetura ----------
class SimpleCNN(nn.Module):
    def __init__(self, n_classes=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # -> 32 x H x W
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # -> 32 x H/2 x W/2

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # -> 64 x H/4 x W/4

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),  # -> 128 x H/8 x W/8

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4,4))
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256*4*4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, n_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# ---------- Datasets ----------
IMG_SIZE = 224
batch_size = 16
train_transforms = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(0.1,0.1,0.1,0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])
val_transforms = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

train_dataset = datasets.ImageFolder(ROOT / "train", transform=train_transforms)
val_dataset = datasets.ImageFolder(ROOT / "val", transform=val_transforms)
test_dataset = datasets.ImageFolder(ROOT / "test", transform=val_transforms)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers=2)

# ---------- Treino ----------
def train(model, epochs=20, lr=1e-4):
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_val_acc = 0.0
    history = []
    for epoch in range(1, epochs+1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        t0 = time.time()
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * imgs.size(0)
            _, preds = outputs.max(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
        train_loss = running_loss / total
        train_acc = correct / total

        # validação
        model.eval()
        v_loss = 0.0
        v_correct = 0
        v_total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                loss = criterion(outputs, labels)
                v_loss += loss.item() * imgs.size(0)
                _, preds = outputs.max(1)
                v_correct += (preds == labels).sum().item()
                v_total += labels.size(0)
        val_loss = v_loss / v_total
        val_acc = v_correct / v_total

        elapsed = time.time() - t0
        history.append((epoch, train_loss, val_loss, train_acc, val_acc, elapsed))
        print(f"Epoch {epoch}/{epochs} - train_loss {train_loss:.4f} val_loss {val_loss:.4f} train_acc {train_acc:.4f} val_acc {val_acc:.4f} time {elapsed:.1f}s")

        # salvar checkpoint
        torch.save({'epoch': epoch, 'model_state': model.state_dict(), 'optimizer_state': optimizer.state_dict()},
                   RESULTS_DIR / f"checkpoint_epoch_{epoch}.pth")
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), RESULTS_DIR / "best_model.pth")
    # salvar histórico
    df = pd.DataFrame(history, columns=['epoch','train_loss','val_loss','train_acc','val_acc','epoch_time_s'])
    df.to_csv(RESULTS_DIR / "cnn_metrics.csv", index=False)
    return model, df

if __name__ == "__main__":
    model = SimpleCNN(n_classes=2)
    model, df = train(model, epochs=30, lr=1e-4)
    print("Treino finalizado. Métricas salvas em:", RESULTS_DIR)

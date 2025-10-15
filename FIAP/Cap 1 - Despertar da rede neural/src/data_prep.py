"""
data_prep.py
- Organiza imagens em train/val/test splits
- Gera data.yaml para YOLO
Seed fixada para reprodutibilidade.
"""
import os
import random
import shutil
from pathlib import Path

SEED = 42
random.seed(SEED)

ROOT_DRIVE = Path("/content/drive/MyDrive/FarmTech_Fase6/Cap1_Despertar_RedeNeural/dataset")
SOURCE_DIR = Path("/content/source_images")
CLASSES = {"vaca": "vaca", "cerca": "cerca"}

def create_structure(root: Path):
    for split in ["train", "val", "test"]:
        for cls in CLASSES:
            (root / split / cls).mkdir(parents=True, exist_ok=True)

def split_copy(source_dir: Path, root: Path, per_class=40, train_n=32, val_n=4, test_n=4):
    assert train_n + val_n + test_n == per_class
    for cls in CLASSES:
        src_cls_dir = source_dir / cls
        imgs = list(src_cls_dir.glob("*.*"))
        if len(imgs) < per_class:
            raise ValueError(f"Faltam imagens na classe {cls}: {len(imgs)} encontrados, {per_class} requeridos")
        imgs = imgs[:per_class]
        random.shuffle(imgs)
        train = imgs[:train_n]
        val = imgs[train_n:train_n+val_n]
        test = imgs[train_n+val_n:train_n+val_n+test_n]
        for p in train:
            shutil.copy(p, root / "train" / cls / p.name)
        for p in val:
            shutil.copy(p, root / "val" / cls / p.name)
        for p in test:
            shutil.copy(p, root / "test" / cls / p.name)

def write_data_yaml(root: Path, out_path: Path):
    data = {
        'train': str(root / 'train'),
        'val': str(root / 'val'),
        'test': str(root / 'test'),
        'nc': len(CLASSES),
        'names': list(CLASSES.keys())
    }
    import yaml
    with open(out_path, 'w') as f:
        yaml.dump(data, f)

if __name__ == "__main__":
    create_structure(ROOT_DRIVE)
    split_copy(Path("/content/source_images"), ROOT_DRIVE, per_class=40, train_n=32, val_n=4, test_n=4)
    write_data_yaml(ROOT_DRIVE, ROOT_DRIVE.parent / "data.yaml")
    print("Dataset organizado em:", ROOT_DRIVE)

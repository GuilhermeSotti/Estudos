"""
Extrai ZIPs locais, valida imagens, copia até MAX_IMAGES por classe,
gera splits train/val/test (32/4/4 por classe) e escreve dataset/data.yaml.

Coloque seus zips em: dataset/raw/
 - cows.zip  -> será usado como 'vaca'
 - fences.zip -> será usado como 'cerca'

Uso:
    python src/prepare_dataset_from_zips.py
"""
import random
import zipfile
import shutil
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
RAW_DIR = BASE / "dataset" / "raw"
SRC_DIR = BASE / "dataset" / "source_images"
DATASET_DIR = BASE / "dataset"
MAX_IMAGES = 40 
SPLIT_COUNTS = {"train": 32, "val": 4, "test": 4}
SEED = 42

ZIP_MAP = {
    "vaca": "cows.zip",
    "cerca": "fences.zip"
}

def extract_zip_to_temp(zip_path: Path, temp_dir: Path):
    temp_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)

def find_images(root: Path):
    exts = (".jpg", ".jpeg", ".png", ".webp")
    return [p for p in root.rglob("*") if p.suffix.lower() in exts]

def is_valid_image(p: Path):
    try:
        with Image.open(p) as im:
            im.verify()
        return True
    except Exception:
        return False

def prepare_class(class_key: str, zip_name: str):
    print(f"--- Preparando classe '{class_key}' a partir de {zip_name} ---")
    zip_path = RAW_DIR / zip_name
    if not zip_path.exists():
        print(f"[ERRO] zip não encontrado: {zip_path}. Pule essa classe.")
        return 0

    temp_dir = DATASET_DIR / f"_tmp_{class_key}"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    extract_zip_to_temp(zip_path, temp_dir)
    images = find_images(temp_dir)
    print(f"Encontradas {len(images)} imagens brutas em {zip_name}")

    valid = [p for p in images if is_valid_image(p)]
    print(f"Imagens válidas: {len(valid)}")

    valid = valid[:MAX_IMAGES]
    out_src_class = SRC_DIR / class_key
    if out_src_class.exists():
        shutil.rmtree(out_src_class)
    out_src_class.mkdir(parents=True, exist_ok=True)

    for i, p in enumerate(valid, start=1):
        dest = out_src_class / f"{class_key}_{i:03d}{p.suffix.lower()}"
        shutil.copy(p, dest)

    print(f"Copiados {len(valid)} imagens para {out_src_class}")
    shutil.rmtree(temp_dir, ignore_errors=True)
    return len(valid)

def create_splits_and_yaml(class_keys):
    random.seed(SEED)

    for split in SPLIT_COUNTS:
        for cls in class_keys:
            dirpath = DATASET_DIR / split / f"class_{cls}"
            dirpath.mkdir(parents=True, exist_ok=True)

    summary = {}
    for cls in class_keys:
        src_cls_dir = SRC_DIR / cls
        imgs = sorted([p for p in src_cls_dir.glob("*.*")])
        if len(imgs) < sum(SPLIT_COUNTS.values()):
            print(f"[AVISO] Classe {cls} tem {len(imgs)} imagens — requeridas {sum(SPLIT_COUNTS.values())}. Ajuste MAX_IMAGES ou adicione imagens.")
        random.shuffle(imgs)
        idx = 0
        for split, n in SPLIT_COUNTS.items():
            sel = imgs[idx: idx + n]
            idx += n
            dst_dir = DATASET_DIR / split / f"class_{cls}"
            for p in sel:
                shutil.copy(p, dst_dir / p.name)
            print(f"{cls} -> {split}: {len(sel)}")
        summary[cls] = len(imgs)

    data_yaml = DATASET_DIR / "data.yaml"
    names = list(class_keys)
    yaml_text = f"train: {str((DATASET_DIR / 'train').as_posix())}\nval: {str((DATASET_DIR / 'val').as_posix())}\ntest: {str((DATASET_DIR / 'test').as_posix())}\n\nnc: {len(names)}\nnames: {names}\n"
    data_yaml.write_text(yaml_text)
    print(f"data.yaml escrito em {data_yaml}")
    return summary

if __name__ == "__main__":
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    print("Iniciando preparação do dataset (extração -> validação -> cópia)...")
    counts = {}
    for cls_key, zip_name in ZIP_MAP.items():
        counts[cls_key] = prepare_class(cls_key, zip_name)
    print("Resumo das cópias:", counts)
    print("Criando splits (train/val/test) e data.yaml...")
    summary = create_splits_and_yaml(list(ZIP_MAP.keys()))
    print("Resumo final:", summary)
    print("✅ prepare_dataset_from_zips concluído.")

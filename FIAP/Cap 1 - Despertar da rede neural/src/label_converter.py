#!/usr/bin/env python3
"""
label_converter.py
- Valida e converte labels para formato YOLO (se necessário).
- Checa se bbox está normalizado entre 0 e 1.
"""
import os
from pathlib import Path

def check_yolo_label(lbl_path: Path, img_w: int, img_h: int):
    lines = []
    with open(lbl_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                raise ValueError(f"Formato inválido em {lbl_path}: {line}")
            cls, xc, yc, w, h = map(float, parts)
            if not (0 <= xc <= 1 and 0 <= yc <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                raise ValueError(f"Valores não-normalizados em {lbl_path}")
            lines.append(line)
    return lines

if __name__ == "__main__":
    print("Uso: chame este script para validar labels em train/labels/")

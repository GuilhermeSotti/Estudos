"""
eval_metrics.py
- Avalia classificadores (CNN) e gera CSV com precision/recall/f1/matriz_confusao
- Para detecção: utiliza pycocotools para calcular mAP@0.5 (necessita anotações COCO ou conversão)
"""
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix, accuracy_score

def evaluate_classification(y_true, y_pred, labels):
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels, average=None)
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    df = pd.DataFrame({
        'label': labels,
        'precision': p,
        'recall': r,
        'f1': f1
    })
    return df, acc, cm

if __name__ == "__main__":
    y_true = [0,0,1,1,0,1]
    y_pred = [0,1,1,1,0,1]
    df, acc, cm = evaluate_classification(y_true, y_pred, labels=[0,1])
    print(df)
    print("acc", acc)
    print("conf matrix:\n", cm)

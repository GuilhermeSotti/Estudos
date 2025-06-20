import logging
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report, roc_auc_score)

logger = logging.getLogger(__name__)

def evaluate_model(model, X_test, y_test, class_names: list[str], output_dir: str, prefix: str = "eval"):
    os.makedirs(output_dir, exist_ok=True)
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)
    report_path = os.path.join(output_dir, f"{prefix}_classification_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    logger.info(f"Classification report salvo em {report_path}")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(len(class_names)), yticks=np.arange(len(class_names)),
           xticklabels=class_names, yticklabels=class_names,
           ylabel='True label', xlabel='Predicted label',
           title='Matriz de Confusão')
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    cm_path = os.path.join(output_dir, f"{prefix}_confusion_matrix.png")
    fig.savefig(cm_path)
    plt.close(fig)
    logger.info(f"Matriz de confusão salva em {cm_path}")
    metrics_summary = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision_macro": precision_score(y_test, y_pred, average='macro'),
        "recall_macro": recall_score(y_test, y_pred, average='macro'),
        "f1_macro": f1_score(y_test, y_pred, average='macro')
    }
    if hasattr(model, "predict_proba"):
        try:
            y_prob = model.predict_proba(X_test)
            from sklearn.preprocessing import label_binarize
            y_test_bin = label_binarize(y_test, classes=range(len(class_names)))
            aucs = []
            for i in range(len(class_names)):
                aucs.append(roc_auc_score(y_test_bin[:, i], y_prob[:, i]))
            metrics_summary["roc_auc_ovr_macro"] = float(np.mean(aucs))
        except Exception:
            pass



    metrics_path = os.path.join(output_dir, f"{prefix}_metrics_summary.json")
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_summary, f, indent=4)
    logger.info(f"Métricas resumo salvas em {metrics_path}")
    return report, metrics_summary, cm_path

import shap
import os
import logging
import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)

def explain_with_shap(model, X_train: pd.DataFrame, X_test: pd.DataFrame, output_dir: str, feature_names: list[str]):
    os.makedirs(output_dir, exist_ok=True)
    try:
        explainer = shap.Explainer(model, X_train)
        shap_values = explainer(X_test)
        fig = shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
        fig_path = os.path.join(output_dir, "shap_summary.png")
        plt.savefig(fig_path, bbox_inches='tight')
        plt.close()
        logger.info(f"SHAP summary plot salvo em {fig_path}")
    except Exception as e:
        logger.error(f"Erro em SHAP explainability: {e}")

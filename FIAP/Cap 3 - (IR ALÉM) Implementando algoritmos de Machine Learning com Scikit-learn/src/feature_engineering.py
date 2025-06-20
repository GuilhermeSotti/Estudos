import numpy as np
import pandas as pd
import logging
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import joblib
import os

logger = logging.getLogger(__name__)

def calc_compactness(df: pd.DataFrame, area_col: str = "area", perim_col: str = "perimeter", out_col: str = "compactness_calc") -> pd.DataFrame:
    df2 = df.copy()
    mask = df2[perim_col] > 0
    df2.loc[mask, out_col] = 4 * np.pi * df2.loc[mask, area_col] / (df2.loc[mask, perim_col] ** 2)
    df2.loc[~mask, out_col] = np.nan
    logger.info("Compacidade calculada")
    return df2

def calc_ratio_length_width(df: pd.DataFrame, length_col: str = "length", width_col: str = "width", out_col: str = "ratio_length_width") -> pd.DataFrame:
    df2 = df.copy()
    df2[out_col] = df2[length_col] / df2[width_col].replace({0: np.nan})
    logger.info("Ratio length/width calculado")
    return df2

def apply_pca(X: pd.DataFrame, n_components: int, save_dir: str | None = None):
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X)
    df_pca = pd.DataFrame(X_pca, columns=[f"pca{i+1}" for i in range(n_components)], index=X.index)
    logger.info(f"PCA aplicado: {n_components} componentes, variância explicada total {pca.explained_variance_ratio_.sum():.3f}")
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        joblib.dump(pca, os.path.join(save_dir, "pca.joblib"))
        logger.info(f"PCA salvo em {save_dir}")
    return df_pca, pca

def apply_lda(X: pd.DataFrame, y: pd.Series, n_components: int, save_dir: str | None = None):
    lda = LDA(n_components=n_components)
    X_lda = lda.fit_transform(X, y)
    df_lda = pd.DataFrame(X_lda, columns=[f"lda{i+1}" for i in range(n_components)], index=X.index)
    logger.info(f"LDA aplicado: {n_components} componentes")
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        joblib.dump(lda, os.path.join(save_dir, "lda.joblib"))
        logger.info(f"LDA salvo em {save_dir}")
    return df_lda, lda

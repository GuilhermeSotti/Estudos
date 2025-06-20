import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate, StratifiedKFold
from typing import Dict, Any

logger = logging.getLogger(__name__)

def get_model_instance(model_type: str, params: Dict[str, Any], random_state: int = 42):
    """
    Retorna instância de modelo sklearn conforme tipo e params.
    """
    if model_type.lower() == "knn":
        return KNeighborsClassifier(**params)
    elif model_type.lower() == "svm":
        return SVC(**params, probability=True, random_state=random_state)
    elif model_type.lower() == "rf":
        return RandomForestClassifier(**params, random_state=random_state)
    elif model_type.lower() == "naive_bayes":
        return GaussianNB(**params)
    elif model_type.lower() == "logistic_regression":
        return LogisticRegression(**params, random_state=random_state, max_iter=1000)
    else:
        raise ValueError(f"Tipo de modelo desconhecido: {model_type}")

def build_pipeline(model_type: str, params: Dict[str, Any], scaler: bool = True, random_state: int = 42):
    steps = []
    if scaler:
        steps.append(("scaler", StandardScaler()))
    model = get_model_instance(model_type, params, random_state=random_state)
    steps.append(("clf", model))
    pipeline = Pipeline(steps)
    logger.debug(f"Pipeline montado para {model_type}, scaler={scaler}, params={params}")
    return pipeline

def cross_validate_model(pipe, X, y, cv_n_splits: int, cv_shuffle: bool, random_state: int, scoring: list[str]):
    cv = StratifiedKFold(n_splits=cv_n_splits, shuffle=cv_shuffle, random_state=random_state)
    scores = cross_validate(pipe, X, y, cv=cv, scoring=scoring, return_train_score=False)
    logger.info(f"Cross-val completed for pipeline: mean scores: " +
                ", ".join([f"{k}: {v.mean():.3f}" for k,v in scores.items() if k.startswith("test_")]))
    return scores

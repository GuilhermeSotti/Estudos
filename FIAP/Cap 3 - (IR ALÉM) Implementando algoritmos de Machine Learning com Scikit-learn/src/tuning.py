import logging
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from typing import Dict

logger = logging.getLogger(__name__)

def tune_model(pipe, param_grid: Dict[str, list], X, y, cv, scoring: list[str], method: str = "grid", n_iter: int = 10):
    """
    Retorna objeto GridSearchCV/RandomizedSearchCV já ajustado em X,y.
    """
    if method == "grid":
        search = GridSearchCV(pipe, param_grid, cv=cv, scoring=scoring[0], refit=scoring[0], return_train_score=True)
    elif method == "random":
        search = RandomizedSearchCV(pipe, param_grid, cv=cv, scoring=scoring[0], n_iter=n_iter, random_state=42, return_train_score=True)
    else:
        raise NotImplementedError("Otimização bayesiana não implementada, usar grid ou random")
    logger.info(f"Iniciando {method} search com params: {param_grid}")
    search.fit(X, y)
    logger.info(f"Melhores parâmetros: {search.best_params_}, melhor {scoring[0]}: {search.best_score_:.3f}")
    return search

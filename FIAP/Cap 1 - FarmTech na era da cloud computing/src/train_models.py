import os
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
import joblib
import pandas as pd
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

from src.data_processing import load_data, basic_cleaning, feature_engineering, prepare_train_test

def train_and_save():
    df = load_data("../data/crop_yield.csv")
    df = basic_cleaning(df)
    df = feature_engineering(df)

    X_train, X_test, y_train, y_test = prepare_train_test(df, target='rendimento')

    models = {
        "linear": LinearRegression(),
        "dt": DecisionTreeRegressor(random_state=42),
        "rf": RandomForestRegressor(n_estimators=200, random_state=42),
        "xgb": XGBRegressor(n_estimators=200, random_state=42, verbosity=0),
        "svr": SVR(kernel='rbf', C=1.0, epsilon=0.2)
    }

    results = []
    for name, model in models.items():
        print(f"Treinando {name}...")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = root_mean_squared_error(y_test, preds)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        print(f"{name} RMSE={rmse:.3f} MAE={mae:.3f} R2={r2:.3f}")
        joblib.dump(model, f"models/{name}_model.joblib")
        results.append({"model": name, "rmse": rmse, "mae": mae, "r2": r2})

    df_res = pd.DataFrame(results).sort_values("rmse")
    df_res.to_csv("../artifacts/metrics.csv", index=False)
    print("Treinamento concluído. Métricas salvas em artifacts/metrics.csv")

if __name__ == "__main__":
    train_and_save()

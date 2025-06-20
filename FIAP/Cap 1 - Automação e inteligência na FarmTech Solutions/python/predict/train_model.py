from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from predict.config import MODEL_PATH, MODEL_DIR, RF_PARAMS
from predict.preprocessing import load_data, engineer_features, get_feature_target

def train_and_export(test_size: float = 0.2):
    df = load_data()
    
    df_feat = engineer_features(df)
    X, y = get_feature_target(df_feat)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RF_PARAMS["random_state"]
    )
    
    model = RandomForestRegressor(**RF_PARAMS)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    print(f"Modelo treinado com MSE: {mse:.4f}")
    print(f"Exportando modelo para {MODEL_PATH}")
        
    MODEL_DIR.mkdir(exist_ok=True)
    dump(model, MODEL_PATH)

if __name__ == "__main__":
    train_and_export()

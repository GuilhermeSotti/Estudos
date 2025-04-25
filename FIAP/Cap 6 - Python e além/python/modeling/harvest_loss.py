import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import KBinsDiscretizer
import joblib

def train_harvest_loss(df: pd.DataFrame, features: list, target: str, out_path: str):
    """
    Discretiza perdas em 2 classes e treina RandomForestClassifier.
    """
    dirpath = os.path.dirname(out_path)
    if dirpath and not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    X = df[features]
    y = df[target]

    kbd = KBinsDiscretizer(n_bins=2, encode='ordinal', strategy='quantile')
    y = kbd.fit_transform(df[[features[0]]]).astype(int).ravel()

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    joblib.dump(clf, out_path)
    return clf
import sys
sys.path.append("C:/pqa")

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from config import RATED_DATA_PATH, MODEL_PATH

FEATURE_COLS = [
    'word_count', 'sent_count', 'avg_word_len',
    'has_role', 'has_example', 'has_format',
    'question_marks', 'sentiment', 'specificity',
    'flesch_score', 'grade_level'
]

def train_model(data_path, model_path):
    df = pd.read_csv(data_path).dropna(subset=['quality_score'])
    print(f"Training on {len(df)} records...")

    X = df[FEATURE_COLS]
    y = df['quality_score']

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=4,
        random_state=42
    )
    model.fit(X, y)

    importance = pd.Series(
        model.feature_importances_,
        index=FEATURE_COLS
    ).sort_values(ascending=False)

    print("\nTop features that affect prompt quality:")
    print(importance.to_string())

    joblib.dump({"model": model, "features": FEATURE_COLS}, model_path)
    print(f"\nModel saved to {model_path}")

    plt.figure(figsize=(8, 5))
    importance.plot(kind='bar', color='steelblue')
    plt.title("Feature Importance")
    plt.ylabel("Importance Score")
    plt.tight_layout()
    plt.savefig("models/feature_importance.png", dpi=120)
    print("Chart saved to models/feature_importance.png")

if __name__ == "__main__":
    train_model(RATED_DATA_PATH, MODEL_PATH)
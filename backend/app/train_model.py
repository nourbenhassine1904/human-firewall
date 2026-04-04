import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

from backend.app.model_utils import load_dataset


DATA_PATH = "data/raw/messages_dataset.csv"
MODEL_DIR = "backend/models"
MODEL_PATH = os.path.join(MODEL_DIR, "phishing_model.joblib")


def train():
    df = load_dataset(DATA_PATH)

    # garder seulement les colonnes utiles
    df = df[["clean_text", "label"]].dropna()

    # sécurité
    df = df[df["label"].isin(["safe", "phishing"])]

    X = df["clean_text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            min_df=1
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification report:\n")
    print(classification_report(y_test, y_pred))
    print("\nConfusion matrix:\n")
    print(confusion_matrix(y_test, y_pred))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train()
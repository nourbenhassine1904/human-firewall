import os
import re
import joblib
import pandas as pd

MODEL_PATH = "backend/models/phishing_model.joblib"


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " URL ", text)
    text = re.sub(r"\d+", " NUM ", text)
    text = re.sub(r"[^a-zA-ZÀ-ÿ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["clean_text"] = df["text"].astype(str).apply(clean_text)
    return df


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def predict_message(text: str):
    model = load_model()
    clean = clean_text(text)

    pred = model.predict([clean])[0]
    probs = model.predict_proba([clean])[0]

    classes = list(model.named_steps["clf"].classes_)
    prob_dict = {classes[i]: float(probs[i]) for i in range(len(classes))}

    phishing_prob = prob_dict.get("phishing", 0.0)

    return {
        "clean_text": clean,
        "prediction": pred,
        "probabilities": prob_dict,
        "ml_score": phishing_prob
    }
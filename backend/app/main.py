from fastapi import FastAPI
from backend.app.schemas import AnalyzeRequest, AnalyzeResponse
from backend.app.model_utils import predict_message
from backend.app.rules import detect_rules, recommend_action
from backend.app.explain import explain_prediction

app = FastAPI(title="Human Firewall API")


@app.get("/")
def root():
    return {"message": "Human Firewall backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_message(payload: AnalyzeRequest):
    text = payload.text.strip()

    ml_result = predict_message(text)
    rules_result = detect_rules(text)

    ml_score = ml_result["ml_score"]
    rules_score = rules_result["rules_score"]

    final_score = round((0.7 * ml_score) + (0.3 * rules_score), 4)

    prediction = "phishing" if final_score >= 0.5 else "safe"

    explanation = explain_prediction(
        text=text,
        rules_triggered=rules_result["rules_triggered"],
        prediction=prediction,
        risk_score=final_score
    )

    recommended_action = recommend_action(prediction, final_score)

    return {
        "input_text": text,
        "prediction": prediction,
        "risk_score": final_score,
        "probabilities": ml_result["probabilities"],
        "rules_triggered": rules_result["rules_triggered"],
        "explanation": explanation,
        "recommended_action": recommended_action
    }
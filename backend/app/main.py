from fastapi import FastAPI, HTTPException
from uuid import uuid4
from backend.app.rules import (
    detect_rules,
    recommend_action,
    get_severity,
    get_attack_type,
    get_remediation_tips
)

from backend.app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    DecisionRequest,
    DecisionResponse
)
from backend.app.model_utils import predict_message
from backend.app.rules import detect_rules, recommend_action
from backend.app.explain import explain_prediction
from backend.app.logger_utils import create_analysis_log, read_logs, update_decision_log

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

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

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
    severity = get_severity(final_score)
    attack_type = get_attack_type(text, prediction)
    remediation_tips = get_remediation_tips(attack_type, prediction)

    analysis_id = str(uuid4())

    log_entry = {
        "analysis_id": analysis_id,
        "input_text": text,
        "prediction": prediction,
        "risk_score": final_score,
        "probabilities": ml_result["probabilities"],
        "rules_triggered": rules_result["rules_triggered"],
        "explanation": explanation,
        "recommended_action": recommended_action,
        "severity": severity,
        "attack_type": attack_type,
        "remediation_tips": remediation_tips
    }

    create_analysis_log(log_entry)

    return {
        "analysis_id": analysis_id,
        "input_text": text,
        "prediction": prediction,
        "risk_score": final_score,
        "probabilities": ml_result["probabilities"],
        "rules_triggered": rules_result["rules_triggered"],
        "explanation": explanation,
        "recommended_action": recommended_action,
        "severity": severity,
        "attack_type": attack_type,
        "remediation_tips": remediation_tips
    }


@app.post("/decision", response_model=DecisionResponse)
def submit_decision(payload: DecisionRequest):
    allowed = ["approve", "reject", "need_review"]

    if payload.human_decision not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"human_decision must be one of: {allowed}"
        )

    updated_entry = update_decision_log(
        analysis_id=payload.analysis_id,
        human_decision=payload.human_decision,
        analyst_comment=payload.analyst_comment or ""
    )

    if not updated_entry:
        raise HTTPException(status_code=404, detail="analysis_id not found")

    return {
        "message": "Human decision saved successfully",
        "analysis_id": payload.analysis_id,
        "human_decision": payload.human_decision,
        "analyst_comment": payload.analyst_comment or ""
    }


@app.get("/logs")
def get_logs():
    return read_logs()
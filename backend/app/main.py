from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from backend.app.rules import (
    detect_rules,
    recommend_action,
    get_severity,
    get_attack_type,
    get_remediation_tips,
    detect_psychological_manipulation,
    detect_tunisian_context,
    detect_qr_risk
)

from backend.app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    DecisionRequest,
    DecisionResponse
)
from backend.app.model_utils import predict_message
from backend.app.explain import explain_prediction
from backend.app.logger_utils import create_analysis_log, read_logs, update_decision_log

app = FastAPI(title="Human Firewall API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Human Firewall backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_message(payload: AnalyzeRequest):
    text = payload.text.strip()
    mode = payload.mode.strip().lower()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if mode not in ["message", "qr"]:
        raise HTTPException(status_code=400, detail="mode must be 'message' or 'qr'")

    ml_result = predict_message(text)
    rules_result = detect_rules(text)
    qr_result = detect_qr_risk(text) if mode == "qr" else {"qr_triggers": [], "qr_score": 0.0}

    ml_score = ml_result["ml_score"]
    rules_score = rules_result["rules_score"]

    if mode == "qr":
        final_score = round((0.4 * ml_score) + (0.25 * rules_score) + (0.35 * qr_result["qr_score"]), 4)
    else:
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

    psych_result = detect_psychological_manipulation(text)
    tn_result = detect_tunisian_context(text)

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
        "remediation_tips": remediation_tips,
        "psychological_profile": psych_result["psychological_profile"],
        "psychological_explanation": psych_result["psychological_explanation"],
        "tunisian_context_detected": tn_result["tunisian_context_detected"],
        "tunisian_indicators": tn_result["tunisian_indicators"],
        "tunisian_context_message": tn_result["tunisian_context_message"],
        "ml_score": round(ml_score, 4),
        "rules_score": round(rules_score, 4),
        "analysis_mode": mode,
        "qr_triggers": qr_result["qr_triggers"],
        "qr_score": qr_result["qr_score"]
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
        "remediation_tips": remediation_tips,
        "psychological_profile": psych_result["psychological_profile"],
        "psychological_explanation": psych_result["psychological_explanation"],
        "tunisian_context_detected": tn_result["tunisian_context_detected"],
        "tunisian_indicators": tn_result["tunisian_indicators"],
        "tunisian_context_message": tn_result["tunisian_context_message"],
        "ml_score": round(ml_score, 4),
        "rules_score": round(rules_score, 4),
        "analysis_mode": mode,
        "qr_triggers": qr_result["qr_triggers"],
        "qr_score": qr_result["qr_score"]
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
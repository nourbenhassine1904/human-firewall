from pydantic import BaseModel
from typing import Dict, List, Optional


class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    analysis_id: str
    input_text: str
    prediction: str
    risk_score: float
    probabilities: Dict[str, float]
    rules_triggered: List[str]
    explanation: str
    recommended_action: str


class DecisionRequest(BaseModel):
    analysis_id: str
    human_decision: str   # approve / reject / need_review
    analyst_comment: Optional[str] = ""


class DecisionResponse(BaseModel):
    message: str
    analysis_id: str
    human_decision: str
    analyst_comment: Optional[str] = ""
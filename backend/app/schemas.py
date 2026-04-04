from pydantic import BaseModel
from typing import Dict, List


class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    input_text: str
    prediction: str
    risk_score: float
    probabilities: Dict[str, float]
    rules_triggered: List[str]
    explanation: str
    recommended_action: str
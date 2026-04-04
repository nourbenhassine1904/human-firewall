import json
import os
from datetime import datetime
from typing import List, Dict, Any

LOG_PATH = "logs/audit_log.json"


def ensure_log_file():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def read_logs() -> List[Dict[str, Any]]:
    ensure_log_file()
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def write_logs(logs: List[Dict[str, Any]]):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def append_log(entry: Dict[str, Any]):
    logs = read_logs()
    logs.append(entry)
    write_logs(logs)


def create_analysis_log(entry: Dict[str, Any]):
    entry["created_at"] = datetime.utcnow().isoformat()
    entry["human_decision"] = None
    entry["analyst_comment"] = ""
    append_log(entry)


def update_decision_log(analysis_id: str, human_decision: str, analyst_comment: str = ""):
    logs = read_logs()

    for item in logs:
        if item.get("analysis_id") == analysis_id:
            item["human_decision"] = human_decision
            item["analyst_comment"] = analyst_comment
            item["decision_time"] = datetime.utcnow().isoformat()
            write_logs(logs)
            return item

    return None
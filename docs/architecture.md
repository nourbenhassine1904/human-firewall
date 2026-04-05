# Architecture Overview

Human Firewall follows a human-in-the-loop cybersecurity workflow.

## Main Components
- Streamlit frontend dashboard
- FastAPI backend API
- Text preprocessing module
- TF-IDF + Logistic Regression classifier
- Rule-based phishing indicator engine
- Explanation generator
- Human validation workflow
- JSON audit logs
- Dockerized deployment

## Data Flow
1. User submits a suspicious message from the Streamlit dashboard.
2. The FastAPI backend receives the request.
3. The text is preprocessed.
4. The ML model and rule-based engine analyze the message.
5. The system computes a final risk score.
6. The backend generates an explanation and recommended action.
7. A human analyst validates the decision.
8. All actions are stored in audit logs.

## Security Philosophy
The AI never executes critical actions automatically.
It supports the analyst with explainable recommendations, while preserving full human control.

                        +----------------------+
                        |   Citizen / Analyst  |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        |  Streamlit Frontend  |
                        |  Dashboard Interface |
                        +----------+-----------+
                                   |
                     HTTP requests | 
                                   v
                        +----------------------+
                        |   FastAPI Backend    |
                        |   /analyze           |
                        |   /decision          |
                        |   /logs              |
                        +----------+-----------+
                                   |
                 +-----------------+------------------+
                 |                                    |
                 v                                    v
      +----------------------+           +----------------------+
      |  Text Preprocessing  |           |  Rule-based Engine   |
      |  clean_text()        |           | suspicious keywords  |
      |  normalize input     |           | risk rules           |
      +----------+-----------+           +----------+-----------+
                 |                                    |
                 +-----------------+------------------+
                                   |
                                   v
                        +----------------------+
                        |   ML Classifier      |
                        | TF-IDF + LogisticReg |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Scoring + Fusion      |
                        | ML score + rules      |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Explanation Engine    |
                        | why alert was raised  |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Recommended Action    |
                        | Warn / Escalate / No  |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Human Validation      |
                        | approve/reject/review |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Audit Logs JSON       |
                        | traceable decisions   |
                        +----------------------+

Our architecture is built around an explainable human-in-the-loop workflow.
The Streamlit dashboard collects suspicious messages and interacts with a FastAPI backend.
The backend preprocesses the text, combines a TF-IDF + Logistic Regression classifier with rule-based cyber indicators, generates an explanation, and recommends an action.
No critical action is executed automatically: the final decision is always validated by a human operator.
All analyses and decisions are stored in auditable JSON logs.
The system is packaged in a dockerized architecture for reproducibility.
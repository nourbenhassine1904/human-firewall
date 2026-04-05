# Transparency Note — Human Firewall

## 1. System Purpose

Human Firewall is an explainable AI-assisted phishing detection system designed to protect Tunisian citizens from suspicious messages, phishing attempts, and local social engineering attacks.

The system does not replace the human operator. Its purpose is to assist the analyst by detecting suspicious content, explaining why an alert was raised, recommending an action, and preserving full human control over the final decision.

---

## 2. Data Sources

The MVP was developed using a small text dataset composed of:
- safe messages
- phishing messages
- synthetic examples manually created by the team
- examples adapted to the Tunisian context

The dataset includes French and English messages, with some locally relevant phishing patterns such as:
- fake banking alerts
- fake delivery notifications
- urgent account verification requests
- socially manipulative scam messages

Because of time constraints during the hackathon, the dataset is limited in size and partly synthetic.

---

## 3. Data Processing and Feature Engineering

Before training, all messages were preprocessed through a text-cleaning pipeline:
- lowercasing
- URL normalization
- digit normalization
- punctuation/noise reduction
- whitespace normalization

The system then applies:
- TF-IDF vectorization for text representation
- a Logistic Regression classifier for phishing prediction
- a rule-based suspicious keyword detector to enrich the final risk score

This design was chosen to avoid black-box behavior and to keep the system interpretable.

---

## 4. Model Choice Justification

We selected TF-IDF + Logistic Regression because:
- it is fast to train and deploy
- it is suitable for a hackathon MVP
- it provides a transparent and reproducible baseline
- it is easier to explain than opaque deep learning models

We also added a rule-based layer to strengthen explainability and better highlight suspicious cyber indicators such as urgency, account suspension, credential requests, and malicious action prompts.

The final score combines:
- the machine learning score
- the rule-based score

This hybrid approach improves interpretability and aligns with the human-controlled philosophy of the challenge.

---

## 5. Explainability

The system is designed with zero black-box logic in the final user workflow.

For each analyzed message, the dashboard displays:
- the predicted class
- the risk score
- triggered suspicious rules
- a textual explanation
- the recommended action

This allows the human operator to understand why the system raised an alert.

---

## 6. Human-in-the-loop Guarantee

Human Firewall does not execute critical actions automatically.

The system only:
- analyzes the message
- estimates the risk
- explains the alert
- recommends an action

The final decision must always be validated by a human operator through one of the available actions:
- approve
- reject
- need_review

This ensures compliance with the principle:
**“AI proposes, human decides.”**

---

## 7. Traceability and Auditability

Every analysis generates an auditable JSON log containing:
- a unique analysis ID
- the input message
- the prediction
- the risk score
- triggered rules
- generated explanation
- recommended action
- human decision
- analyst comment
- timestamps

This provides full traceability of both AI suggestions and human decisions.

---

## 8. Biases and Limitations

This MVP has several limitations:
- the dataset is relatively small
- part of the data is synthetic
- linguistic coverage is limited
- some phishing styles may not yet be represented
- the model may produce false positives or false negatives

The Tunisian cyber context is diverse, and real attacks may evolve quickly. Therefore, this prototype should be considered a first explainable decision-support tool, not a fully complete production system.

These limitations are partially mitigated by the mandatory human validation step.

---

## 9. AI Defense and Safety Measures

To reduce the risks associated with unsafe or overconfident AI behavior, we adopted the following safeguards:
- no fully autonomous critical action
- explainable outputs only
- auditable logs
- rule-based verification layer
- final human validation
- reproducible backend and frontend architecture

Because our system focuses on structured phishing message analysis rather than open-ended generation, the exposure to prompt injection is limited compared with pure LLM-based systems.

---

## 10. Reproducibility

The project is structured as a dockerized MVP with:
- FastAPI backend
- Streamlit frontend
- versioned source code
- logged outputs
- documented run instructions

This improves reproducibility and allows the jury to inspect the architecture and workflow easily.

---

## 11. Conclusion

Human Firewall is an explainable, traceable, and human-controlled AI cybersecurity assistant.

Its design prioritizes:
- transparency
- human oversight
- local relevance
- engineering simplicity
- reproducibility

This makes it aligned with the objectives of the hackathon: building AI-augmented cyber defense systems that support humans without replacing them.
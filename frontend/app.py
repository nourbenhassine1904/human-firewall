import streamlit as st
import requests
import pandas as pd

import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8001")

st.set_page_config(page_title="Human Firewall", layout="wide")

st.title("Human Firewall")
st.subheader("Explainable phishing detection with human-in-the-loop")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "demo_message" not in st.session_state:
    st.session_state.demo_message = ""

# ----------------------------
# Section 1: Analyze message
# ----------------------------
st.header("1. Analyze a suspicious message")

# Demo Scenarios
st.header("Quick Demo Scenarios")

col1, col2, col3 = st.columns(3)

if col1.button("Simulate Banking Scam"):
    st.session_state.demo_message = "Urgent : votre compte BIAT sera suspendu immédiatement. Vérifiez vos informations maintenant via ce lien."

if col2.button("Simulate Delivery Scam"):
    st.session_state.demo_message = "Votre colis ne peut pas être livré. Merci de confirmer votre adresse avant minuit via ce lien."

if col3.button("Simulate OTP Scam"):
    st.session_state.demo_message = "Votre code OTP est requis pour éviter le blocage de votre compte. Envoyez-le immédiatement."

default_message = st.session_state.get("demo_message", "")

message = st.text_area(
    "Paste a suspicious SMS, email, or message here:",
    value=default_message,
    height=180,
    placeholder="Ex: Votre compte bancaire sera suspendu. Cliquez ici immédiatement..."
)

if st.button("Analyze"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        try:
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                json={"text": message}
            )

            if response.status_code == 200:
                st.session_state.analysis_result = response.json()
                st.success("Analysis completed successfully.")
            else:
                st.error(f"Backend error: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Make sure FastAPI is running on port 8001.")

# ----------------------------
# Section 2: Show analysis
# ----------------------------
if st.session_state.analysis_result:
    result = st.session_state.analysis_result

    # Block 1: Risk Warning
    if result["severity"] == "high":
        st.error("🔴 HIGH RISK — DO NOT INTERACT")
    elif result["severity"] == "medium":
        st.warning("🟠 MEDIUM RISK — VERIFY SOURCE")
    else:
        st.success("🟢 LOW RISK — SAFE")

    st.header("2. Analysis result")

    col1, col2, col3 = st.columns(3)
    col1.metric("Prediction", result["prediction"])
    col2.metric("Risk Score", f"{result['risk_score']:.2f}")
    col3.metric("Recommended Action", result["recommended_action"])

    # Block 2: Threat Summary
    st.subheader("Threat Summary")
    col1, col2, col3 = st.columns(3)
    col1.info(f"**Severity:** {result['severity']}")
    col2.info(f"**Attack Type:** {result['attack_type']}")
    col3.info(f"**Recommended Action:** {result['recommended_action']}")

    # Block 3: Score Breakdown
    st.subheader("Explainable AI Score Breakdown")
    score_df = pd.DataFrame({
        "Component": ["ML Score", "Rules Score", "Final Risk Score"],
        "Value": [
            result["ml_score"],
            result["rules_score"],
            result["risk_score"]
        ]
    })
    st.dataframe(score_df, use_container_width=True)

    st.subheader("Probabilities")
    probs_df = pd.DataFrame(
        list(result["probabilities"].items()),
        columns=["Class", "Probability"]
    )
    st.dataframe(probs_df, use_container_width=True)

    # Block 4: Social Engineering Analysis
    st.subheader("Social Engineering Analysis")
    if result["psychological_profile"]:
        st.warning(result["psychological_explanation"])
        for item in result["psychological_profile"]:
            st.write(f"- {item}")
    else:
        st.info(result["psychological_explanation"])

    # Block 5: Citizen Protection Mode
    st.subheader("Citizen Protection Mode 🇹🇳")
    if result["tunisian_context_detected"]:
        st.success(result["tunisian_context_message"])
        for indicator in result["tunisian_indicators"]:
            st.write(f"- {indicator}")
    else:
        st.info(result["tunisian_context_message"])

    # Block 6: Remediation Tips
    st.subheader("Remediation Tips")
    for tip in result["remediation_tips"]:
        st.write(f"- {tip}")

    st.subheader("Triggered Rules")
    if result["rules_triggered"]:
        for rule in result["rules_triggered"]:
            st.write(f"- {rule}")
    else:
        st.write("No suspicious rules triggered.")

    st.subheader("Explanation")
    st.info(result["explanation"])

    st.subheader("Analysis ID")
    st.code(result["analysis_id"])

    # Block 7: Human Control Required
    st.markdown("### Human Control Required")
    st.info("No critical action is executed automatically. Human validation is mandatory.")

    # ----------------------------
    # Section 3: Human decision
    # ----------------------------
    st.header("3. Human validation")

    human_decision = st.selectbox(
        "Choose human decision:",
        ["approve", "reject", "need_review"]
    )

    analyst_comment = st.text_area(
        "Analyst comment (optional):",
        placeholder="Ex: Confirmed phishing due to suspicious link and urgency."
    )

    if st.button("Submit Decision"):
        try:
            decision_response = requests.post(
                f"{API_BASE_URL}/decision",
                json={
                    "analysis_id": result["analysis_id"],
                    "human_decision": human_decision,
                    "analyst_comment": analyst_comment
                }
            )

            if decision_response.status_code == 200:
                st.success("Human decision saved successfully.")
                st.json(decision_response.json())
            else:
                st.error(f"Decision error: {decision_response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend.")

# ----------------------------
# Section 4: Logs history
# ----------------------------
st.header("4. Audit logs history")

if st.button("Refresh Logs"):
    try:
        logs_response = requests.get(f"{API_BASE_URL}/logs")

        if logs_response.status_code == 200:
            logs = logs_response.json()

            if logs:
                logs_df = pd.DataFrame(logs)
                st.dataframe(logs_df, use_container_width=True)
            else:
                st.info("No logs available yet.")
        else:
            st.error(f"Logs error: {logs_response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend.")
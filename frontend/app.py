import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Human Firewall", layout="wide")

st.title("Human Firewall")
st.subheader("Explainable phishing detection with human-in-the-loop")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# ----------------------------
# Section 1: Analyze message
# ----------------------------
st.header("1. Analyze a suspicious message")

message = st.text_area(
    "Paste a suspicious SMS, email, or message here:",
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
            st.error("Cannot connect to backend. Make sure FastAPI is running on port 8000.")

# ----------------------------
# Section 2: Show analysis
# ----------------------------
if st.session_state.analysis_result:
    result = st.session_state.analysis_result

    st.header("2. Analysis result")

    col1, col2, col3 = st.columns(3)
    col1.metric("Prediction", result["prediction"])
    col2.metric("Risk Score", f"{result['risk_score']:.2f}")
    col3.metric("Recommended Action", result["recommended_action"])

    st.subheader("Probabilities")
    probs_df = pd.DataFrame(
        list(result["probabilities"].items()),
        columns=["Class", "Probability"]
    )
    st.dataframe(probs_df, use_container_width=True)

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
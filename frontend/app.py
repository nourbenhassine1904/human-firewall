import streamlit as st

st.set_page_config(page_title="Human Firewall", layout="wide")

st.title("Human Firewall")
st.write("Prototype de détection de phishing avec human-in-the-loop")

message = st.text_area("Collez un message suspect ici")

if st.button("Analyser"):
    if message.strip():
        st.success("Analyse déclenchée")
        st.write("Le résultat apparaîtra ici.")
    else:
        st.warning("Veuillez coller un message.")
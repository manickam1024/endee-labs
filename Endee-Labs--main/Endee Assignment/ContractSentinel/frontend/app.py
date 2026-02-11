import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="ContractSentinel", page_icon="⚖️", layout="wide")

st.title("⚖️ ContractSentinel: Agentic Legal Review")
st.markdown("### Powered by Endee Vector Database & Agentic AI")

# Sidebar for Ingestion
with st.sidebar:
    st.header("📄 Ingestion Pipeline")
    uploaded_file = st.file_uploader("Upload Contract (PDF)", type="pdf")
    
    if uploaded_file and st.button("Ingest Document"):
        with st.spinner("Chunking, Embedding & Indexing into Endee..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            try:
                response = requests.post(f"{BACKEND_URL}/ingest", files=files)
                if response.status_code == 200:
                    st.success(f"Success! Doc ID: {response.json().get('document_id')}")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

    st.markdown("---")
    st.info("💡 **Tip:** Ask about 'Liability', 'Indemnification', or 'Termination' clauses.")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask the Legal Agent..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend Agent
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking (Reasoning & Searching Endee)..."):
            try:
                response = requests.post(f"{BACKEND_URL}/chat", json={"query": prompt})
                if response.status_code == 200:
                    agent_response = response.json().get("response")
                    st.markdown(agent_response)
                    st.session_state.messages.append({"role": "assistant", "content": agent_response})
                else:
                    st.error("Agent Error: " + response.text)
            except Exception as e:
                st.error(f"Connection failed: {e}")

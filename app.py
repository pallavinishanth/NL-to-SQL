"""Streamlit UI — run with: streamlit run app.py"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# On Streamlit Cloud, ANTHROPIC_API_KEY comes from the secrets manager
if "ANTHROPIC_API_KEY" not in os.environ:
    try:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("ANTHROPIC_API_KEY not set. Add it to .env (local) or Streamlit secrets (cloud).")
        st.stop()

# Auto-initialize the SQLite DB if it doesn't exist (e.g., first run on Streamlit Cloud)
_db_path = os.path.join(os.path.dirname(__file__), "db", "store.db")
if not os.path.exists(_db_path):
    from db.setup_db import setup as _setup_db
    _setup_db()

from graph import build_graph

st.set_page_config(
    page_title="NL to SQL Agent",
    page_icon="🤖",
    layout="wide",
)

st.title("NL to SQL Agent")
st.caption("Ask questions about the store database in plain English.")

SAMPLE_QUESTIONS = [
    "How many customers do we have?",
    "Which product has the highest revenue?",
    "Show me top 3 customers by total spending",
    "How many orders are pending?",
    "What is the average order value?",
    "Which category has the most products?",
    "List all products with less than 100 units in stock",
    "How many orders were placed each month?",
]

with st.sidebar:
    st.header("Sample Questions")
    for q in SAMPLE_QUESTIONS:
        if st.button(q, use_container_width=True):
            st.session_state["selected_question"] = q

    st.divider()
    st.markdown("**Database Tables**")
    st.code("customers\nproducts\ncategories\norders\norder_items", language="text")

if "graph" not in st.session_state:
    st.session_state["graph"] = build_graph()

if "history" not in st.session_state:
    st.session_state["history"] = []

question = st.text_input(
    "Your question:",
    value=st.session_state.pop("selected_question", ""),
    placeholder="e.g. Which product has the highest revenue?",
)

col1, col2 = st.columns([1, 5])
run_clicked = col1.button("Run", type="primary", use_container_width=True)
col2.button("Clear History", on_click=lambda: st.session_state.update(history=[]))

if run_clicked and question.strip():
    initial_state = {
        "user_question": question,
        "schema_context": "",
        "sql_query": "",
        "validation_result": "",
        "execution_result": "",
        "final_answer": "",
        "error": None,
        "retry_count": 0,
    }

    with st.spinner("Thinking..."):
        result = st.session_state["graph"].invoke(initial_state)

    st.session_state["history"].insert(0, {
        "question": question,
        "sql": result["sql_query"],
        "raw": result["execution_result"],
        "answer": result["final_answer"],
        "retries": result.get("retry_count", 0),
    })

for i, entry in enumerate(st.session_state["history"]):
    with st.expander(f"Q: {entry['question']}", expanded=(i == 0)):
        st.markdown(f"**Answer:** {entry['answer']}")

        st.markdown("**SQL Query**")
        st.code(entry["sql"], language="sql")

        if entry["raw"]:
            st.markdown("**Raw Results**")
            st.text(entry["raw"])

        if entry["retries"] > 0:
            st.caption(f"Retried {entry['retries']} time(s) to get valid results.")

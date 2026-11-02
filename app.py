import pandas as pd
import streamlit as st

from graph import ask_sql_assistant

st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered SQL Assistant")
st.caption("Multi-agent natural-language-to-SQL system")

question = st.text_area(
    "Ask a question about your database",
    placeholder="Example: Show the top 5 customers by total spending",
    height=100,
)

if st.button("Run Query", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Agents are processing your question..."):
                result = ask_sql_assistant(question.strip())

            st.subheader("Execution Plan")
            st.write(result.get("plan") or "No plan available.")

            st.subheader("Generated SQL")
            st.code(result.get("sql_query") or "No SQL generated.", language="sql")

            st.subheader("Analysis")
            st.write(result.get("explanation") or "No explanation available.")

            if result.get("results") is not None:
                st.subheader("Query Results")
                df = pd.DataFrame(result["results"])
                st.dataframe(df, use_container_width=True)

            with st.expander("Database Schema"):
                st.text(result.get("schema") or "No schema available.")

            if result.get("validation_error"):
                st.error(result["validation_error"])

            if result.get("execution_error"):
                st.error(result["execution_error"])

            st.caption(
                f"SQL validation retries: {result.get('retry_count', 0)}"
            )

        except Exception as exc:
            st.error(f"Request failed: {exc}")
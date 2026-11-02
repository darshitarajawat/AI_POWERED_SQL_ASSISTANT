import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
    temperature=0
)


def result_analyzer_agent(state):
    if state.get("validation_error"):
        explanation = (
            "Unable to generate a valid SQL query after "
            f"{state.get('retry_count', 0)} failed attempt(s). "
            f"Reason: {state['validation_error']}"
        )
        return {"explanation": explanation}

    if state.get("execution_error"):
        explanation = (
            "The query could not be executed. "
            f"Database error: {state['execution_error']}"
        )
        return {"explanation": explanation}

    rows = state.get("results") or []

    # Keep the context sent to the model small.
    sample = json.dumps(rows[:50], default=str)

    response = llm.invoke([
        SystemMessage(content="""
You are a SQL Result Analysis Agent.

Explain the query results accurately and clearly.
Use only the supplied result data.
Do not invent totals, records, or trends.
Mention when no rows were returned.
Keep the explanation concise.
"""),
        HumanMessage(content=(
            f"User question: {state['question']}\n"
            f"Executed SQL: {state.get('sql_query')}\n"
            f"Number of returned rows: {len(rows)}\n"
            f"Result sample (up to 50 rows): {sample}"
        ))
    ])

    return {"explanation": response.content}
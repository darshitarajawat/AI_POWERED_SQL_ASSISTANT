import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    temperature=0
)


def planner_agent(state):
    response = llm.invoke([
        SystemMessage(content="""
You are the Planner Agent in a multi-agent SQL assistant.

Analyze the user's database question and supplied schema.
Create a short execution plan covering:
- Relevant tables and columns
- Filters, joins, and aggregations
- Sorting and result limits
- Whether clarification is needed

Do not generate SQL.
Do not invent tables or columns.
"""),
        HumanMessage(content=(
            f"User question: {state['question']}\n\n"
            f"Database schema:\n{state.get('schema') or 'Not available'}"
        ))
    ])

    return {"plan": response.content}
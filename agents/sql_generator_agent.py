import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


def sql_generator_agent(state):
    correction = state.get("validation_error")

    response = llm.invoke([
        SystemMessage(content="""
You are a SQLite SQL Generation Agent.

Generate exactly one read-only SELECT query.
Use only tables and columns in the supplied schema.
Follow the supplied execution plan.
Use explicit JOIN conditions when necessary.
Use LIMIT 100 by default unless the user requests a smaller limit.
Do not generate INSERT, UPDATE, DELETE, DROP, CREATE, or ALTER.
Do not generate multiple statements.
Return only SQL, without Markdown fences.
If an earlier validation error is supplied, correct it.
Generate SQL queries using literal values when the user's
question provides those values.

Do not use named parameters such as :course_id or
positional placeholders such as ?.

Generate executable SQLite SELECT queries.
"""),
        HumanMessage(content=(
            f"Question:\n{state['question']}\n\n"
            f"Schema:\n{state.get('schema') or ''}\n\n"
            f"Plan:\n{state.get('plan') or ''}\n\n"
            f"Previous validation error:\n{correction or 'None'}"
        ))
    ])

    sql = response.content.strip()

    # Remove optional Markdown code fences.
    if sql.startswith("```"):
        lines = sql.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        sql = "\n".join(lines).strip()

    # Clear the previous validation error for the new attempt.
    return {
        "sql_query": sql,
        "validation_error": None,
        "execution_error": None,
        "results": None,
        "explanation": None,
    }
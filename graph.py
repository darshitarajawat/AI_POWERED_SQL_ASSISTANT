from langgraph.graph import StateGraph, START, END

from state import SQLAssistantState
from agents.planner_agent import planner_agent
from agents.schema_agent import schema_agent
from agents.sql_generator_agent import sql_generator_agent
from agents.validator_agent import validator_agent
from agents.executor_agent import executor_agent
from agents.result_analyzer_agent import result_analyzer_agent


def after_validation(state):
    if state.get("validation_error"):
        if state.get("retry_count", 0) <= 2:
            return "generate"
        return "analyze"

    return "execute"


def build_graph():
    workflow = StateGraph(SQLAssistantState)

    workflow.add_node("schema", schema_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("generate", sql_generator_agent)
    workflow.add_node("validate", validator_agent)
    workflow.add_node("execute", executor_agent)
    workflow.add_node("analyze", result_analyzer_agent)

    workflow.add_edge(START, "schema")
    workflow.add_edge("schema", "planner")
    workflow.add_edge("planner", "generate")
    workflow.add_edge("generate", "validate")

    workflow.add_conditional_edges(
        "validate",
        after_validation,
        {
            "generate": "generate",
            "execute": "execute",
            "analyze": "analyze",
        }
    )

    workflow.add_edge("execute", "analyze")
    workflow.add_edge("analyze", END)

    return workflow.compile()


sql_assistant_graph = build_graph()


def ask_sql_assistant(question: str):
    initial_state = {
        "question": question,
        "plan": None,
        "schema": None,
        "sql_query": None,
        "validation_error": None,
        "execution_error": None,
        "results": None,
        "explanation": None,
        "retry_count": 0,
    }

    return sql_assistant_graph.invoke(initial_state)
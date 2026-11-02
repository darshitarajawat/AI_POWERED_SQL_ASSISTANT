from database import execute_readonly


def executor_agent(state):
    try:
        results = execute_readonly(state["sql_query"])

        return {
            "results": results,
            "execution_error": None,
        }

    except Exception as exc:
        return {
            "results": None,
            "execution_error": str(exc),
        }
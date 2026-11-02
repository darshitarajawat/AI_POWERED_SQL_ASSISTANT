from sql_validator import validate_sql


def validator_agent(state):
    sql = state.get("sql_query") or ""

    is_valid, error = validate_sql(sql)

    if is_valid:
        return {"validation_error": None}

    return {
        "validation_error": error,
        "retry_count": state.get("retry_count", 0) + 1,
    }
from database import get_schema


def schema_agent(state):
    schema = get_schema()
    return {"schema": schema}
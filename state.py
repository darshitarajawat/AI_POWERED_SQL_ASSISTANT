from typing import TypedDict, Optional, Any


class SQLAssistantState(TypedDict):
    question: str
    plan: Optional[str]
    schema: Optional[str]
    sql_query: Optional[str]

    validation_error: Optional[str]
    execution_error: Optional[str]

    results: Optional[Any]
    explanation: Optional[str]

    retry_count: int
from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_question: str
    schema_context: str
    sql_query: str
    validation_result: str
    execution_result: str
    final_answer: str
    error: Optional[str]
    retry_count: int

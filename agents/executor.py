from tools.db_tools import execute_query


def executor_node(state: dict) -> dict:
    result, error = execute_query(state["sql_query"])
    if error:
        return {
            "execution_result": "",
            "error": error,
            "retry_count": state.get("retry_count", 0) + 1,
        }
    return {
        "execution_result": result,
        "error": None,
    }

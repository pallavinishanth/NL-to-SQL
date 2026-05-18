BLOCKED_KEYWORDS = {"DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "CREATE", "REPLACE"}


def validator_node(state: dict) -> dict:
    sql = state.get("sql_query", "").strip()

    if not sql:
        return {"validation_result": "INVALID: Empty query"}

    sql_upper = sql.upper()
    tokens = set(sql_upper.split())

    for keyword in BLOCKED_KEYWORDS:
        if keyword in tokens:
            return {"validation_result": f"INVALID: '{keyword}' is not allowed"}

    if not sql_upper.lstrip().startswith("SELECT"):
        return {"validation_result": "INVALID: Query must start with SELECT"}

    return {"validation_result": "VALID"}

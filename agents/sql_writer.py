from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)


def sql_writer_node(state: dict) -> dict:
    error_context = ""
    if state.get("error"):
        error_context = (
            f"\nThe previous SQL query failed with this error:\n  {state['error']}\n"
            f"Previous query was:\n  {state.get('sql_query', '')}\n"
            "Please fix the query based on the error above."
        )

    prompt = f"""You are an expert SQLite SQL writer. Generate a valid SQLite SELECT query.

Database Schema:
{state['schema_context']}

User Question: {state['user_question']}
{error_context}

Rules:
- Write only a single SELECT query
- Do NOT use DML statements (INSERT, UPDATE, DELETE, DROP, etc.)
- Use proper SQLite syntax (e.g. strftime for dates)
- Return ONLY the raw SQL query — no markdown, no explanation, no backticks
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    sql = response.content.strip().strip("```sql").strip("```").strip()
    return {"sql_query": sql}

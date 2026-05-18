from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)


def explainer_node(state: dict) -> dict:
    if state.get("error") and not state.get("execution_result"):
        return {
            "final_answer": (
                f"I was unable to answer your question after {state.get('retry_count', 0)} attempt(s). "
                f"Last error: {state['error']}"
            )
        }

    prompt = f"""You are a helpful data analyst. The user asked a question and a SQL query was executed.
Explain the results clearly and concisely in natural language.

User Question: {state['user_question']}

SQL Query Used:
{state['sql_query']}

Query Results:
{state['execution_result']}

Instructions:
- Answer the user's question directly using the data
- Highlight key numbers, trends, or insights
- Keep it concise (2-4 sentences max)
- Do not repeat the SQL query or raw table data
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_answer": response.content.strip()}

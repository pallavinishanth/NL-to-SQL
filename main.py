"""CLI entry point — run this to test queries from the terminal."""

import os
from dotenv import load_dotenv

load_dotenv()

from graph import build_graph  # noqa: E402

app = build_graph()

SAMPLE_QUESTIONS = [
    "How many customers do we have in total?",
    "Which product has the highest revenue?",
    "Show me the top 3 customers by total spending",
    "How many orders are pending?",
    "What is the average order value?",
    "Which category has the most products?",
    "List all products with less than 100 units in stock",
]


def ask(question: str, verbose: bool = True) -> dict:
    initial_state = {
        "user_question": question,
        "schema_context": "",
        "sql_query": "",
        "validation_result": "",
        "execution_result": "",
        "final_answer": "",
        "error": None,
        "retry_count": 0,
    }

    result = app.invoke(initial_state)

    if verbose:
        print("\n" + "=" * 60)
        print(f"Question : {question}")
        print(f"SQL      : {result['sql_query']}")
        print(f"Answer   : {result['final_answer']}")
        if result.get("retry_count", 0) > 0:
            print(f"Retries  : {result['retry_count']}")
        print("=" * 60)

    return result


if __name__ == "__main__":
    print("NL to SQL Agent — sample queries\n")
    for q in SAMPLE_QUESTIONS:
        ask(q)

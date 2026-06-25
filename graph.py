from langgraph.graph import StateGraph, END

from state import AgentState
from tools.mcp_client import get_schema
from agents.sql_writer import sql_writer_node
from agents.validator import validator_node
from agents.executor import executor_node
from agents.explainer import explainer_node

MAX_RETRIES = 3


def schema_injector_node(state: AgentState) -> AgentState:
    return {"schema_context": get_schema()}


def route_after_validation(state: AgentState) -> str:
    if state["validation_result"].startswith("VALID"):
        return "executor"
    return "sql_writer"


def route_after_execution(state: AgentState) -> str:
    if state.get("error") and state.get("retry_count", 0) < MAX_RETRIES:
        return "sql_writer"
    return "explainer"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("schema_injector", schema_injector_node)
    graph.add_node("sql_writer", sql_writer_node)
    graph.add_node("validator", validator_node)
    graph.add_node("executor", executor_node)
    graph.add_node("explainer", explainer_node)

    graph.set_entry_point("schema_injector")

    graph.add_edge("schema_injector", "sql_writer")
    graph.add_edge("sql_writer", "validator")

    graph.add_conditional_edges(
        "validator",
        route_after_validation,
        {"executor": "executor", "sql_writer": "sql_writer"},
    )

    graph.add_conditional_edges(
        "executor",
        route_after_execution,
        {"sql_writer": "sql_writer", "explainer": "explainer"},
    )

    graph.add_edge("explainer", END)

    return graph.compile()

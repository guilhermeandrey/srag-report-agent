from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from models import GraphState
from nodes import final_report_agent, news_agent


def compile_state_graph() -> CompiledStateGraph:
    workflow = StateGraph(GraphState)
    workflow.add_node("news", news_agent)
    workflow.add_node("final", final_report_agent)
    workflow.set_entry_point("news")
    workflow.add_edge("news", "final")
    workflow.add_edge("final", END)
    app = workflow.compile()
    return app

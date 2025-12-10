from typing import List
from langgraph.graph import MessageGraph, END

from execute_tools import execute_tools
from chains import first_responder_chain, reviser_chain
from langchain_core.messages import BaseMessage, ToolMessage

MAX_ITERATIONS = 2
DRAFT = "draft"
TOOLS = "tools"
REVISER = "reviser"

graph = MessageGraph()

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item,ToolMessage) for item in state)
    if count_tool_visits >MAX_ITERATIONS:
        return END
    return TOOLS


graph.add_node(DRAFT, first_responder_chain)
graph.add_node(TOOLS, execute_tools)
graph.add_node(REVISER, reviser_chain)

graph.add_edge(DRAFT, TOOLS)
graph.add_edge(TOOLS, REVISER)
graph.add_conditional_edges(REVISER, event_loop)
graph.set_entry_point(DRAFT)

app = graph.compile()
print(app.get_graph().draw_mermaid())

response = app.invoke("write about whether alian life exists")

print(response[-1].tool_calls[0]["args"]["answer"])
print()
print(response)

from typing import TypedDict
from langgraph.graph import StateGraph, END

class SimpleState(TypedDict):
    count : int

def increment_node(state: SimpleState) -> SimpleState:
    return {
        "count": state["count"] + 1
    }

def should_continue(state: SimpleState) -> str:
    if state["count"] > 5:
        return "stop"
    return "continue"


graph = StateGraph(SimpleState)

graph.add_node("increment", increment_node)
graph.add_conditional_edges("increment", should_continue, {
    "continue": "increment",
    "stop": END
})
graph.set_entry_point("increment")
app = graph.compile()

state = { "count": 0}
result = app.invoke(state)
print(result)
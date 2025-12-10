from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
import operator

class SimpleState(TypedDict):
    count : int
    sum : Annotated[int, operator.add]
    history: Annotated[List[int], operator.concat]

def increment_node(state: SimpleState) -> SimpleState:
    new_count = state["count"] + 1
    return {
        "count": new_count,
        "sum": new_count,
        "history": [state["sum"]]

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

state = {
    "count": 0,
    "sum": 0,
    "history": []
}
result = app.invoke(state)
print(result)
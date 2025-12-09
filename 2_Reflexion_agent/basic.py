import os
from dotenv import load_dotenv
from chains import generator_chain, reflection_chain
from langchain_core.messages import HumanMessage
from langgraph.graph import MessageGraph, END

load_dotenv()
print(os.getenv("GOOGLE_API_KEY"))

REFLECT = "reflect"
GENERATE = "generate"
graph = MessageGraph()

def generation_node(state):
    return generator_chain.invoke({
        "messages": state
    })

def reflection_node(messages):
    response = reflection_chain.invoke({
        "messages": messages
    })
    return HumanMessage(content = response.content)

def should_continue(state):
    if len(state)>4:
        return END
    return REFLECT

graph.add_node(GENERATE, generation_node)
graph.add_node(REFLECT, reflection_node)
graph.set_entry_point(GENERATE)

graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()
print(app.get_graph().draw_mermaid())

response = app.invoke(HumanMessage(content="AI and small scale business growth"))
print(response)
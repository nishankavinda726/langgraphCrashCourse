from typing import List, Annotated, TypedDict
from langgraph.graph import StateGraph, add_messages, END
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chat_node(state:BasicChatState):
    return {
        "messages":llm.invoke(state["messages"])
    }

graph = StateGraph(BasicChatState)

graph.add_node("chat", chat_node)
graph.set_entry_point("chat")
graph.add_edge("chat", END)

app = graph.compile()

while True:
    user_input = input("Enter a message: ")
    if user_input in ["exit", "end"]:
        break
    else:
        result = app.invoke({
            "messages": HumanMessage(content=user_input)
        })

        print(result)
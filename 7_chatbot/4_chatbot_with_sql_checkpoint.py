from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, add_messages
from langchain_core.messages import AIMessage, HumanMessage

from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()
sqlite_conn = sqlite3.connect("chatbot.db", check_same_thread=False)

llm = ChatGroq(model="llama-3.1-8b-instant")

memory = SqliteSaver(sqlite_conn)

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

graph = StateGraph(ChatState)

CHAT_NODE = "chat_node"
TOOLS_NODE = "tools"

def chatbot_node(state: ChatState):
    return{
        "messages": llm.invoke(state["messages"]),
    }

graph.add_node(CHAT_NODE, chatbot_node)
graph.add_edge(CHAT_NODE, END)
graph.set_entry_point(CHAT_NODE)

app = graph.compile(checkpointer=memory)
config = {
    "configurable":{
        "thread_id":1
    }
}
while True:
    user_input = input("Enter a message: ")
    if user_input in ["exit", "end"]:
        break
    else:
        result = app.invoke(
            {
                "messages": [HumanMessage(content=user_input)]
            }, config=config
        )
        print(f"AI: {result["messages"][-1].content}")

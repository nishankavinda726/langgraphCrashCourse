from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import TavilySearchResults
from langgraph.graph import StateGraph, END, add_messages
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import ToolNode
load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="llama-3.1-8b-instant")
tavily_search_tool = TavilySearchResults(search_depth='basic', max_results=2)
tools = [tavily_search_tool]

llm_with_tools = llm.bind_tools(tools=tools)
graph = StateGraph(ChatState)

CHAT_NODE = "chat_node"
TOOLS_NODE = "tools"

def chatbot_node(state: ChatState):
    return{
        "messages": llm_with_tools.invoke(state["messages"]),
    }
tool_node = ToolNode(tools=tools)
def tool_router(state: ChatState):
    last_msg = state["messages"][-1]
    if hasattr(last_msg,"tool_calls") and len(last_msg.tool_calls)>0:
        return TOOLS_NODE
    else:
        return END
graph.add_node(CHAT_NODE, chatbot_node)
graph.add_node(TOOLS_NODE, tool_node)
graph.set_entry_point(CHAT_NODE)
graph.add_conditional_edges(CHAT_NODE, tool_router)
graph.add_edge(TOOLS_NODE, CHAT_NODE)

app = graph.compile()

while True:
    user_input = input("Enter a message: ")
    if user_input in ["exit", "end"]:
        break
    else:
        result = app.invoke(
            {
                "messages": [HumanMessage(content=user_input)]
            }
        )
        print(result)

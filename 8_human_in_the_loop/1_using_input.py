from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, add_messages
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

class ChatState(TypedDict):
    messages:  Annotated[list, add_messages]

CREATE_POST = "generate_post"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback"

def create_post(state: ChatState):
    return {
        "messages": llm.invoke(state["messages"])
    }

def collect_feedback(state: ChatState):
    feedback = input("How can I improve this post?")
    return {
        "messages":[HumanMessage(content=feedback)]
    }

def post(state: ChatState):
    final_post = state["messages"][-1].content
    print("\n current post")
    print(final_post)
    print("post published")


def get_review_decisions(state: ChatState):
    post_content = state["messages"][-1].content

    print("\n current post")
    print(post_content)
    print()

    decision = input("post on Linkedin (yes/no)?\n")

    if decision.lower() == "yes":
        return POST
    else:
        return COLLECT_FEEDBACK

graph = StateGraph(ChatState)

graph.add_node(CREATE_POST, create_post)
graph.add_node(POST, post)
graph.add_node(COLLECT_FEEDBACK, collect_feedback)

graph.set_entry_point(CREATE_POST)

graph.add_conditional_edges(CREATE_POST, get_review_decisions)
graph.add_edge(COLLECT_FEEDBACK, CREATE_POST)
graph.add_edge(POST, END)

app = graph.compile()

response = app.invoke({
    "messages": [HumanMessage(content="write me a linkedin post about how we can find solutions using AI for global warming")],
})

print(response)
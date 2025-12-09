import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain.agents import initialize_agent, tool
# from langchain.agents import create_agent
# from langchain_core.tools import tool

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search_tool = TavilySearchResults(search_depth="basic")

@tool
def get_system_time(format: str ="%Y-%m-%d %H:%M:%S"):
    """Return the current system time."""
    return datetime.datetime.now().strftime(format)

tools = [search_tool, get_system_time]
agent = initialize_agent(tools=tools, llm=llm, verbose=True)
response = agent.invoke("find updates about recent flooding in sri lanka and note down as point form")
print("response")
print(response)
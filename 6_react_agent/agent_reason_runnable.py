import os
from langchain.agents import create_react_agent, tool
import datetime
from langchain_community.tools import TavilySearchResults
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

@tool
def get_systemtime(format: str= "%Y-%m-%d %H:%M:%S"):
    """Return the current system time in the specified format."""
    return datetime.datetime.now().strftime(format)

search_tool = TavilySearchResults(search_depth='basic')

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

react_prompt = hub.pull("hwchase17/react")

tools = [search_tool, get_systemtime]

react_agent_runnable = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
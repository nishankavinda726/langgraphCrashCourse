import json
from langchain_community.tools import TavilySearchResults
from typing import List
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
load_dotenv()

tavily = TavilySearchResults(max_results=5)

def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_msg: AIMessage = state[-1]

    # Exact tools calls from AI msg
    if  not hasattr(last_ai_msg, 'tool_calls') or not last_ai_msg.tool_calls:
        return []

    tool_messages = []

    for tool_call in last_ai_msg.tool_calls:
        if tool_call["name"] in ['AnswerQuestion','RevisedAnswer']:
            call_id = tool_call["id"]
            tool_name = tool_call["name"]
            search_queries = tool_call["args"].get("search_queries", [])

            query_results = {}
            for search_query in search_queries:
                results = tavily.invoke(search_query)
                query_results[search_query] = results

            tool_messages.append(ToolMessage(content=json.dumps(query_results),
                                             tool_call_id= call_id,
                                             name= tool_name)
                                 )
            return tool_messages
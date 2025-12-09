from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
# from langchain_community.tools import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from dotenv import load_dotenv
from schema import AnswerQuestion, RevisedAnswer
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
validator = PydanticToolsParser(tools=[AnswerQuestion])

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a expert AI researcher.
            current time: {time}
            
            1. {first_instruction}
            2. You need to reflect and critique your answer. Me severe to get the maximum improvement.
            3. after refelction, include 1-3 search queries separately for researching improvements. Do not include this inside the reflection 
            
            IMPORTANT: Answer the user's question above using the required format.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),

    ]
).partial(time = lambda: datetime.datetime.now().isoformat())

# -------------------------------------

first_responder_prompt = actor_prompt_template.partial(first_instruction= "provide detailed ~250 word answer.")

first_responder_chain = first_responder_prompt | llm.bind_tools(tools =[AnswerQuestion], tool_choice='AnswerQuestion') | validator

response = first_responder_chain.invoke({
    "messages": [HumanMessage(content="Explain how global warming increase the natural disasters, explain with examples such as Dithwa affected Sri Lanka recently")]
})
print(response)
# -----------------------------------

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

reviser_prompt_template = actor_prompt_template.partial(first_instruction=revise_instructions)

reviser_chain = reviser_prompt_template | llm.bind_tools(tools =[RevisedAnswer], tool_choice='RevisedAnswer')
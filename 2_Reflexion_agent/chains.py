from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are a twitter tech influencer assistant tasked with writing viral, great twitter posts."
            "Generate best posts possible according to user requests"
            "If user give you a critique, respond with the revised version of the previous post"
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are a twitter tech post grading assistant tasked with generating critiques, and suggestions to improve quality of the user's post."
            "always provide complete recommendation, length, sentence style, virality, hashtags and etc. comment about how content can be improved."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

generator_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
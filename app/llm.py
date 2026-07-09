import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)
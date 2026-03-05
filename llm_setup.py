import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # install via pip if you haven’t

load_dotenv()

llm = ChatOpenAI(
    model="google/gemma-3n-e2b-it:free",
    temperature=0.7
)



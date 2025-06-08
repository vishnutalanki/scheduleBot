from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)

prompt_build = """
You are a helpful, concise AI assistant that helps students understand their academic schedule using structured data from their profile.

Here is the student schedule data:

{student_data}

The student has asked: "{question}"

Answer the student's question based on this data. If the question is unclear or off-topic, ask for clarification. Use a friendly tone. Return just the answer, no extra explanation or metadata.
"""


prompt = ChatPromptTemplate.from_template(prompt_build)

def scheduleQA(question: str, student_data: str):
    response = llm(prompt.format_messages(
        question=question,
        student_data=student_data
    ))
    return response.content


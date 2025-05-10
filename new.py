import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

# LangChain tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A chatbot with openai"

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant.please response to the user queries"),
        ("user", "question:{question}"),
    ]
)

def generate_response(question, api_key, llm, temperature, max_token):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm, temperature=temperature, max_tokens=max_token)
    chain = prompt | llm
    answer = chain.invoke({"question": question})
    return answer.content  # ✅ Only change: return clean message

# Title of the app
st.title("enhanced Q&A chatbot with openai")

# Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("enter your openai_api_key")

# Dropdown to select model
llm = st.sidebar.selectbox("select an open AI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

# Adjust response parameters
temperature = st.sidebar.slider("temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max tokens", min_value=50, max_value=300, value=150)

# Main interface
st.write("go ahead and ask any qustions")
user_input = st.text_input("you:")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("please provide the query")

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

@tool
def calculator(expression):
    """Evaluate an arithmetic expression (+, -, *, /, parentheses)."""
    try:
        result=eval(expression)
        return str(result)
    except:
        return "Error : cannot solve expression"

@tool
def get_weather(city):
    """Fetch current weather for a given city using OpenWeather API."""
    try:
        api_key=os.getenv("OPENWEATHER_API_KEY")
        url=f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response=requests.get(url)
        weather=response.json()
        return json.dumps(weather)
    except:
        return "Error"

@tool
def read_file(filepath):
    """Read and return the contents of a text file."""
    try:
        with open(filepath,'r') as file:
            text=file.read()
            return text
    except:
        return "Error: Cannot read file"

@wrap_model_call
def model_logging(request,handler):
    """Middleware that logs model calls before and after execution."""
    print("\nBefore model call :","-"*20)
    response=handler(request)
    print("After model call :","-"*20)
    if response.result and response.result[0].content:
        response.result[0].content=response.result[0].content.upper()
    return response

llm=init_chat_model(
    model="google/gemma-3n-e4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)

agent=create_agent(
    model=llm,
    tools=[calculator,get_weather,read_file],
    middleware=[model_logging],
    system_prompt="You are a helpful assistant. Answer in short.Always use the calculator tool for any arithmetic expressions or equations."
)

st.title("LangChain Assistant")
st.write("Enter question here:")

user_input=st.text_input("You:")

if user_input:
    if user_input.lower()=="exit":
        st.warning("Session ended. Refresh to start again.")
    else:
        result=agent.invoke({
            "messages":[
                {"role":"user","content":user_input}
            ]
        })
        ai_msg=result["messages"][-1]
        st.success(f"AI: {ai_msg.content}")

        st.subheader("Full Conversation:")
        for msg in result["messages"]:
            role="USER" if msg.__class__.__name__=="HumanMessage" else "AI"
            st.write(f"{role}: {msg.content}")



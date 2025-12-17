import os
import requests
import streamlit as st

st.title("My Chatbot")

groq_key=os.getenv("GROQ_API_KEY")
groq_url="https://api.groq.com/openai/v1/chat/completions"
groq_headers={"Authorization":f"Bearer {groq_key}","Content-Type":"application/json"}

lm_url="http://127.0.0.1:1234/v1/chat/completions"
lm_headers={"Authorization":"Bearer dummy_key","Content-Type":"application/json"}

st.sidebar.title("Select Model")
model_sel=st.sidebar.radio("Choose LLM",["Groq Cloud","LM Studio"])

if "hist" not in st.session_state:
    st.session_state.hist=[]

input=st.chat_input("Ask anything:")

if input:
    if model_sel=="Groq Cloud":
        data={
            "model":"llama-3.3-70b-versatile",
            "messages":[{"role":"user","content":input}]
        }
        res=requests.post(groq_url,headers=groq_headers,json=data)
    else:
        data={
            "model":"phi-4-mini-instruct",
            "messages":[{"role":"user","content":input}]
        }
        res=requests.post(lm_url,headers=lm_headers,json=data)

    resp=res.json()
    if "choices" in resp:
        result=resp["choices"][0]["message"]["content"]
    else:
        result=str(resp)

    st.session_state.hist.append({"usr":input,"mdl":result})

for msg in st.session_state.hist:
    st.chat_message("user").write(msg["usr"])
    st.chat_message("assistant").write(msg["mdl"])

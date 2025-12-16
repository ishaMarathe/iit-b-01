import streamlit as st
import time

st.title("Simple Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"]=[]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt=st.chat_input("Say something...")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    def stream_response():
        response_text=f"You said: {prompt}"
        for word in response_text.split():
            yield word+" "
            time.sleep(0.15)

    with st.chat_message("assistant"):
        st.write_stream(stream_response)

    full_reply=f"You said: {prompt}"
    st.session_state.messages.append({"role":"assistant","content":full_reply})

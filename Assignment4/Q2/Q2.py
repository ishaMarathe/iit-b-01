import streamlit as st
import pandas as pd
from datetime import datetime
import os

if "user" not in st.session_state:
    st.session_state.user=None

if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["userid","password"]).to_csv("users.csv",index=False)

if not os.path.exists("userfiles.csv"):
    pd.DataFrame(columns=["userid","csv_name","time"]).to_csv("userfiles.csv",index=False)

st.sidebar.title("Menu")

if st.session_state.user is None:
    choice=st.sidebar.selectbox("Select",["Home","Login","Register"])
    if choice=="Home":
        st.write("Welcome")

    elif choice=="Register":
        u=st.text_input("User ID")
        p=st.text_input("Password")
        if st.button("Register"):
            df=pd.read_csv("users.csv")
            df.loc[len(df)]=[u,p]
            df.to_csv("users.csv",index=False)
            st.success("Registered")

    elif choice=="Login":
        u=st.text_input("User ID")
        p=st.text_input("Password")
        if st.button("Login"):
            df=pd.read_csv("users.csv")
            if ((df["userid"]==u)&(df["password"]==p)).any():
                st.session_state.user=u
                st.success("Login successful")
            else:
                st.error("Invalid user")

else:
    choice=st.sidebar.selectbox("Select",["Explore CSV","See History","Logout"])
    if choice=="Explore CSV":
        file=st.file_uploader("Upload CSV",type="csv")
        if file:
            pd.read_csv(file)
            df=pd.read_csv("userfiles.csv")
            df.loc[len(df)]=[st.session_state.user,file.name,datetime.now()]
            df.to_csv("userfiles.csv",index=False)
            st.success("File uploaded")

    elif choice=="See History":
        df=pd.read_csv("userfiles.csv")
        st.dataframe(df[df["userid"]==st.session_state.user])

    elif choice=="Logout":
        st.session_state.user=None
        st.success("Logged out")

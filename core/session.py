import streamlit as st 
from core.chat_history import ChatHistory

class Session():
    def __init__(self):
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = ChatHistory()
            
    def get_history(self):
        return st.session_state["chat_history"]

    
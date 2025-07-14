import streamlit as st

class UserInput:
    def __init__(self):
        pass
    
    def get_input(self):
        return st.text_input(
            label="Your Message",
            placeholder="Ask Anything",
            key="user_input"
        )




import streamlit as st

class Settings:
    def __init__(self):
        if "settings" not in st.session_state:
            st.session_state["settings"] = {
                "bot_name": "Bot",
                "theme": "light"
            }

    def get_settings(self):
        return st.session_state["settings"]

    def update_settings(self, key, value):
        st.session_state["settings"][key] = value



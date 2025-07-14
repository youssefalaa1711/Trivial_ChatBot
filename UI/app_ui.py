import streamlit as st
from datetime import datetime

from core.session import Session
from core.user_input import UserInput
from core.message import Message
from core.settings import Settings
from core.file_upload import FileUpload
from utils.random_responder import RandomResponder


class AppUI:
    def __init__(self):
        self.session = Session()
        self.chat_history = self.session.get_history()
        self.user_input = UserInput()
        self.settings = Settings()
        self.file_upload = FileUpload()

    def run(self):
        st.set_page_config(page_title="Trivial ChatBot", layout="wide")
        # Theme CSS
        settings = self.settings.get_settings()
        theme = settings.get("theme", "light")
        accent_color = settings.get("accent_color", "#4F8BF9")
        if theme == "dark":
            st.markdown(f"""
                <style>
                body, .stApp {{ background-color: #18191A !important; color: #f1f1f1 !important; }}
                .stChatMessage.user {{background-color: #263238; color: #fff;}}
                .stChatMessage.assistant {{background-color: {accent_color}; color: #fff;}}
                .stChatInput {{background: #23272F; color: #fff;}}
                </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <style>
                .stChatMessage.user {{background-color: #e0f7fa; border-radius: 10px; margin-bottom: 8px;}}
                .stChatMessage.assistant {{background-color: {accent_color}; border-radius: 10px; margin-bottom: 8px; color: #fff;}}
                .stChatInput {{position: fixed; bottom: 0; left: 0; width: 100%; background: #fff; padding: 1rem 2rem; box-shadow: 0 -2px 8px rgba(0,0,0,0.05);}}
                </style>
            """, unsafe_allow_html=True)

        # Title always at the top
        st.markdown("<h1 style='text-align:center;'>Trivial ChatBot</h1>", unsafe_allow_html=True)

        # Sidebar with settings
        st.sidebar.title("⚙️ Settings")
        theme = st.sidebar.selectbox("Theme", ["Light", "Dark"], index=0 if settings.get("theme") == "light" else 1)
        emoji = st.sidebar.selectbox("Bot Emoji", ["🤖", "💬", "🧠", "👾", "🦾"], index=["🤖", "💬", "🧠", "👾", "🦾"].index(settings.get("emoji", "🤖")))
        bot_name = st.sidebar.text_input("Bot Name", value=settings.get("bot_name", "Bot"))
        if st.sidebar.button("Clear Chat"):
            self.chat_history.clear()
            st.session_state["last_input"] = ""
        # Save settings
        self.settings.update_settings("theme", theme.lower())
        self.settings.update_settings("bot_name", bot_name)
        self.settings.update_settings("emoji", emoji)

        # File upload in sidebar
        with st.sidebar:
            uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
            if uploaded_file:
                file_text = self.file_upload.read_file(uploaded_file)
                st.write("📄 File Content:")
                st.text(file_text)

        st.divider()

        # Main chat area
        chat_container = st.container()
        with chat_container:
            for msg in self.chat_history.get_all():
                role = "user" if msg.sender == "User" else "assistant"
                emoji_display = "" if role == "user" else settings.get("emoji", "🤖")
                with st.chat_message(role):
                    st.markdown(f"{emoji_display} **{msg.sender}**: {msg.content}")

        # Input at the bottom (fixed bar)
        st.markdown("<div class='stChatInput'></div>", unsafe_allow_html=True)
        st.text_input(
            label="Your Message",
            placeholder="Ask Anything",
            key="user_input",
            on_change=self.handle_user_input
        )

    def handle_user_input(self):
        # Ensure 'last_input' is initialized
        if "last_input" not in st.session_state:
            st.session_state["last_input"] = ""
        user_text = st.session_state.get("user_input", "").strip()
        if user_text and user_text != st.session_state["last_input"]:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.chat_history.add_message(Message("User", user_text, timestamp))
            bot_name = self.settings.get_settings().get("bot_name", "Bot")
            bot_reply = RandomResponder.get_response()
            self.chat_history.add_message(Message(bot_name, bot_reply, timestamp))
            st.session_state["last_input"] = user_text
        st.session_state["user_input"] = ""  # Clear input field

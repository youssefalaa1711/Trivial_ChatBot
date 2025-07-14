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

        # Title always at the top
        st.title("Trivial ChatBot")

        # Sidebar with settings (scrollable)
        with st.sidebar:
            st.title("⚙️ Settings")
            settings = self.settings.get_settings()
            # Remove theme selector
            emoji = st.selectbox("Bot Emoji", ["🤖", "💬", "🧠", "👾", "🦾"], index=["🤖", "💬", "🧠", "👾", "🦾"].index(settings.get("emoji", "🤖")))
            bot_name = st.text_input("Bot Name", value=settings.get("bot_name", "Bot"))
            user_name = st.text_input("Your Name (optional)", value=st.session_state.get("user_name", "You"))
            st.session_state["user_name"] = user_name
            if st.button("Clear Chat"):
                self.chat_history.clear()
                st.session_state["last_input"] = ""
            self.settings.update_settings("bot_name", bot_name)
            self.settings.update_settings("emoji", emoji)
            uploaded_file = st.file_uploader("Upload a file (txt, png, jpg, jpeg, gif, bmp, webp)", type=["txt", "png", "jpg", "jpeg", "gif", "bmp", "webp"])
            if uploaded_file:
                if uploaded_file.type.startswith("image/"):
                    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                elif uploaded_file.type == "text/plain":
                    file_text = self.file_upload.read_file(uploaded_file)
                    st.write("📄 File Content:")
                    st.text_area("File Preview", file_text, height=100)
                else:
                    st.warning("Unsupported file type.")

        st.divider()

        # Welcome message
        if not self.chat_history.get_all():
            st.success(f"{settings.get('emoji', '🤖')} **{bot_name}:** Welcome to Trivial ChatBot! How can I help you today?")

        # Main chat area (no timestamp for user)
        chat_placeholder = st.container()
        with chat_placeholder:
            for msg in self.chat_history.get_all():
                role = "user" if msg.sender == "User" else "assistant"
                if role == "user":
                    st.info(f"**{st.session_state.get('user_name', 'You')}:** {msg.content}")
                else:
                    st.success(f"{settings.get('emoji', '🤖')} **{msg.sender}:** {msg.content}")

        # Input at the bottom (single-line, Enter to send)
        st.text_input(
            label="Your Message",
            placeholder="Ask Anything",
            key="user_input",
            on_change=self.handle_user_input,
            help="Type your message and press Enter."
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
            emoji = self.settings.get_settings().get("emoji", "🤖")
            with st.spinner(f"Thinking... {emoji}"):
                bot_reply = RandomResponder.get_response()
            self.chat_history.add_message(Message(bot_name, bot_reply, timestamp))
            st.session_state["last_input"] = user_text
        st.session_state["user_input"] = ""  # Clear input field

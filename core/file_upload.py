import streamlit as st

class FileUpload:
    
    def __init__(self):
        pass
    
    def upload_file(self):
        uploaded_file = st.file_uploader("Upload a text file",type=["txt"])
        return uploaded_file
    
    def read_file(self,uploaded_file):
        return uploaded_file.read().decode("utf-8")
        
class ChatHistory:
    
    def __init__(self):
        self.messages= []
        
    def add_message(self,message):
        self.messages.append(message)
        
    def get_all(self):
        return self.messages

    def clear(self):
        self.messages.clear()


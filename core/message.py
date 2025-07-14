import time

class Message:
    def __init__(self, sender: str, content: str, timestamp: str):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp

    def __str__(self):
        return f"{self.sender} ({self.timestamp}): {self.content}"

    


#print(user1)
import random

class RandomResponder:
    replies = [
        "Wow!",
        "Amazing!",
        "Great!",
        "How can I help?",
        "That's interesting!",
        "Tell me more!",
        "I'm here to assist you!",
        "Could you elaborate?",
        "Let's talk about it!",
        "What else would you like to know?",
        "I'm listening!",
        "That's cool!",
        "Do you have another question?",
        "I'm happy to help!",
        "Let's keep chatting!"
    ]

    @classmethod
    def get_response(cls):
        return random.choice(cls.replies)
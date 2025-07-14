import random

class RandomResponder:
    replies =["wow","amazing","Great","How can i help?" ]
    
    @classmethod
    def get_response(cls):
        return random.choice(cls.replies)
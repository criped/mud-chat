

class Message:
    TYPE = 'chat.message'

    def __init__(self, text):
        self.payload = {
            'type': self.TYPE,
            'text': str(text),
        }



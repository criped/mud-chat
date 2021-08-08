

class GroupMessage:
    TYPE = 'chat.group_message'

    def __init__(self, text, username, location, read_mode=True):
        text = f"{username} says: {text}" if read_mode else text

        self.payload = {
            'type': self.TYPE,
            'text': text,
            'username': username,
            'location': location
        }

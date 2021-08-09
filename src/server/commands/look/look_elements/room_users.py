from contrib.mud_auth.models import User
from server.commands.look.look_elements.base import LookElementAbstract


class LookElementUsers(LookElementAbstract):
    TEMPLATE = 'Players: {players}\n'
    PLAYERS_SEPARATOR = ', '
    LOGGED_PLAYER = '{username} (you)'

    def __init__(self, connection, *args, **kwargs):
        self.connection = connection

    async def get_element_str(self) -> str:
        usernames = await User.get_online_usernames_in_location(
            self.connection.scope['session']['current_location_id']
        )
        username_logged_in = self.connection.scope['session']['username']
        usernames.remove(username_logged_in)
        # Place logged in username at the beginning
        usernames = [
            self.LOGGED_PLAYER.format(
                username=username_logged_in
            ),
            *usernames
        ]
        return self.TEMPLATE.format(
            players=self.PLAYERS_SEPARATOR.join(usernames)
        )

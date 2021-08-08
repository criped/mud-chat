from channels.auth import login
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy as _

from contrib.mud_auth.models import User
from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin


class CommandLogin(CommandAbstract):
    ALIASES = ('login', 'l')
    MESSAGE_ERROR_USER_NOT_FOUND = _('User not found')
    MESSAGE_ERROR_WRONG_PASSWORD = _('Incorrect password')
    MESSAGE_SUCCESS = _('Logged in successfully as {username}!')
    MESSAGE_SUCCESS_BROADCAST = _('User {username} is online')

    NOTIFICATION_SUCCESS = _('User {username} logged in successfully!')

    def __init__(self, connection, parser: CommandParserLogin) -> None:
        super().__init__(connection, parser)

    async def run(self) -> None:
        """
        Logs in an user by username and password.

        It checks that the user exists and that the given password is correct, sending a text to the user
        for each specific case.

        Finally, a text is sent to all the online users
        """
        username = self.parser.username
        try:
            user = await User.get_by_username(username)
        except User.DoesNotExist:
            await self.send_chat_message(
                self.MESSAGE_ERROR_USER_NOT_FOUND
            )
            return

        if check_password(self.parser.password, user.password):
            await login(self.connection.scope, user)
        else:
            await self.send_chat_message(self.MESSAGE_ERROR_WRONG_PASSWORD)
            return

        # Notify all online users. Do this before login the user in to prevent such user from receiving this message
        await self.send_broadcast_message(self.MESSAGE_SUCCESS_BROADCAST.format(username=username))

        # Place user in a game location
        if user.location_id:
            await self.connection.channel_layer.group_add(
                str(user.location_id),
                self.connection.channel_name
            )
        else:
            await self.connection.channel_layer.group_add(
                'random_location',
                self.connection.channel_name
            )

        # Send messages
        await self.send_chat_message(
            self.MESSAGE_SUCCESS.format(username=username)
        )

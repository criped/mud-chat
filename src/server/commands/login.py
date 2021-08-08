from channels.auth import login, get_user
from channels.db import database_sync_to_async
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _

from contrib.mud_auth.models import User
from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin
from world.models import Room


class CommandLogin(CommandAbstract):
    ALIASES = ('login',)
    HELP = _('login <name> <password> - It lets you in the game :) You can also use `l` for shortcut')
    MESSAGE_ERROR_USER_NOT_FOUND = _('User not found')
    MESSAGE_ERROR_WRONG_PASSWORD = _('Incorrect password')
    MESSAGE_SUCCESS = _('Logged in successfully as {username}!')
    MESSAGE_SUCCESS_BROADCAST = _('User {username} is online')

    NOTIFICATION_SUCCESS = _('User {username} logged in successfully!')

    def __init__(self, connection, parser: CommandParserLogin, *args, **kwargs) -> None:
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
            room = await Room.get_room_by_id(user.location_id)
            await self.connection.channel_layer.group_add(
                str(room.id),
                self.connection.channel_name
            )
        else:
            room = await Room.get_default_room()
            await self.connection.channel_layer.group_add(
                str(room.id),
                self.connection.channel_name
            )
            await User.update_location(user, room.id)

        self.connection.scope['session']['current_location_id'] = room.id
        await database_sync_to_async(self.connection.scope['session'].save)()

        # Send messages
        await self.send_chat_message(
            self.MESSAGE_SUCCESS.format(username=username)
        )

    @classmethod
    async def is_available(cls, connection, *args, **kwargs) -> bool:
        user = await get_user(connection.scope)
        return type(user) == AnonymousUser

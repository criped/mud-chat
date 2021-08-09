import json

from channels.auth import get_user
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.translation import ugettext_lazy as _

from contrib.mud_auth.models import User
from server.commands.command_registry import CommandRegistry, CommandNotFoundException
from server.messages.base import Message
from server.messages.group import GroupMessage


class MUDConsumer(AsyncWebsocketConsumer):
    WELCOME_MESSAGE = _(
        "Welcome MUD server! Log in or register if you do not have an account yet. "
        "Enter `help` to see all the available commands."
    )

    async def connect(self):
        await super().connect()
        await self.chat_message(
            Message(self.WELCOME_MESSAGE).payload
        )

    async def disconnect(self, code):
        # Set user as offline when disconnected without logging out
        await User.set_is_online(await get_user(self.scope), False)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receives text from websocket connection and runs according command if the input provided is well formed.
        :param text_data: text received. JSON object containing the text entered by the user
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['text']
        available_command_classes = await CommandRegistry.get_available_commands(self)
        try:
            command_class, command_parser = CommandRegistry.get_command_from_message(message, available_command_classes)
        except CommandNotFoundException as exc:
            await self.chat_message(
                Message(str(exc)).payload
            )
        else:
            command = command_class(
                self,
                command_parser(message)
            )
            await command.run()

    async def chat_message(self, event):
        """
        Sends text to the user-specific websocket connection
        :param event: dictionary containing the entry text, which is the text to be sent.
        """
        message = event['text']

        # Send text to WebSocket
        await self.send(
            text_data=json.dumps(
                Message(message).payload
            )
        )

    async def chat_group_message(self, event):
        """
        Handles event sent in a group and sends it to the user
        :param event: dictionary containing the entry text, which is the text to be sent.
        """
        message = event['text']
        user = await get_user(self.scope)

        if user.username != event['username']:
            # Send text to WebSocket
            await self.send(
                text_data=json.dumps(
                    GroupMessage(message, event['username'], event['location']).payload
                )
            )

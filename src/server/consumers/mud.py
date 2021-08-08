import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.translation import ugettext_lazy as _

from server.commands.command_registry import CommandRegistry, CommandNotFoundException
from server.messages.base import Message


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
        await self.channel_layer.group_discard(
            "random_location",  # TODO: manage rooms
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receives text from websocket connection and runs according command if the input provided is well formed.
        :param text_data: text received. JSON object containing the text entered by the user
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['text']

        try:
            command_class, command_parser = CommandRegistry.get_command_from_message(message)
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

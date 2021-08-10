import json
from typing import List, Dict

from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase  # Use TransactionTestCase over TestCase because it keeps connection alive

from contrib.mud_auth.models import User
from main.asgi import application
from server.commands.login import CommandLogin
from server.consumers.mud import MUDConsumer


class IntegrationTestsCommandLogin(TransactionTestCase):
    PATH = 'mud/'
    LOCATION = 'random_room'

    COMMAND_NAME = 'login'
    USER_CREDENTIALS = ('test_username', 'test_pws')
    COMMAND_TEMPLATE_LOGIN = 'login {} {}'

    AMOUNT_OF_ONLINE_USERS = 5

    fixtures = ('world/fixtures/room.json', 'world/fixtures/room_exit.json')

    async def create_user(self, username=USER_CREDENTIALS[0], password=USER_CREDENTIALS[1]):
        self.user = await User.register_user(username, password)

    def get_event_message(self, message):
        return json.loads(message)['text']

    def send_event_message(self, message):
        return json.dumps({'text': message})

    async def get_events_to_be_received_by_communicator(self, communicator) -> List[dict]:
        events = []
        while not await communicator.receive_nothing():
            event = await communicator.receive_from()
            events.append(event)
        return communicator, events

    async def initialize_communicator(self) -> [WebsocketCommunicator, List[Dict]]:
        events = []
        communicator = WebsocketCommunicator(application, self.PATH)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        events.append(await communicator.receive_from())
        return communicator, events

    async def login_user_via_communicator(
            self,
            communicator,
            username=USER_CREDENTIALS[0],
            password=USER_CREDENTIALS[1]
    ) -> [WebsocketCommunicator, List[Dict]]:
        events = []
        await communicator.send_to(
            text_data=self.send_event_message(
                self.COMMAND_TEMPLATE_LOGIN.format(username, password)
            )
        )
        response = await communicator.receive_from()
        events.append(response)
        return communicator, events

    async def test_welcome_message(self):
        """
        Asserts users receive a welcome message when connected
        """
        communicator, events = await self.initialize_communicator()
        self.assertEqual(len(events), 1)
        self.assertEqual(
            self.get_event_message(events[0]),
            str(MUDConsumer.WELCOME_MESSAGE)
        )

        await communicator.disconnect()

    async def test_login_successful(self):
        """
        Asserts users are properly logged in
        """
        await self.create_user()
        communicator, _ = await self.initialize_communicator()
        communicator, events_login = await self.login_user_via_communicator(communicator)

        self.assertEqual(len(events_login), 1)
        self.assertEqual(
            self.get_event_message(events_login[0]),
            CommandLogin.MESSAGE_SUCCESS.format(username=self.user)
        )

        await communicator.disconnect()

    async def test_logged_in_users_receive_login_notification(self):
        """
        Asserts logged in users receive the notification about the last user who was logged in
        """

        # Connect and login many users
        online_users = []
        for i in range(self.AMOUNT_OF_ONLINE_USERS):
            username = f'test_username_{i}'
            password = f'test_pwd_{i}'
            await self.create_user(username, password)

            communicator, _ = await self.initialize_communicator()
            communicator, _ = await self.login_user_via_communicator(
                communicator,
                username=username,
                password=password
            )
            online_users.append(communicator)

        # Login a new one to trigger a new login notification for online users
        await self.create_user()

        communicator, _ = await self.initialize_communicator()
        communicator, _ = await self.login_user_via_communicator(communicator)

        # Assert the just logged in user does not receive the notification of its own login
        self.assertTrue(await communicator.receive_nothing())

        for online_user in online_users:
            # Get all the events, but only look at the last one, which should be the last login notification
            communicator, events = await self.get_events_to_be_received_by_communicator(online_user)
            self.assertEqual(
                self.get_event_message(events[-1]),
                CommandLogin.MESSAGE_SUCCESS_BROADCAST.format(username=self.USER_CREDENTIALS[0])
            )
            await online_user.disconnect()

        await communicator.disconnect()

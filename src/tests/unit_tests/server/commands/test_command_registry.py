from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.test import override_settings

from server.commands.command_registry import CommandRegistry
from server.commands.login import CommandLogin
from server.commands.logout import CommandLogout
from server.commands.parsers.parser_login import CommandParserLogin
from server.commands.parsers.parser_logout import CommandParserLogout
from server.commands.parsers.parser_register import CommandParserRegister
from server.commands.register import CommandRegister
from tests.utils import TestCommandAlwaysAvailable


class CommandRegistryTest(TestCase):
    TEST_MUD_COMMANDS_BASE = {
        'server.commands.login.CommandLogin': 'server.commands.parsers.parser_login.CommandParserLogin',
        'server.commands.register.CommandRegister': 'server.commands.parsers.parser_register.CommandParserRegister',
    }
    TEST_MUD_COMMANDS = {
        'server.commands.logout.CommandLogout': 'server.commands.parsers.parser_logout.CommandParserLogout',
    }

    # override command base so that new commands do not break it
    @override_settings(MUD_COMMANDS_BASE=TEST_MUD_COMMANDS_BASE)
    def test_registered_base_commands(self):
        """
        Asserts that the out-of-the-box command configurations are loaded
        """
        # Clear lru_cache to trigger it reload
        CommandRegistry.registered_commands.cache_clear()

        expected = {
            CommandLogin: CommandParserLogin,
            CommandRegister: CommandParserRegister,
        }
        self.assertEqual(
            CommandRegistry.registered_commands(),
            expected
        )
        # Clear lru_cache to avoid issues with other test cases
        CommandRegistry.registered_commands.cache_clear()

    @override_settings(MUD_COMMANDS_BASE=TEST_MUD_COMMANDS_BASE)
    @override_settings(MUD_COMMANDS=TEST_MUD_COMMANDS)
    def test_registered_base_commands_with_extended(self):
        """
        Asserts that the out-of-the-box command configurations are loaded and also extended ones
        """
        CommandRegistry.registered_commands.cache_clear()

        expected = {
            CommandLogin: CommandParserLogin,
            CommandRegister: CommandParserRegister,
            CommandLogout: CommandParserLogout
        }
        self.assertEqual(
            CommandRegistry.registered_commands(),
            expected
        )

        CommandRegistry.registered_commands.cache_clear()

    def test_get_command_from_message(self):
        """
        Asserts that correct command config is returned when a text message containing command name is entered
        """
        test_text_message = 'logout'

        expected_config = (CommandLogout, CommandParserLogout)
        command_config = CommandRegistry.get_command_from_message(
            test_text_message,
            [CommandLogout]
        )
        self.assertEqual(
            command_config[0],
            expected_config[0]
        )
        self.assertEqual(
            command_config[1],
            expected_config[1]
        )

    @patch('server.commands.command_registry.CommandRegistry.registered_commands')
    async def test_get_available_commands(self, mock_registered_commands):
        """
        Asserts that available commands are fetched according to their `is_available()` method
        """
        connection = MagicMock()
        expected_commands = [TestCommandAlwaysAvailable, TestCommandAlwaysAvailable]
        mock_registered_commands.return_value = expected_commands

        available_commands = await CommandRegistry.get_available_commands(connection)
        self.assertEqual(
            available_commands,
            expected_commands
        )

from asgiref.sync import sync_to_async
from django.utils.translation import ugettext_lazy as _

from server.commands.base import CommandAbstract
from server.commands import command_registry
from server.commands.parsers.parser_register import CommandParserRegister


class CommandHelp(CommandAbstract):
    ALIASES = ('help', 'h')
    HELP = _('help - It shows help about currently available commands.')
    MESSAGE_HELP_ALL_COMMANDS = _('These are the available commands and some help for them: \n{}')

    def __init__(self, connection, parser: CommandParserRegister, *args, **kwargs) -> None:
        super().__init__(connection, parser)
        self.available_commands = command_registry.CommandRegistry.get_available_commands(connection)

    async def compose_help_message(self):
        return self.MESSAGE_HELP_ALL_COMMANDS.format(
            '\n'.join([f' - {command.HELP}' for command in await self.available_commands])
        )

    async def run(self) -> None:
        """
        Gets help of all available commands and sends a chat message to the user that requested it
        """

        commands_help = await self.compose_help_message()

        await self.send_chat_message(commands_help)

    @classmethod
    async def is_available(cls, connection, *args, **kwargs) -> bool:
        return await sync_to_async(lambda: True)()

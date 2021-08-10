from asgiref.sync import sync_to_async

from server.commands.base import CommandAbstract


class TestCommandAlwaysAvailable(CommandAbstract):
    def __init__(self, connection, parser, *args, **kwargs) -> None:
        self.connection = connection
        self.parser = parser

    async def run(self) -> None:
        pass

    @classmethod
    async def is_available(cls, connection, *args, **kwargs) -> bool:
        return await sync_to_async(lambda: True)()

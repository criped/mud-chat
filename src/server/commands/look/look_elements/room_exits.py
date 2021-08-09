from server.commands.look.look_elements.base import LookElementAbstract
from world.models import RoomExit


class LookElementRoomExits(LookElementAbstract):
    EXIT_SEPARATOR = ', '
    TEMPLATE = 'Exit: {exit_names}\n'

    def __init__(self, connection, *args, **kwargs):
        self.connection = connection

    async def get_element_str(self) -> str:
        exit_names = await RoomExit.get_exit_names(
            self.connection.scope['session']['current_location_id']
        )
        return self.TEMPLATE.format(
            exit_names=self.EXIT_SEPARATOR.join(exit_names)
        )

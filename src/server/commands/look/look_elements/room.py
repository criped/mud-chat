from server.commands.look.look_elements.base import LookElementAbstract
from world.models import Room


class LookElementRoom(LookElementAbstract):
    TEMPLATE = '{room_name}\n\n{room_description}\n\n'

    def __init__(self, connection, *args, **kwargs):
        self.connection = connection

    async def get_element_str(self) -> str:
        room = await Room.get_room_by_id(
            self.connection.scope['session']['current_location_id']
        )
        return self.TEMPLATE.format(
            room_name=room.name,
            room_description=room.desc
        )

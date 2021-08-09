from typing import List

from channels.db import database_sync_to_async
from django.db import models
from django.utils.translation import ugettext_lazy as _

from world.models import Room


class RoomExit(models.Model):

    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_(
            "Name of the room"
        ),
    )
    location = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='exit_locations',
        help_text=_('Room to exit from'),
    )
    destination = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='exit_destinations',
        help_text=_('Room to exit to'),
    )

    @classmethod
    @database_sync_to_async
    def check_exit(cls, room_id: int, direction: str):
        return cls.objects.filter(
            location=room_id,
            name=direction
        ).exists()

    @classmethod
    @database_sync_to_async
    def get_exit_destination(cls, room_id: int, direction: str):
        return cls.objects.get(
            location=room_id,
            name=direction
        ).destination

    @classmethod
    @database_sync_to_async
    def get_exit_names(cls, room_id: int) -> List[str]:
        return list(cls.objects.filter(
            location=room_id,
        ).order_by(
            'name'
        ).values_list(
            'name',
            flat=True
        ))

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

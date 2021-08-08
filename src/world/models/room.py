from channels.db import database_sync_to_async
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Room(models.Model):
    desc = models.TextField(
        _('Description'),
        help_text=_(
            "Description of the room"
        ),
    )

    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_(
            "Name of the room"
        ),
    )

    @classmethod
    @database_sync_to_async
    def get_default_room(cls):
        return cls.objects.all().order_by('id').first()

    @classmethod
    @database_sync_to_async
    def get_room_by_id(cls, room_id: int):
        return cls.objects.get(pk=room_id)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

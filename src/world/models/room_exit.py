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

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

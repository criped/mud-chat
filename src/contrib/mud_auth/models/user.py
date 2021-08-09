from typing import List

from channels.db import database_sync_to_async
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Custom User model which allows Django User model to be extended
    """

    location_id = models.IntegerField(
        _('Location ID'),
        null=True,
        blank=True,
        help_text=_(
            "Current location of the user if it is online in the game. "
            "Otherwise, location where it was last time it logged out."
        ),
    )

    is_online = models.BooleanField(
        _('Is online'),
        default=False,
        help_text=_(
            "Whether the user is online in the game"
        ),
    )

    @classmethod
    @database_sync_to_async
    def register_user(cls, username, password):
        return cls.objects.create_user(username=username, password=password)

    @classmethod
    @database_sync_to_async
    def get_by_username(cls, username):
        return cls.objects.get(username=username)

    @classmethod
    @database_sync_to_async
    def check_exists(cls, username) -> bool:
        return cls.objects.filter(username=username).exists()

    @classmethod
    @database_sync_to_async
    def update_location(cls, user, location_id: int):
        user.location_id = location_id
        user.save(update_fields=['location_id'])
        return user

    @classmethod
    @database_sync_to_async
    def get_online_usernames_in_location(cls, location_id: int) -> List[str]:
        return list(cls.objects.filter(
            is_online=True,
            location_id=location_id
        ).order_by(
            'username'
        ).values_list(
            'username',
            flat=True
        ))

    @classmethod
    @database_sync_to_async
    def set_is_online(cls, user, is_online: int = True) -> List[str]:
        user.is_online = is_online
        return user.save(update_fields=['is_online'])

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

from channels.db import database_sync_to_async
from django.contrib.auth.models import AbstractUser
from django.db.models import IntegerField

from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Custom User model which allows Django User model to be extended
    """

    location_id = IntegerField(
        _('Location ID'),
        null=True,
        blank=True,
        help_text=_(
            "Current location of the user if it is online in the game. "
            "Otherwise, location where it was last time it logged out."
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
    def update_location(cls, username, location_id: int):
        user =  cls.objects.get(username=username)
        user.location_id = location_id
        user.save(update_fields=['location_id'])
        return user

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

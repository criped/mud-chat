from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Custom User model which allows Django User model to be extended
    """

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

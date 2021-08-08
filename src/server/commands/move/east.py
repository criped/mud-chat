from django.utils.translation import ugettext_lazy as _

from server.commands.move.base import CommandBaseMove


class CommandEast(CommandBaseMove):
    ALIASES = ('east', 'e')
    HELP = _('east - Move to a room located in the east. Use `e` for shortcut')
    DIRECTION = ALIASES[0]

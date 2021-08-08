from django.utils.translation import ugettext_lazy as _

from server.commands.move.base import CommandBaseMove


class CommandNorth(CommandBaseMove):
    ALIASES = ('north', 'n')
    HELP = _('north - Move to a room located in the north. Use `n` for shortcut')
    DIRECTION = ALIASES[0]

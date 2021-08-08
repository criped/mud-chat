from django.utils.translation import ugettext_lazy as _

from server.commands.move.base import CommandBaseMove


class CommandSouth(CommandBaseMove):
    ALIASES = ('south', 's')
    HELP = _('south - Move to a room located in the south. Use `s` for shortcut')
    DIRECTION = ALIASES[0]

from django.utils.translation import ugettext_lazy as _

from server.commands.move.base import CommandBaseMove


class CommandWest(CommandBaseMove):
    ALIASES = ('west', 'w')
    HELP = _('west - Move to a room located in the west. Use `w` for shortcut')
    DIRECTION = ALIASES[0]

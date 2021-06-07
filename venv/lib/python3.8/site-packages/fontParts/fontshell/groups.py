import defcon
from fontParts.base import BaseGroups
from fontParts.fontshell.base import RBaseObject


class RGroups(RBaseObject, BaseGroups):

    wrapClass = defcon.Groups

    def _get_side1KerningGroups(self):
        return self.naked().getRepresentation("defcon.groups.kerningSide1Groups")

    def _get_side2KerningGroups(self):
        return self.naked().getRepresentation("defcon.groups.kerningSide2Groups")

    def _items(self):
        return self.naked().items()

    def _contains(self, key):
        return key in self.naked()

    def _setItem(self, key, value):
        self.naked()[key] = list(value)

    def _getItem(self, key):
        return self.naked()[key]

    def _delItem(self, key):
        del self.naked()[key]

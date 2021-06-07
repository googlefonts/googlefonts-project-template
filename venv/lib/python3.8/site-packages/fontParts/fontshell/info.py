import defcon
from fontParts.base import BaseInfo
from fontParts.fontshell.base import RBaseObject


class RInfo(RBaseObject, BaseInfo):

    wrapClass = defcon.Info

    def _getAttr(self, attr):
        return getattr(self.naked(), attr)

    def _setAttr(self, attr, value):
        setattr(self.naked(), attr, value)

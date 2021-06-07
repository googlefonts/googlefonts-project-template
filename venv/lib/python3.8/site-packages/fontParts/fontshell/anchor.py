import defcon
from fontParts.base import BaseAnchor
from fontParts.fontshell.base import RBaseObject


class RAnchor(RBaseObject, BaseAnchor):

    wrapClass = defcon.Anchor

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
            wrap.x = 0
            wrap.y = 0
        super(RAnchor, self)._init(wrap=wrap)

    # --------
    # Position
    # --------

    # x

    def _get_x(self):
        return self.naked().x

    def _set_x(self, value):
        self.naked().x = value

    # y

    def _get_y(self):
        return self.naked().y

    def _set_y(self, value):
        self.naked().y = value

    # --------------
    # Identification
    # --------------

    # identifier

    def _get_identifier(self):
        anchor = self.naked()
        return anchor.identifier

    def _getIdentifier(self):
        anchor = self.naked()
        return anchor.generateIdentifier()

    def _setIdentifier(self, value):
        self.naked().identifier = value

    # name

    def _get_name(self):
        return self.naked().name

    def _set_name(self, value):
        self.naked().name = value

    # color

    def _get_color(self):
        value = self.naked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(self, value):
        self.naked().color = value

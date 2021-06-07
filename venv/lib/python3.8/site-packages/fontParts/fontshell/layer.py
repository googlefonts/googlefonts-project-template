import defcon
from fontParts.base import BaseLayer
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.lib import RLib
from fontParts.fontshell.glyph import RGlyph


class RLayer(RBaseObject, BaseLayer):

    wrapClass = defcon.Layer
    libClass = RLib
    glyphClass = RGlyph

    # -----------
    # Sub-Objects
    # -----------

    # lib

    def _get_lib(self):
        return self.libClass(wrap=self.naked().lib)

    # --------------
    # Identification
    # --------------

    # name

    def _get_name(self):
        return self.naked().name

    def _set_name(self, value, **kwargs):
        self.naked().name = value

    # color

    def _get_color(self):
        value = self.naked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(self, value, **kwargs):
        self.naked().color = value

    # -----------------
    # Glyph Interaction
    # -----------------

    def _getItem(self, name, **kwargs):
        layer = self.naked()
        glyph = layer[name]
        return self.glyphClass(glyph)

    def _keys(self, **kwargs):
        return self.naked().keys()

    def _newGlyph(self, name, **kwargs):
        layer = self.naked()
        layer.newGlyph(name)
        return self[name]

    def _removeGlyph(self, name, **kwargs):
        layer = self.naked()
        del layer[name]

    # -------
    # mapping
    # -------

    def _getReverseComponentMapping(self):
        return self.naked().componentReferences

    def _getCharacterMapping(self):
        return self.naked().unicodeData

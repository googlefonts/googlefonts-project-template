from fontParts.base.lib import BaseLib


class Lib(BaseLib):

    def __init__(self, **kwargs):
        self._dict = {}
        super(BaseLib, self).__init__(self, **kwargs)

    def _set_glyph(self, glyph):
        self._dict["glyph"] = glyph

    def _getItem(self, attr):
        if not attr in self._dict:
            return None
        return self._dict[attr]

    def _setItem(self, attr, value):
        self._dict[attr] = value

    def _items(self):
        return self._dict.items()

    def _contains(self, attr):
        return attr in self._dict

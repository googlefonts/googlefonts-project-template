from fontParts.base.image import BaseImage
from babelfont import addUnderscoreProperty

@addUnderscoreProperty("data")
class Image(BaseImage):

    def __init__(self, **kwargs):
        self._dict = {}
        super(BaseImage, self).__init__(self, **kwargs)

    def _getAttr(self, attr):
        if not attr in self._dict:
            return None
        return self._dict[attr]

    def _setAttr(self, attr, value):
        self._dict[attr] = value

from fontParts.base.info import BaseInfo
from babelfont import addUnderscoreProperty

@addUnderscoreProperty("font")
class Info(BaseInfo):

    def __init__(self, **kwargs):
        self._dict = {}
        super(BaseInfo, self).__init__(self, **kwargs)

    def _getAttr(self, attr):
        if not attr in self._dict:
            return None
        return self._dict[attr]

    def _setAttr(self, attr, value):
        self._dict[attr] = value

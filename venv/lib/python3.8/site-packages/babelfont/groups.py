from fontParts.base.groups import BaseGroups
from collections import OrderedDict


class Groups(BaseGroups):

    def __init__(self, **kwargs):
        self._dict = OrderedDict()
        super(BaseGroups, self).__init__(self, **kwargs)

    def _set_font(self, font):
        self._font = font

    def _getItem(self, attr):
        if not attr in self._dict:
            return None
        return self._dict[attr]

    def _setItem(self, attr, value):
        self._dict[attr] = value

    def _contains(self, attr):
        return attr in self._dict

    def _items(self):
        return self._dict.items()

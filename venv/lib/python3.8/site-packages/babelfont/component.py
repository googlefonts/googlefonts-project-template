from fontParts.base.component import BaseComponent
from babelfont import addUnderscoreProperty
from babelfont.glyph import Glyph


@addUnderscoreProperty("baseGlyph")
@addUnderscoreProperty("glyph")
@addUnderscoreProperty("transformation")
@addUnderscoreProperty("identifier")
class Component(BaseComponent):
    def _init(self, **kwargs):
        self._transformation = (1, 0, 0, 1, 0, 0)
        self._identifier = None
        pass
    pass
    # XXX _set_index

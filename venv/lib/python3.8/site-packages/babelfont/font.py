from fontParts.base.font import BaseFont
from babelfont.lib import Lib
from babelfont import addUnderscoreProperty
from babelfont.glyph import Glyph
from babelfont.groups import Groups
from babelfont.info import Info
from babelfont.layer import Layer
from babelfont.features import Features
from babelfont.kerning import Kerning
from babelfont import Babelfont


@addUnderscoreProperty("path")
@addUnderscoreProperty("format")
@addUnderscoreProperty("info")
@addUnderscoreProperty("groups")
@addUnderscoreProperty("kerning")
@addUnderscoreProperty("features")
@addUnderscoreProperty("lib")
@addUnderscoreProperty("layers")
@addUnderscoreProperty("layerOrder")
class Font(BaseFont):
    def _init(self, **kwargs):
        self._layerOrder = []
        self._layers = []
        self._info = Info()
        self._info.font = self
        self._groups = Groups()
        self._kerning = Kerning()
        self._features = Features()
        self._lib = Lib()
        self._unicodemap = None
        self._reversedunicodemap = None

    def __eq__(self, other):
        return NotImplemented

    def _save(self, path=None, **kwargs):
        if not path:
            path = self._path
        if not path:
            raise ValueError
        Babelfont.save(self, path)

    def _close(self, **kwargs):
        pass

    def _keys(self, **kwargs):
        if len(self._layers) > 0:
            return self.defaultLayer.keys()
        return []

    def exportedGlyphs(self):
        return [ k for k in self.defaultLayer.keys() if self[k].exported ]

    def _get_defaultLayerName(self):
        if len(self._layers) > 0:
            return self._layers[0].name
        return None

    def _set_defaultLayerName(self, name):
        self._layers[0].name = name

    def _newLayer(self, name, color, **kwargs):
        layer = Layer()
        layer.name = name
        self._layers.append(layer)
        self._layerOrder.append(name)
        return layer

    def _removeLayer(self, name, **kwargs):
        self._layers = [ l for l in self._layers if l.name != name ]

    def _build_maps(self):
        if self._unicodemap is None or self._reversedunicodemap is None:
            self._unicodemap = {}
            self._reversedunicodemap = {}
            for g in self:
                if g.unicodes:
                    self._reversedunicodemap[g.name] = g.unicodes[0]
                for cp in g.unicodes:
                    self._unicodemap[cp] = g.name
            if ".notdef" in self:
                self._unicodemap[0] = ".notdef"
            else:
                self._unicodemap[0] = self.glyphOrder[0]

    def _get_glyphOrder(self):
        return self.lib.glyphOrder

    def glyphForCodepoint(self, u, fallback=True):
        self._build_maps()
        if fallback:
            return self._unicodemap.get(u, self._unicodemap[0])
        else:
            return self._unicodemap.get(u, None)

    def codepointForGlyph(self, g):
        self._build_maps()
        return self._reversedunicodemap.get(g, 0)

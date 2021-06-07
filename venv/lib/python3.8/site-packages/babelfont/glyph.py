from fontParts.base.glyph import BaseGlyph
from babelfont.image import Image
from babelfont import addUnderscoreProperty
from babelfont.lib import Lib
from babelfont.anchor import Anchor


# @addUnderscoreProperty(["name", "unicodes", "width", "height", "lib"])
@addUnderscoreProperty("name")
@addUnderscoreProperty("unicodes")
@addUnderscoreProperty("guidelines")
@addUnderscoreProperty("image")
@addUnderscoreProperty("width")
@addUnderscoreProperty("height")
@addUnderscoreProperty("lib")
@addUnderscoreProperty("note")
@addUnderscoreProperty("markColor")
class Glyph(BaseGlyph):
    def _init(self, *args, **kwargs):
        self._lib = Lib()
        self._components = []
        self._anchors = []
        self._unicodes = []
        self._guidelines = []
        self._contours = []
        self._image = Image()
        self.exported = True
        self._width = 0
        self._height = 0
        self._note = ""
        self._markColor = None

    def _autoUnicodes(self):
        # Maybe someday
        self.raiseNotImplementedError()

    def _get_lib(self):
        return self._lib

    def _lenContours(self):
        return len(self._contours)

    def _lenGuidelines(self):
        return 0

    def _clearImage(self):
        self._image = Image()

    def _getContour(self, index, **kwargs):
        return self._contours[index]

    def _appendContour(self, contour, offset=None, **kwargs):
        copy = contour.copy()
        if offset != (0, 0):
            copy.moveBy(offset)
        copy._glyph = self
        self._contours.append(copy)

    def _removeContour(self, index, **kwargs):
        del(self._contours[index])


    def _lenComponents(self):
        return len(self._components)

    def _getComponent(self, index, **kwargs):
        return self._components[index]

    def _removeComponent(self, index, **kwargs):
        del(self._components[index])


    def _lenAnchors(self):
        return len(self._anchors)

    def _getAnchor(self, index, **kwargs):
        return self._anchors[index]

    def _removeAnchor(self, index, **kwargs):
        del(self._anchors[index])

    def _appendAnchor(self, name, **kwargs):
        self._anchors.append(Anchor(name=name, **kwargs))

    # Babelfont glyphs have a category, even if fontParts ones don't
    @property
    def category(self):
        if "public.openTypeCategory" in self.lib:
            return self.lib["public.openTypeCategory"]

    def set_category(self, category):
        assert(category in ["ligature", "mark", "base"])
        self.lib["public.openTypeCategory"] = category
        if category == "ligature" and \
            "com.schriftgestaltung.Glyphs.category" not in self.lib:
            self.lib["com.schriftgestaltung.Glyphs.category"] = "Letter"
            self.lib["com.schriftgestaltung.Glyphs.subcategory"] = "Ligature"
        elif category == "mark" and \
            "com.schriftgestaltung.Glyphs.category" not in self.lib:
            self.lib["com.schriftgestaltung.Glyphs.category"] = "Mark"
        elif category == "base" and \
            "com.schriftgestaltung.Glyphs.category" not in self.lib:
            self.lib["com.schriftgestaltung.Glyphs.category"] = "Letter"

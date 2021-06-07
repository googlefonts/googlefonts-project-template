from fontParts.base.contour import BaseContour
from fontParts.fontshell.segment import RSegment # Fine until fontshell splits...
from babelfont import addUnderscoreProperty
from babelfont.point import Point


@addUnderscoreProperty("clockwise")
class Contour(BaseContour):
    segmentClass = RSegment
    def _init(self, **kwargs):
        self._points = []
    def _lenPoints(self):
        return len(self._points)

    def _getPoint(self, index, **kwargs):
        return self._points[index]

    def _get_glyph(self):
        return self._glyph

    def _correct_direction(self):
        signedArea = 0
        for ix, p in enumerate(self._points):
            if ix + 1 >= len(self._points):
                nextPt = self._points[0]
            else:
                nextPt = self._points[ix+1]
            signedArea = signedArea + (p.x * nextPt.y - nextPt.x * p.y)
        if signedArea > 0:
            self.clockwise = False
        else:
            self.clockwise = True

    def _insertPoint(self, index, position, type=None, smooth=None,
                     name=None, identifier=None, **kwargs):
        point = Point()
        point.x = position[0]
        point.y = position[1]
        point.type = type
        point.smooth = smooth
        point.name = name
        self._points.insert(index, point)

    @property
    def identifier(self):
        return None


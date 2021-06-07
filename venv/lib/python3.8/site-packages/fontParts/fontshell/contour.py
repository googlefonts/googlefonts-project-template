import defcon
from fontParts.base import BaseContour
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.point import RPoint
from fontParts.fontshell.segment import RSegment
from fontParts.fontshell.bPoint import RBPoint


class RContour(RBaseObject, BaseContour):

    wrapClass = defcon.Contour
    pointClass = RPoint
    segmentClass = RSegment
    bPointClass = RBPoint

    # --------------
    # Identification
    # --------------

    # index

    def _set_index(self, value):
        contour = self.naked()
        glyph = contour.glyph
        glyph.removeContour(contour)
        glyph.insertContour(value, contour)

    # identifier

    def _get_identifier(self):
        contour = self.naked()
        return contour.identifier

    def _getIdentifier(self):
        contour = self.naked()
        return contour.generateIdentifier()

    def _getIdentifierforPoint(self, point):
        contour = self.naked()
        point = point.naked()
        return contour.generateIdentifierForPoint(point)

    # ----
    # Open
    # ----

    def _get_open(self):
        return self.naked().open

    # ------
    # Bounds
    # ------

    def _get_bounds(self):
        return self.naked().bounds

    # ----
    # Area
    # ----

    def _get_area(self):
        return self.naked().area

    # ---------
    # Direction
    # ---------

    def _get_clockwise(self):
        return self.naked().clockwise

    def _reverseContour(self, **kwargs):
        self.naked().reverse()

    # ------------------------
    # Point and Contour Inside
    # ------------------------

    def _pointInside(self, point):
        return self.naked().pointInside(point)

    def _contourInside(self, otherContour):
        return self.naked().contourInside(otherContour.naked(), segmentLength=5)

    # ------
    # Points
    # ------

    def _lenPoints(self, **kwargs):
        return len(self.naked())

    def _getPoint(self, index, **kwargs):
        contour = self.naked()
        point = contour[index]
        return self.pointClass(point)

    def _insertPoint(self, index, position, type=None, smooth=None,
                     name=None, identifier=None, **kwargs):
        point = self.pointClass()
        point.x = position[0]
        point.y = position[1]
        point.type = type
        point.smooth = smooth
        point.name = name
        point = point.naked()
        point.identifier = identifier
        self.naked().insertPoint(index, point)

    def _removePoint(self, index, preserveCurve, **kwargs):
        contour = self.naked()
        point = contour[index]
        contour.removePoint(point)

from __future__ import absolute_import, print_function, division

from fontTools.pens.basePen import BasePen
from fontTools.misc.bezierTools import splitLine, splitCubic


class MarginPen(BasePen):
    """
    Pen to calculate the margins at a given height or width.

    - isHorizontal = True: slice the glyph at y=value.
    - isHorizontal = False: slice the glyph at x=value.

    Possible optimisation:
    Initialise the pen object with a list of points we want to measure,
    then draw the glyph once, but do the splitLine() math for all measure points.
    """

    def __init__(self, glyphSet, value, isHorizontal=True):
        BasePen.__init__(self, glyphSet)
        self.value = value
        self.hits = {}
        self.filterDoubles = True
        self.contourIndex = None
        self.startPt = None
        self.currentPt = None
        self.isHorizontal = isHorizontal

    def _moveTo(self, pt):
        self.currentPt = pt
        self.startPt = pt
        if self.contourIndex is None:
            self.contourIndex = 0
        else:
            self.contourIndex += 1

    def _lineTo(self, pt):
        if self.filterDoubles:
            if pt == self.currentPt:
                return
        hits = splitLine(self.currentPt, pt, self.value, self.isHorizontal)
        if len(hits) > 1:
            # result will be 2 tuples of 2 coordinates
            # first two points: start to intersect
            # second two points: intersect to end
            # so, second point in first tuple is the intersect
            # then, the first coordinate of that point is the x.
            if self.contourIndex not in self.hits:
                self.hits[self.contourIndex] = []
            if self.isHorizontal:
                self.hits[self.contourIndex].append(round(hits[0][-1][0], 4))
            else:
                self.hits[self.contourIndex].append(round(hits[0][-1][1], 4))
        if self.isHorizontal and pt[1] == self.value:
            # it could happen
            if self.contourIndex not in self.hits:
                self.hits[self.contourIndex] = []
            self.hits[self.contourIndex].append(pt[0])
        elif (not self.isHorizontal) and (pt[0] == self.value):
            # it could happen
            if self.contourIndex not in self.hits:
                self.hits[self.contourIndex] = []
            self.hits[self.contourIndex].append(pt[1])
        self.currentPt = pt

    def _curveToOne(self, pt1, pt2, pt3):
        hits = splitCubic(self.currentPt, pt1, pt2, pt3, self.value, self.isHorizontal)
        for i in range(len(hits) - 1):
            # a number of intersections is possible. Just take the
            # last point of each segment.
            if self.contourIndex not in self.hits:
                self.hits[self.contourIndex] = []
            if self.isHorizontal:
                self.hits[self.contourIndex].append(round(hits[i][-1][0], 4))
            else:
                self.hits[self.contourIndex].append(round(hits[i][-1][1], 4))
        if self.isHorizontal and pt3[1] == self.value:
            # it could happen
            if self.contourIndex not in self.hits:
                self.hits[self.contourIndex] = []
            self.hits[self.contourIndex].append(pt3[0])
        if (not self.isHorizontal) and (pt3[0] == self.value):
            # it could happen
            if self.contourIndex not in self.hits:
                self.hits[self.contourIndex] = []
            self.hits[self.contourIndex].append(pt3[1])
        self.currentPt = pt3

    def _closePath(self):
        if self.currentPt != self.startPt:
            self._lineTo(self.startPt)
        self.currentPt = self.startPt = None

    def _endPath(self):
        self.currentPt = None

    def addComponent(self, baseGlyph, transformation):
        if self.glyphSet is None:
            return
        if baseGlyph in self.glyphSet:
            glyph = self.glyphSet[baseGlyph]
        if glyph is not None:
            glyph.draw(self)

    def getMargins(self):
        """
        Return the extremes of the slice for all contours combined, i.e. the whole glyph.
        """
        allHits = []
        for index, pts in self.hits.items():
            allHits.extend(pts)
        if allHits:
            return min(allHits), max(allHits)
        return None

    def getContourMargins(self):
        """
        Return the extremes of the slice for each contour.
        """
        allHits = {}
        for index, pts in self.hits.items():
            unique = list(set(pts))
            unique.sort()
            allHits[index] = unique
        return allHits

    def getAll(self):
        """
        Return all the slices.
        """
        allHits = []
        for index, pts in self.hits.items():
            allHits.extend(pts)
        unique = list(set(allHits))
        unique.sort()
        return unique


# =========
# = tests =
# =========

def _makeTestGlyph():
    # make a simple glyph that we can test the pens with.
    from fontParts.fontshell import RGlyph
    testGlyph = RGlyph()
    testGlyph.name = "testGlyph"
    testGlyph.width = 1000
    pen = testGlyph.getPen()
    pen.moveTo((100, 100))
    pen.lineTo((900, 100))
    pen.lineTo((900, 800))
    pen.lineTo((100, 800))
    # a curve
    pen.curveTo((120, 700), (120, 300), (100, 100))
    pen.closePath()
    # pen.addComponent("a", (1, 0, 0, 1, 0, 0))
    return testGlyph


def _testMarginPen():
    """
    >>> from fontPens.printPen import PrintPen
    >>> glyph = _makeTestGlyph()
    >>> pen = MarginPen(dict(), 200, isHorizontal=True)
    >>> glyph.draw(pen)
    >>> pen.getAll()
    [107.5475, 900.0]
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

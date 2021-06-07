from __future__ import absolute_import, print_function, division

from fontTools.pens.basePen import AbstractPen

from fontPens.penTools import distance


class ThresholdPen(AbstractPen):
    """
    This pen only draws segments longer in length than the threshold value.

    - otherPen: a different segment pen object this filter should draw the results with.
    - threshold: the minimum length of a segment
    """

    def __init__(self, otherPen, threshold=10):
        self.threshold = threshold
        self._lastPt = None
        self.otherPen = otherPen

    def moveTo(self, pt):
        self._lastPt = pt
        self.otherPen.moveTo(pt)

    def lineTo(self, pt, smooth=False):
        if self.threshold <= distance(pt, self._lastPt):
            self.otherPen.lineTo(pt)
            self._lastPt = pt

    def curveTo(self, pt1, pt2, pt3):
        if self.threshold <= distance(pt3, self._lastPt):
            self.otherPen.curveTo(pt1, pt2, pt3)
            self._lastPt = pt3

    def qCurveTo(self, *points):
        if self.threshold <= distance(points[-1], self._lastPt):
            self.otherPen.qCurveTo(*points)
            self._lastPt = points[-1]

    def closePath(self):
        self.otherPen.closePath()

    def endPath(self):
        self.otherPen.endPath()

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)


def thresholdGlyph(aGlyph, threshold=10):
    """
    Convenience function that applies the **ThresholdPen** to a glyph in place.
    """
    from fontTools.pens.recordingPen import RecordingPen
    recorder = RecordingPen()
    filterpen = ThresholdPen(recorder, threshold)
    aGlyph.draw(filterpen)
    aGlyph.clear()
    recorder.replay(aGlyph.getPen())
    return aGlyph


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
    pen.lineTo((900, 109))
    pen.lineTo((900, 800))
    pen.lineTo((100, 800))
    pen.closePath()
    pen.addComponent("a", (1, 0, 0, 1, 0, 0))
    return testGlyph


def _testThresholdPen():
    """
    >>> from fontPens.printPen import PrintPen
    >>> glyph = _makeTestGlyph()
    >>> pen = ThresholdPen(PrintPen())
    >>> glyph.draw(pen)
    pen.moveTo((100, 100))
    pen.lineTo((900, 100))
    pen.lineTo((900, 800))
    pen.lineTo((100, 800))
    pen.closePath()
    pen.addComponent('a', (1.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    """


def _testThresholdGlyph():
    """
    >>> from fontPens.printPen import PrintPen
    >>> glyph = _makeTestGlyph()
    >>> thresholdGlyph(glyph) #doctest: +ELLIPSIS
    <RGlyph...
    >>> glyph.draw(PrintPen())
    pen.moveTo((100, 100))
    pen.lineTo((900, 100))
    pen.lineTo((900, 800))
    pen.lineTo((100, 800))
    pen.closePath()
    pen.addComponent('a', (1.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

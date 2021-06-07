from __future__ import absolute_import, print_function, division

from fontTools.pens.pointPen import AbstractPointPen

from fontPens.penTools import distance


class ThresholdPointPen(AbstractPointPen):
    """
    Rewrite of the ThresholdPen as a PointPen
    so that we can preserve named points and other arguments.
    This pen will add components from the original glyph, but
    but it won't filter those components.

    "move", "line", "curve" or "qcurve"
    """

    def __init__(self, otherPointPen, threshold=10):
        self.threshold = threshold
        self._lastPt = None
        self._offCurveBuffer = []
        self.otherPointPen = otherPointPen

    def beginPath(self, identifier=None):
        """Start a new sub path."""
        self.otherPointPen.beginPath(identifier)
        self._lastPt = None

    def endPath(self):
        """End the current sub path."""
        self.otherPointPen.endPath()

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        """Add a point to the current sub path."""
        if segmentType in ['curve', 'qcurve']:
            # it's an offcurve, let's buffer them until we get another oncurve
            # and we know what to do with them
            self._offCurveBuffer.append((pt, segmentType, smooth, name, kwargs))
            return

        elif segmentType == "move":
            # start of an open contour
            self.otherPointPen.addPoint(pt, segmentType, smooth, name)  # how to add kwargs?
            self._lastPt = pt
            self._offCurveBuffer = []

        elif segmentType == "line":
            if self._lastPt is None:
                self.otherPointPen.addPoint(pt, segmentType, smooth, name)  # how to add kwargs?
                self._lastPt = pt
            elif distance(pt, self._lastPt) >= self.threshold:
                # we're oncurve and far enough from the last oncurve
                if self._offCurveBuffer:
                    # empty any buffered offcurves
                    for buf_pt, buf_segmentType, buf_smooth, buf_name, buf_kwargs in self._offCurveBuffer:
                        self.otherPointPen.addPoint(buf_pt, buf_segmentType, buf_smooth, buf_name)  # how to add kwargs?
                    self._offCurveBuffer = []
                # finally add the oncurve.
                self.otherPointPen.addPoint(pt, segmentType, smooth, name)  # how to add kwargs?
                self._lastPt = pt
            else:
                # we're too short, so we're not going to make it.
                # we need to clear out the offcurve buffer.
                self._offCurveBuffer = []

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        """Add a sub glyph. Note: this way components are not filtered."""
        self.otherPointPen.addComponent(baseGlyphName, transformation, identifier)


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
    >>> from fontPens.printPointPen import PrintPointPen
    >>> from random import seed
    >>> seed(100)
    >>> glyph = _makeTestGlyph()
    >>> pen = ThresholdPointPen(PrintPointPen())
    >>> glyph.drawPoints(pen)
    pen.beginPath()
    pen.addPoint((100, 100), segmentType='line')
    pen.addPoint((900, 100), segmentType='line')
    pen.addPoint((900, 800), segmentType='line')
    pen.addPoint((100, 800), segmentType='line')
    pen.endPath()
    pen.addComponent('a', (1.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

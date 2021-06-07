from __future__ import absolute_import, print_function, division

from fontTools.misc.bezierTools import calcQuadraticArcLength
from fontTools.pens.basePen import BasePen

from fontPens.penTools import estimateCubicCurveLength, distance, interpolatePoint, getCubicPoint, getQuadraticPoint


class FlattenPen(BasePen):
    """
    This filter pen processes the contours into a series of straight lines by flattening the curves.

    - otherPen: a different segment pen object this filter should draw the results with.
    - approximateSegmentLength: the length you want the flattened segments to be (roughly).
    - segmentLines: whether to cut straight lines into segments as well.
    - filterDoubles: don't draw if a segment goes to the same coordinate.
    """

    def __init__(self, otherPen, approximateSegmentLength=5, segmentLines=False, filterDoubles=True):
        self.approximateSegmentLength = approximateSegmentLength
        BasePen.__init__(self, {})
        self.otherPen = otherPen
        self.currentPt = None
        self.firstPt = None
        self.segmentLines = segmentLines
        self.filterDoubles = filterDoubles

    def _moveTo(self, pt):
        self.otherPen.moveTo(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        if self.filterDoubles:
            if pt == self.currentPt:
                return
        if not self.segmentLines:
            self.otherPen.lineTo(pt)
            self.currentPt = pt
            return
        d = distance(self.currentPt, pt)
        maxSteps = int(round(d / self.approximateSegmentLength))
        if maxSteps < 1:
            self.otherPen.lineTo(pt)
            self.currentPt = pt
            return
        step = 1.0 / maxSteps
        for factor in range(1, maxSteps + 1):
            self.otherPen.lineTo(interpolatePoint(self.currentPt, pt, factor * step))
        self.currentPt = pt

    def _curveToOne(self, pt1, pt2, pt3):
        falseCurve = (pt1 == self.currentPt) and (pt2 == pt3)
        if falseCurve:
            self._lineTo(pt3)
            return
        est = estimateCubicCurveLength(self.currentPt, pt1, pt2, pt3) / self.approximateSegmentLength
        maxSteps = int(round(est))
        if maxSteps < 1:
            self.otherPen.lineTo(pt3)
            self.currentPt = pt3
            return
        step = 1.0 / maxSteps
        for factor in range(1, maxSteps + 1):
            pt = getCubicPoint(factor * step, self.currentPt, pt1, pt2, pt3)
            self.otherPen.lineTo(pt)
        self.currentPt = pt3

    def _qCurveToOne(self, pt1, pt2):
        falseCurve = (pt1 == self.currentPt) or (pt1 == pt2)
        if falseCurve:
            self._lineTo(pt2)
            return
        est = calcQuadraticArcLength(self.currentPt, pt1, pt2) / self.approximateSegmentLength
        maxSteps = int(round(est))
        if maxSteps < 1:
            self.otherPen.lineTo(pt2)
            self.currentPt = pt2
            return
        step = 1.0 / maxSteps
        for factor in range(1, maxSteps + 1):
            pt = getQuadraticPoint(factor * step, self.currentPt, pt1, pt2)
            self.otherPen.lineTo(pt)
        self.currentPt = pt2

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.otherPen.closePath()
        self.currentPt = None

    def _endPath(self):
        self.otherPen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)


def flattenGlyph(aGlyph, threshold=10, segmentLines=True):
    """
    Convenience function that applies the **FlattenPen** pen to a glyph in place.
    """
    if len(aGlyph) == 0:
        return aGlyph
    from fontTools.pens.recordingPen import RecordingPen
    recorder = RecordingPen()
    filterpen = FlattenPen(recorder, approximateSegmentLength=threshold, segmentLines=segmentLines)
    aGlyph.draw(filterpen)
    aGlyph.clear()
    recorder.replay(aGlyph.getPen())
    return aGlyph



class SamplingPen(BasePen):
    """
    This filter pen processes the contours into a series of straight lines by flattening the curves.
    Unlike FlattenPen, SamplingPen draws each curve with the given number of steps.

    - otherPen: a different segment pen object this filter should draw the results with.
    - steps: the number of steps for each curve segment.
    - filterDoubles: don't draw if a segment goes to the same coordinate.
    """

    def __init__(self, otherPen, steps=10, filterDoubles=True):
        BasePen.__init__(self, {})
        self.otherPen = otherPen
        self.currentPt = None
        self.firstPt = None
        self.steps = steps
        self.filterDoubles = filterDoubles

    def _moveTo(self, pt):
        self.otherPen.moveTo(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        if self.filterDoubles:
            if pt == self.currentPt:
                return
        self.otherPen.lineTo(pt)
        self.currentPt = pt
        return

    def _curveToOne(self, pt1, pt2, pt3):
        falseCurve = (pt1 == self.currentPt) and (pt2 == pt3)
        if falseCurve:
            self._lineTo(pt3)
            return
        step = 1.0 / self.steps
        for factor in range(1, self.steps + 1):
            pt = getCubicPoint(factor * step, self.currentPt, pt1, pt2, pt3)
            self.otherPen.lineTo(pt)
        self.currentPt = pt3

    def _qCurveToOne(self, pt1, pt2):
        falseCurve = (pt1 == self.currentPt) or (pt1 == pt2)
        if falseCurve:
            self._lineTo(pt2)
            return
        step = 1.0 / self.steps
        for factor in range(1, self.steps + 1):
            pt = getQuadraticPoint(factor * step, self.currentPt, pt1, pt2)
            self.otherPen.lineTo(pt)
        self.currentPt = pt2

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.otherPen.closePath()
        self.currentPt = None

    def _endPath(self):
        self.otherPen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)


def samplingGlyph(aGlyph, steps=10):
    """
    Convenience function that applies the **SamplingPen** pen to a glyph in place.
    """
    if len(aGlyph) == 0:
        return aGlyph
    from fontTools.pens.recordingPen import RecordingPen
    recorder = RecordingPen()
    filterpen = SamplingPen(recorder, steps=steps)
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
    testGlyph.width = 500
    pen = testGlyph.getPen()
    pen.moveTo((10, 10))
    pen.lineTo((10, 30))
    pen.lineTo((30, 30))
    pen.lineTo((30, 10))
    pen.closePath()
    return testGlyph


def _testFlattenPen():
    """
    >>> from fontPens.printPen import PrintPen
    >>> glyph = _makeTestGlyph()
    >>> pen = FlattenPen(PrintPen(), approximateSegmentLength=10, segmentLines=True)
    >>> glyph.draw(pen)
    pen.moveTo((10, 10))
    pen.lineTo((10.0, 20.0))
    pen.lineTo((10.0, 30.0))
    pen.lineTo((20.0, 30.0))
    pen.lineTo((30.0, 30.0))
    pen.lineTo((30.0, 20.0))
    pen.lineTo((30.0, 10.0))
    pen.lineTo((20.0, 10.0))
    pen.lineTo((10.0, 10.0))
    pen.closePath()
    """


def _testFlattenGlyph():
    """
    >>> from fontPens.printPen import PrintPen
    >>> glyph = _makeTestGlyph()
    >>> flattenGlyph(glyph) #doctest: +ELLIPSIS
    <RGlyph...
    >>> glyph.draw(PrintPen())
    pen.moveTo((10.0, 10.0))
    pen.lineTo((10.0, 20.0))
    pen.lineTo((10.0, 30.0))
    pen.lineTo((20.0, 30.0))
    pen.lineTo((30.0, 30.0))
    pen.lineTo((30.0, 20.0))
    pen.lineTo((30.0, 10.0))
    pen.lineTo((20.0, 10.0))
    pen.closePath()
    """


def _makeTestGlyphWithCurve():
    # make a simple glyph that we can test the pens with.
    from fontParts.fontshell import RGlyph
    testGlyph = RGlyph()
    testGlyph.name = "testGlyph"
    testGlyph.width = 500
    pen = testGlyph.getPen()
    pen.moveTo((84, 37))
    pen.lineTo((348, 37))
    pen.lineTo((348, 300))
    pen.curveTo((265, 350.0), (177, 350.0), (84, 300))
    pen.closePath()
    return testGlyph


def _testFlattenPen():
    """
    >>> from fontPens.printPen import PrintPen
    >>> glyph = _makeTestGlyphWithCurve()
    >>> pen = SamplingPen(PrintPen(), steps=2)
    >>> glyph.draw(pen)
    pen.moveTo((84, 37))
    pen.lineTo((348, 37))
    pen.lineTo((348, 300))
    pen.lineTo((219.75, 337.5))
    pen.lineTo((84, 300))
    pen.lineTo((84, 37))
    pen.closePath()

    """


def _testFlattenGlyph():
    """
    >>> from fontPens.printPen import PrintPen
    >>> glyph = _makeTestGlyphWithCurve()
    >>> samplingGlyph(glyph) #doctest: +ELLIPSIS
    <RGlyph...
    >>> glyph.draw(PrintPen())
    pen.moveTo((84, 37))
    pen.lineTo((348, 37))
    pen.lineTo((348, 300))
    pen.lineTo((322.95, 313.5))
    pen.lineTo((297.6, 324.0))
    pen.lineTo((271.95, 331.5))
    pen.lineTo((246.0, 336.0))
    pen.lineTo((219.75, 337.5))
    pen.lineTo((193.19999999999996, 336.0))
    pen.lineTo((166.35, 331.5))
    pen.lineTo((139.2, 324.0))
    pen.lineTo((111.75, 313.5))
    pen.lineTo((84, 300))
    pen.closePath()
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()

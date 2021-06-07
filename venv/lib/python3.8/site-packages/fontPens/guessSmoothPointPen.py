from __future__ import absolute_import, print_function, division

import math
from fontTools.pens.pointPen import AbstractPointPen


class GuessSmoothPointPen(AbstractPointPen):
    """
    Filtering PointPen that tries to determine whether an on-curve point
    should be "smooth", ie. that it's a "tangent" point or a "curve" point.
    """

    def __init__(self, outPen, error=0.05):
        self._outPen = outPen
        self._error = error
        self._points = None

    def _flushContour(self):
        points = self._points
        nPoints = len(points)
        if not nPoints:
            return
        if points[0][1] == "move":
            # Open path.
            indices = range(1, nPoints - 1)
        elif nPoints > 1:
            # Closed path. To avoid having to mod the contour index, we
            # simply abuse Python's negative index feature, and start at -1
            indices = range(-1, nPoints - 1)
        else:
            # closed path containing 1 point (!), ignore.
            indices = []
        for i in indices:
            pt, segmentType, dummy, name, kwargs = points[i]
            if segmentType is None:
                continue
            prev = i - 1
            next = i + 1
            if points[prev][1] is not None and points[next][1] is not None:
                continue
            # At least one of our neighbors is an off-curve point
            pt = points[i][0]
            prevPt = points[prev][0]
            nextPt = points[next][0]
            if pt != prevPt and pt != nextPt:
                dx1, dy1 = pt[0] - prevPt[0], pt[1] - prevPt[1]
                dx2, dy2 = nextPt[0] - pt[0], nextPt[1] - pt[1]
                a1 = math.atan2(dx1, dy1)
                a2 = math.atan2(dx2, dy2)
                if abs(a1 - a2) < self._error:
                    points[i] = pt, segmentType, True, name, kwargs

        for pt, segmentType, smooth, name, kwargs in points:
            self._outPen.addPoint(pt, segmentType, smooth, name, **kwargs)

    def beginPath(self, identifier=None):
        assert self._points is None
        self._points = []
        self._outPen.beginPath(identifier)

    def endPath(self):
        self._flushContour()
        self._outPen.endPath()
        self._points = None

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        self._points.append((pt, segmentType, False, name, kwargs))

    def addComponent(self, glyphName, transformation, identifier=None):
        assert self._points is None
        self._outPen.addComponent(glyphName, transformation, identifier)


def _testGuessSmoothPointPen():
    """
    >>> from fontPens.printPointPen import PrintPointPen
    >>> pen = GuessSmoothPointPen(PrintPointPen())

    >>> pen.beginPath(identifier="abc123")
    pen.beginPath(identifier='abc123')
    >>> pen.addPoint((10, 100), "move")
    >>> pen.addPoint((10, 200))
    >>> pen.addPoint((10, 300))
    >>> pen.addPoint((10, 400), "curve")
    >>> pen.addPoint((10, 500))
    >>> pen.endPath()
    pen.addPoint((10, 100), segmentType='move')
    pen.addPoint((10, 200))
    pen.addPoint((10, 300))
    pen.addPoint((10, 400), segmentType='curve', smooth=True)
    pen.addPoint((10, 500))
    pen.endPath()

    >>> pen.beginPath(identifier="abc123")
    pen.beginPath(identifier='abc123')
    >>> pen.addPoint((10, 100), "move")
    >>> pen.addPoint((10, 200))
    >>> pen.addPoint((8, 300))
    >>> pen.addPoint((10, 400), "curve", smooth=False)
    >>> pen.addPoint((10, 500))
    >>> pen.endPath()
    pen.addPoint((10, 100), segmentType='move')
    pen.addPoint((10, 200))
    pen.addPoint((8, 300))
    pen.addPoint((10, 400), segmentType='curve', smooth=True)
    pen.addPoint((10, 500))
    pen.endPath()

    >>> pen.addComponent("a", (1, 0, 0, 1, 10, 10), "xyz987")
    pen.addComponent('a', (1, 0, 0, 1, 10, 10), identifier='xyz987')
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

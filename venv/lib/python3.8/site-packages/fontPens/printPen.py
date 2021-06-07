from __future__ import absolute_import, print_function, division

from fontTools.misc.py23 import *
from fontTools.pens.basePen import AbstractPen


class PrintPen(AbstractPen):
    """
    A SegmentPen that prints every step.
    """

    def moveTo(self, pt):
        print("pen.moveTo(%s)" % (tuple(pt),))

    def lineTo(self, pt):
        print("pen.lineTo(%s)" % (tuple(pt),))

    def curveTo(self, *pts):
        args = self._pointArgsRepr(pts)
        print("pen.curveTo(%s)" % args)

    def qCurveTo(self, *pts):
        args = self._pointArgsRepr(pts)
        print("pen.qCurveTo(%s)" % args)

    def closePath(self):
        print("pen.closePath()")

    def endPath(self):
        print("pen.endPath()")

    def addComponent(self, baseGlyphName, transformation):
        print("pen.addComponent('%s', %s)" % (baseGlyphName, tuple(transformation)))

    @staticmethod
    def _pointArgsRepr(pts):
        return ", ".join("None" if pt is None else str(tuple(pt)) for pt in pts)


def _testPrintPen():
    """
    >>> pen = PrintPen()
    >>> pen.moveTo((10, 10))
    pen.moveTo((10, 10))
    >>> pen.lineTo((20, 20))
    pen.lineTo((20, 20))
    >>> pen.curveTo((1, 1), (2, 2), (3, 3))
    pen.curveTo((1, 1), (2, 2), (3, 3))
    >>> pen.qCurveTo((4, 4), (5, 5))
    pen.qCurveTo((4, 4), (5, 5))
    >>> pen.qCurveTo((6, 6))
    pen.qCurveTo((6, 6))
    >>> pen.closePath()
    pen.closePath()
    >>> pen.endPath()
    pen.endPath()
    >>> pen.addComponent("a", (1, 0, 0, 1, 10, 10))
    pen.addComponent('a', (1, 0, 0, 1, 10, 10))
    >>> pen.curveTo((1, 1), (2, 2), (3, 3), None)
    pen.curveTo((1, 1), (2, 2), (3, 3), None)
    >>> pen.qCurveTo((1, 1), (2, 2), (3, 3), None)
    pen.qCurveTo((1, 1), (2, 2), (3, 3), None)
    """


def _testPrintPen_nonTuplePoints():
    """
    >>> pen = PrintPen()
    >>> pen.moveTo([10, 10])
    pen.moveTo((10, 10))
    >>> pen.lineTo([20, 20])
    pen.lineTo((20, 20))
    >>> pen.curveTo([1, 1], [2, 2], [3, 3])
    pen.curveTo((1, 1), (2, 2), (3, 3))
    >>> pen.qCurveTo([4, 4], [5, 5])
    pen.qCurveTo((4, 4), (5, 5))
    >>> pen.qCurveTo([6, 6])
    pen.qCurveTo((6, 6))
    >>> pen.closePath()
    pen.closePath()
    >>> pen.endPath()
    pen.endPath()
    >>> pen.addComponent("a", [1, 0, 0, 1, 10, 10])
    pen.addComponent('a', (1, 0, 0, 1, 10, 10))
    >>> pen.curveTo([1, 1], [2, 2], [3, 3], None)
    pen.curveTo((1, 1), (2, 2), (3, 3), None)
    >>> pen.qCurveTo([1, 1], [2, 2], [3, 3], None)
    pen.qCurveTo((1, 1), (2, 2), (3, 3), None)
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

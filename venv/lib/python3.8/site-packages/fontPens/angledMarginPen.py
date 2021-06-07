from __future__ import absolute_import, print_function, division

import math

from fontTools.misc.py23 import *
from fontTools.pens.basePen import BasePen

from fontPens.penTools import getCubicPoint


class AngledMarginPen(BasePen):
    """
    Pen to calculate the margins according to a slanted coordinate system. Slant angle comes from font.info.italicAngle.

    - this pen works on the on-curve points, and approximates the distance to curves.
    - results will be float.
    """

    def __init__(self, glyphSet, width, italicAngle):
        BasePen.__init__(self, glyphSet)
        self.width = width
        self._angle = math.radians(90 + italicAngle)
        self.maxSteps = 100
        self.margin = None
        self._left = None
        self._right = None
        self._start = None
        self.currentPoint = None

    def _getAngled(self, pt):
        right = (self.width + (pt[1] / math.tan(self._angle))) - pt[0]
        left = pt[0] - ((pt[1] / math.tan(self._angle)))
        if self._right is None:
            self._right = right
        else:
            self._right = min(self._right, right)
        if self._left is None:
            self._left = left
        else:
            self._left = min(self._left, left)
        self.margin = self._left, self._right

    def _moveTo(self, pt):
        self._start = self.currentPoint = pt

    def _addMoveTo(self):
        if self._start is None:
            return
        self._start = self.currentPoint = None

    def _lineTo(self, pt):
        self._addMoveTo()
        self._getAngled(pt)
        self.currentPoint = pt

    def _curveToOne(self, pt1, pt2, pt3):
        self._addMoveTo()
        step = 1.0 / self.maxSteps
        factors = range(0, self.maxSteps + 1)
        for i in factors:
            pt = getCubicPoint(i * step, self.currentPoint, pt1, pt2, pt3)
            self._getAngled(pt)
        self.currentPoint = pt3

    def _qCurveToOne(self, bcp, pt):
        self._addMoveTo()
        self._getAngled(pt)
        self.currentPoint = pt


def getAngledMargins(glyph, font):
    """
    Convenience function, returns the angled margins for this glyph. Adjusted for font.info.italicAngle.
    """
    pen = AngledMarginPen(font, glyph.width, font.info.italicAngle)
    glyph.draw(pen)
    return pen.margin


def setAngledLeftMargin(glyph, font, value):
    """
    Convenience function, sets the left angled margin to value. Adjusted for font.info.italicAngle.
    """
    pen = AngledMarginPen(font, glyph.width, font.info.italicAngle)
    g.draw(pen)
    isLeft, isRight = pen.margin
    glyph.leftMargin += value - isLeft


def setAngledRightMargin(glyph, font, value):
    """
    Convenience function, sets the right angled margin to value. Adjusted for font.info.italicAngle.
    """
    pen = AngledMarginPen(font, glyph.width, font.info.italicAngle)
    g.draw(pen)
    isLeft, isRight = pen.margin
    glyph.rightMargin += value - isRight


def centerAngledMargins(glyph, font):
    """
    Convenience function, centers the glyph on angled margins.
    """
    pen = AngledMarginPen(font, glyph.width, font.info.italicAngle)
    g.draw(pen)
    isLeft, isRight = pen.margin
    setAngledLeftMargin(glyph, font, (isLeft + isRight) * .5)
    setAngledRightMargin(glyph, font, (isLeft + isRight) * .5)


def guessItalicOffset(glyph, font):
    """
    Guess the italic offset based on the margins of a symetric glyph.
    For instance H or I.
    """
    l, r = getAngledMargins(glyph, font)
    return l - (l + r) * .5


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
    pen.curveTo((120, 700), (120, 300), (100, 100))
    pen.closePath()
    return testGlyph


def _testAngledMarginPen():
    """
    >>> glyph = _makeTestGlyph()
    >>> pen = AngledMarginPen(dict(), width=0, italicAngle=10)
    >>> glyph.draw(pen)
    >>> pen.margin
    (117.63269807084649, -1041.061584566772)
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

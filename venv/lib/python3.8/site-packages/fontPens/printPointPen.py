from __future__ import absolute_import, print_function, division

from fontTools.misc.py23 import *
from fontTools.pens.pointPen import AbstractPointPen


class PrintPointPen(AbstractPointPen):
    """
    A PointPen that prints every step.
    """

    def __init__(self):
        self.havePath = False

    def beginPath(self, identifier=None):
        self.havePath = True
        if identifier is not None:
            print("pen.beginPath(identifier=%r)" % identifier)
        else:
            print("pen.beginPath()")

    def endPath(self):
        self.havePath = False
        print("pen.endPath()")

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, identifier=None, **kwargs):
        assert self.havePath
        args = ["(%s, %s)" % (pt[0], pt[1])]
        if segmentType is not None:
            args.append("segmentType='%s'" % segmentType)
        if smooth:
            args.append("smooth=True")
        if name is not None:
            args.append("name='%s'" % name)
        if identifier is not None:
            args.append("identifier='%s'" % identifier)
        if kwargs:
            args.append("**%s" % kwargs)
        print("pen.addPoint(%s)" % ", ".join(args))

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        assert not self.havePath
        args = "'%s', %r" % (baseGlyphName, transformation)
        if identifier is not None:
            args += ", identifier='%s'" % identifier
        print("pen.addComponent(%s)" % args)


def _testPrintPointPen():
    """
    >>> pen = PrintPointPen()
    >>> pen.beginPath()
    pen.beginPath()
    >>> pen.beginPath("abc123")
    pen.beginPath(identifier='abc123')
    >>> pen.addPoint((10, 10), "curve", True, identifier="abc123")
    pen.addPoint((10, 10), segmentType='curve', smooth=True, identifier='abc123')
    >>> pen.addPoint((10, 10), "curve", True)
    pen.addPoint((10, 10), segmentType='curve', smooth=True)
    >>> pen.endPath()
    pen.endPath()
    >>> pen.addComponent("a", (1, 0, 0, 1, 10, 10), "xyz987")
    pen.addComponent('a', (1, 0, 0, 1, 10, 10), identifier='xyz987')
    >>> pen.addComponent("a", (1, 0, 0, 1, 10, 10), identifier="xyz9876")
    pen.addComponent('a', (1, 0, 0, 1, 10, 10), identifier='xyz9876')
    >>> pen.addComponent("a", (1, 0, 0, 1, 10, 10))
    pen.addComponent('a', (1, 0, 0, 1, 10, 10))
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

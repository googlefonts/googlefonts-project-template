from __future__ import absolute_import, print_function, division

from fontTools.pens.pointPen import AbstractPointPen


class TransformPointPen(AbstractPointPen):
    """
    PointPen that transforms all coordinates, and passes them to another
    PointPen. It also transforms the transformation given to addComponent().
    """

    def __init__(self, outPen, transformation):
        if not hasattr(transformation, "transformPoint"):
            from fontTools.misc.transform import Transform
            transformation = Transform(*transformation)
        self._transformation = transformation
        self._transformPoint = transformation.transformPoint
        self._outPen = outPen
        self._stack = []

    def beginPath(self, identifier=None):
        self._outPen.beginPath(identifier=identifier)

    def endPath(self):
        self._outPen.endPath()

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        pt = self._transformPoint(pt)
        self._outPen.addPoint(pt, segmentType, smooth, name, **kwargs)

    def addComponent(self, glyphName, transformation, identifier=None):
        transformation = self._transformation.transform(transformation)
        self._outPen.addComponent(glyphName, transformation, identifier)


def _testTransformPointPen():
    """
    >>> from fontPens.printPointPen import PrintPointPen

    >>> pen = TransformPointPen(PrintPointPen(), (1, 0, 0, 1, 20, 20))
    >>> pen.beginPath()
    pen.beginPath()
    >>> pen.addPoint((0, 0), "move", name="hello")
    pen.addPoint((20, 20), segmentType='move', name='hello')
    >>> pen.endPath()
    pen.endPath()
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

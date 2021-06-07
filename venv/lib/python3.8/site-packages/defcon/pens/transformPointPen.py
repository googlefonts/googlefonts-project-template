from fontTools.pens.pointPen import AbstractPointPen
from warnings import warn


class TransformPointPen(AbstractPointPen):

    """PointPen that transforms all coordinates, and passes them to another
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
        try:
            self._outPen.addComponent(glyphName, transformation, identifier)
        except TypeError:
            self._outPen.addComponent(glyphName, transformation)
            warn("The addComponent method needs an identifier kwarg. The component's identifier value has been discarded.", DeprecationWarning)

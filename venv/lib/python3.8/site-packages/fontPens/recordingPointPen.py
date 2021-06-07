from __future__ import absolute_import, print_function, division

from fontTools.pens.pointPen import AbstractPointPen


def replayRecording(recording, pen):
    """Replay a recording, as produced by RecordingPointPen, to a pointpen.

    Note that recording does not have to be produced by those pens.
    It can be any iterable of tuples of method name and tuple-of-arguments.
    Likewise, pen can be any objects receiving those method calls.
    """
    for operator, operands, kwargs in recording:
        getattr(pen, operator)(*operands, **kwargs)


class RecordingPointPen(AbstractPointPen):

    def __init__(self):
        self.value = []

    def beginPath(self, **kwargs):
        self.value.append(("beginPath", (), kwargs))

    def endPath(self):
        self.value.append(("endPath", (), {}))

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        self.value.append(("addPoint", (pt, segmentType, smooth, name), kwargs))

    def addComponent(self, baseGlyphName, transformation, **kwargs):
        self.value.append(("addComponent", (baseGlyphName, transformation), kwargs))

    def replay(self, pen):
        replayRecording(self.value, pen)


def _test():
    """
        >>> from fontPens.printPointPen import PrintPointPen
        >>> pen = RecordingPointPen()
        >>> pen.beginPath()
        >>> pen.addPoint((100, 200), smooth=False, segmentType="line")
        >>> pen.endPath()
        >>> pen.beginPath(identifier="my_path_id")
        >>> pen.addPoint((200, 300), segmentType="line")
        >>> pen.addPoint((200, 400), segmentType="line", identifier="my_point_id")
        >>> pen.endPath()
        >>> pen2 = RecordingPointPen()
        >>> pen.replay(pen2)
        >>> assert pen.value == pen2.value
        >>> ppp = PrintPointPen()
        >>> pen2.replay(ppp)
        pen.beginPath()
        pen.addPoint((100, 200), segmentType='line')
        pen.endPath()
        pen.beginPath(identifier='my_path_id')
        pen.addPoint((200, 300), segmentType='line')
        pen.addPoint((200, 400), segmentType='line', identifier='my_point_id')
        pen.endPath()
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

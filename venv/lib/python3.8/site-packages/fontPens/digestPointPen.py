from __future__ import absolute_import, print_function, division

from fontTools.pens.pointPen import AbstractPointPen


class DigestPointPen(AbstractPointPen):
    """
    This calculates a tuple representing the structure and values in a glyph:

        - including coordinates
        - including components
    """

    def __init__(self, ignoreSmoothAndName=False):
        self._data = []
        self.ignoreSmoothAndName = ignoreSmoothAndName

    def beginPath(self, identifier=None):
        self._data.append(('beginPath', identifier))

    def endPath(self):
        self._data.append('endPath')

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        if self.ignoreSmoothAndName:
            self._data.append((pt, segmentType))
        else:
            self._data.append((pt, segmentType, smooth, name))

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        t = []
        for v in transformation:
            if int(v) == v:
                t.append(int(v))
            else:
                t.append(v)
        self._data.append((baseGlyphName, tuple(t), identifier))

    def getDigest(self):
        """
        Return the digest as a tuple with all coordinates of all points.
        """
        return tuple(self._data)

    def getDigestPointsOnly(self, needSort=True):
        """
        Return the digest as a tuple with all coordinates of all points,
        - but without smooth info or drawing instructions.
        - For instance if you want to compare 2 glyphs in shape,
          but not interpolatability.
        """
        points = []
        for item in self._data:
            if isinstance(item, tuple) and isinstance(item[0], tuple):
                points.append(item[0])
        if needSort:
            points.sort()
        return tuple(points)


class DigestPointStructurePen(DigestPointPen):

    """
    This calculates a tuple representing the structure and values in a glyph:

        - excluding coordinates
        - excluding components
    """

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):
        self._data.append(segmentType)

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        self._data.append(baseGlyphName)


def _testDigestPointPen():
    """
    >>> pen = DigestPointPen()
    >>> pen.beginPath("abc123")
    >>> pen.getDigest()
    (('beginPath', 'abc123'),)
    >>> pen.addPoint((10, 10), "move", True)
    >>> pen.addPoint((-10, 100), "line", False)
    >>> pen.endPath()
    >>> pen.getDigest()
    (('beginPath', 'abc123'), ((10, 10), 'move', True, None), ((-10, 100), 'line', False, None), 'endPath')
    >>> pen.getDigestPointsOnly()  # https://github.com/robofab-developers/fontPens/issues/8
    ((-10, 100), (10, 10))
    >>> pen.beginPath()
    >>> pen.addPoint((100, 100), 'line')
    >>> pen.addPoint((100, 10), 'line')
    >>> pen.addPoint((10, 10), 'line')
    >>> pen.endPath()
    >>> pen.getDigest()
    (('beginPath', 'abc123'), ((10, 10), 'move', True, None), ((-10, 100), 'line', False, None), 'endPath', ('beginPath', None), ((100, 100), 'line', False, None), ((100, 10), 'line', False, None), ((10, 10), 'line', False, None), 'endPath')
    >>> pen.getDigestPointsOnly()
    ((-10, 100), (10, 10), (10, 10), (100, 10), (100, 100))
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

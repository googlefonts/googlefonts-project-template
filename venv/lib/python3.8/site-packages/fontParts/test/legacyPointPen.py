from fontPens.recordingPointPen import RecordingPointPen


class LegacyPointPen(RecordingPointPen):

    """
    A point pen that accepts only the original
    arguments in the various methods.
    """

    def beginPath(self):
        super(LegacyPointPen, self).beginPath()

    def endPath(self):
        super(LegacyPointPen, self).endPath()

    def addPoint(self, pt, segmentType=None, smooth=False, name=None):
        super(LegacyPointPen, self).addPoint(pt,
                                             segmentType=segmentType,
                                             smooth=smooth, name=name)

    def addComponent(self, baseGlyphName, transformation):
        super(LegacyPointPen, self).addComponent(baseGlyphName, transformation)

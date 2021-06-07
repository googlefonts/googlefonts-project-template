from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference
)
from fontParts.base import normalizers
from fontParts.base.compatibility import ContourCompatibilityReporter
from fontParts.base.bPoint import absoluteBCPIn, absoluteBCPOut
from fontParts.base.deprecated import DeprecatedContour, RemovedContour


class BaseContour(
        BaseObject,
        TransformationMixin,
        InterpolationMixin,
        SelectionMixin,
        IdentifierMixin,
        DeprecatedContour,
        RemovedContour
     ):

    segmentClass = None
    bPointClass = None

    def _reprContents(self):
        contents = []
        if self.identifier is not None:
            contents.append("identifier='%r'" % self.identifier)
        if self.glyph is not None:
            contents.append("in glyph")
            contents += self.glyph._reprContents()
        return contents

    def copyData(self, source):
        super(BaseContour, self).copyData(source)
        for sourcePoint in source.points:
            self.appendPoint((0, 0))
            selfPoint = self.points[-1]
            selfPoint.copyData(sourcePoint)

    # -------
    # Parents
    # -------

    # Glyph

    _glyph = None

    glyph = dynamicProperty("glyph",
                            "The contour's parent :class:`BaseGlyph`.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph):
        if self._glyph is not None:
            raise AssertionError("glyph for contour already set")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Font

    font = dynamicProperty("font", "The contour's parent font.")

    def _get_font(self):
        if self._glyph is None:
            return None
        return self.glyph.font

    # Layer

    layer = dynamicProperty("layer", "The contour's parent layer.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

    # --------------
    # Identification
    # --------------

    # index

    index = dynamicProperty(
        "base_index",
        """
        The index of the contour within the parent glyph's contours.

            >>> contour.index
            1
            >>> contour.index = 0

        The value will always be a :ref:`type-int`.
        """
    )

    def _get_base_index(self):
        glyph = self.glyph
        if glyph is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _set_base_index(self, value):
        glyph = self.glyph
        if glyph is None:
            raise FontPartsError("The contour does not belong to a glyph.")
        value = normalizers.normalizeIndex(value)
        contourCount = len(glyph.contours)
        if value < 0:
            value = -(value % contourCount)
        if value >= contourCount:
            value = contourCount
        self._set_index(value)

    def _get_index(self):
        """
        Subclasses may override this method.
        """
        glyph = self.glyph
        return glyph.contours.index(self)

    def _set_index(self, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # identifier

    def getIdentifierForPoint(self, point):
        """
        Create a unique identifier for and assign it to ``point``.
        If the point already has an identifier, the existing
        identifier will be returned.

            >>> contour.getIdentifierForPoint(point)
            'ILHGJlygfds'

        ``point`` must be a :class:`BasePoint`. The returned value
        will be a :ref:`type-identifier`.
        """
        point = normalizers.normalizePoint(point)
        return self._getIdentifierforPoint(point)

    def _getIdentifierforPoint(self, point):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ----
    # Pens
    # ----

    def draw(self, pen):
        """
        Draw the contour's outline data to the given :ref:`type-pen`.

            >>> contour.draw(pen)
        """
        self._draw(pen)

    def _draw(self, pen, **kwargs):
        """
        Subclasses may override this method.
        """
        from fontTools.ufoLib.pointPen import PointToSegmentPen
        adapter = PointToSegmentPen(pen)
        self.drawPoints(adapter)

    def drawPoints(self, pen):
        """
        Draw the contour's outline data to the given :ref:`type-point-pen`.

            >>> contour.drawPoints(pointPen)
        """
        self._drawPoints(pen)

    def _drawPoints(self, pen, **kwargs):
        """
        Subclasses may override this method.
        """
        # The try: ... except TypeError: ...
        # handles backwards compatibility with
        # point pens that have not been upgraded
        # to point pen protocol 2.
        try:
            pen.beginPath(self.identifier)
        except TypeError:
            pen.beginPath()
        for point in self.points:
            typ = point.type
            if typ == "offcurve":
                typ = None
            try:
                pen.addPoint(pt=(point.x, point.y), segmentType=typ,
                             smooth=point.smooth, name=point.name,
                             identifier=point.identifier)
            except TypeError:
                pen.addPoint(pt=(point.x, point.y), segmentType=typ,
                             smooth=point.smooth, name=point.name)
        pen.endPath()

    # ------------------
    # Data normalization
    # ------------------

    def autoStartSegment(self):
        """
        Automatically calculate and set the first segment
        in this contour.

        The behavior of this may vary accross environments.
        """
        self._autoStartSegment()

    def _autoStartSegment(self, **kwargs):
        """
        Subclasses may override this method.

        XXX port this from robofab
        """
        self.raiseNotImplementedError()

    def round(self):
        """
        Round coordinates in all points to integers.
        """
        self._round()

    def _round(self, **kwargs):
        """
        Subclasses may override this method.
        """
        for point in self.points:
            point.round()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, **kwargs):
        """
        Subclasses may override this method.
        """
        for point in self.points:
            point.transformBy(matrix)

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = ContourCompatibilityReporter

    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with **other**. ::

            >>> compatible, report = self.isCompatible(otherContour)
            >>> compatible
            False
            >>> compatible
            [Fatal] Contour: [0] + [0]
            [Fatal] Contour: [0] contains 4 segments | [0] contains 3 segments
            [Fatal] Contour: [0] is closed | [0] is open

        This will return a ``bool`` indicating if the contour is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        return super(BaseContour, self).isCompatible(other, BaseContour)

    def _isCompatible(self, other, reporter):
        """
        This is the environment implementation of
        :meth:`BaseContour.isCompatible`.

        Subclasses may override this method.
        """
        contour1 = self
        contour2 = other
        # open/closed
        if contour1.open != contour2.open:
            reporter.openDifference = True
        # direction
        if contour1.clockwise != contour2.clockwise:
            reporter.directionDifference = True
        # segment count
        if len(contour1) != len(contour2.segments):
            reporter.segmentCountDifference = True
            reporter.fatal = True
        # segment pairs
        for i in range(min(len(contour1), len(contour2))):
            segment1 = contour1[i]
            segment2 = contour2[i]
            segmentCompatibility = segment1.isCompatible(segment2)[1]
            if segmentCompatibility.fatal or segmentCompatibility.warning:
                if segmentCompatibility.fatal:
                    reporter.fatal = True
                if segmentCompatibility.warning:
                    reporter.warning = True
                reporter.segments.append(segmentCompatibility)

    # ----
    # Open
    # ----

    open = dynamicProperty("base_open",
                           "Boolean indicating if the contour is open.")

    def _get_base_open(self):
        value = self._get_open()
        value = normalizers.normalizeBoolean(value)
        return value

    def _get_open(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---------
    # Direction
    # ---------

    clockwise = dynamicProperty("base_clockwise",
                                ("Boolean indicating if the contour's "
                                 "winding direction is clockwise."))

    def _get_base_clockwise(self):
        value = self._get_clockwise()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_clockwise(self, value):
        value = normalizers.normalizeBoolean(value)
        self._set_clockwise(value)

    def _get_clockwise(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_clockwise(self, value):
        """
        Subclasses may override this method.
        """
        if self.clockwise != value:
            self.reverse()

    def reverse(self):
        """
        Reverse the direction of the contour.
        """
        self._reverseContour()

    def _reverse(self, **kwargs):
        """
        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    # ------------------------
    # Point and Contour Inside
    # ------------------------

    def pointInside(self, point):
        """
        Determine if ``point`` is in the black or white of the contour.

            >>> contour.pointInside((40, 65))
            True

        ``point`` must be a :ref:`type-coordinate`.
        """
        point = normalizers.normalizeCoordinateTuple(point)
        return self._pointInside(point)

    def _pointInside(self, point):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.pointInsidePen import PointInsidePen
        pen = PointInsidePen(glyphSet=None, testPoint=point, evenOdd=False)
        self.draw(pen)
        return pen.getResult()

    def contourInside(self, otherContour):
        """
        Determine if ``otherContour`` is in the black or white of this contour.

            >>> contour.contourInside(otherContour)
            True

        ``contour`` must be a :class:`BaseContour`.
        """
        otherContour = normalizers.normalizeContour(otherContour)
        return self._contourInside(otherContour)

    def _contourInside(self, otherContour):
        """
        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    # ---------------
    # Bounds and Area
    # ---------------

    bounds = dynamicProperty("bounds",
                             ("The bounds of the contour: "
                              "(xMin, yMin, xMax, yMax) or None."))

    def _get_base_bounds(self):
        value = self._get_bounds()
        if value is not None:
            value = normalizers.normalizeBoundingBox(value)
        return value

    def _get_bounds(self):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.boundsPen import BoundsPen
        pen = BoundsPen(self.layer)
        self.draw(pen)
        return pen.bounds

    area = dynamicProperty("area",
                           ("The area of the contour: "
                            "A positive number or None."))

    def _get_base_area(self):
        value = self._get_area()
        if value is not None:
            value = normalizers.normalizeArea(value)
        return value

    def _get_area(self):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.areaPen import AreaPen
        pen = AreaPen(self.layer)
        self.draw(pen)
        return abs(pen.value)

    # --------
    # Segments
    # --------

    # The base class implements the full segment interaction API.
    # Subclasses do not need to override anything within the contour
    # other than registering segmentClass. Subclasses may choose to
    # implement this API independently if desired.

    def _setContourInSegment(self, segment):
        if segment.contour is None:
            segment.contour = self

    segments = dynamicProperty("segments")

    def _get_segments(self):
        """
        Subclasses may override this method.
        """
        points = list(self.points)
        if not points:
            return []
        segments = [[]]
        lastWasOffCurve = False
        firstIsMove = points[0].type == "move"
        for point in points:
            segments[-1].append(point)
            if point.type != "offcurve":
                segments.append([])
            lastWasOffCurve = point.type == "offcurve"
        if len(segments[-1]) == 0:
            del segments[-1]
        if lastWasOffCurve and firstIsMove:
            # ignore trailing off curves
            del segments[-1]
        if lastWasOffCurve and not firstIsMove and len(segments) > 1:
            segment = segments.pop(-1)
            segment.extend(segments[0])
            del segments[0]
            segments.append(segment)
        if not lastWasOffCurve and not firstIsMove:
            segment = segments.pop(0)
            segments.append(segment)
        # wrap into segments
        wrapped = []
        for points in segments:
            s = self.segmentClass()
            s._setPoints(points)
            self._setContourInSegment(s)
            wrapped.append(s)
        return wrapped

    def __getitem__(self, index):
        return self.segments[index]

    def __iter__(self):
        return self._iterSegments()

    def _iterSegments(self):
        segments = self.segments
        count = len(segments)
        index = 0
        while count:
            yield segments[index]
            count -= 1
            index += 1

    def __len__(self):
        return self._len__segments()

    def _len__segments(self, **kwargs):
        """
        Subclasses may override this method.
        """
        return len(self.segments)

    def appendSegment(self, type=None, points=None, smooth=False, segment=None):
        """
        Append a segment to the contour.
        """
        if segment is not None:
            if type is not None:
                type = segment.type
            if points is None:
                points = [(point.x, point.y) for point in segment.points]
            smooth = segment.smooth
        type = normalizers.normalizeSegmentType(type)
        pts = []
        for pt in points:
            pt = normalizers.normalizeCoordinateTuple(pt)
            pts.append(pt)
        points = pts
        smooth = normalizers.normalizeBoolean(smooth)
        self._appendSegment(type=type, points=points, smooth=smooth)

    def _appendSegment(self, type=None, points=None, smooth=False, **kwargs):
        """
        Subclasses may override this method.
        """
        self._insertSegment(len(self), type=type, points=points,
                            smooth=smooth, **kwargs)

    def insertSegment(self, index, type=None, points=None, smooth=False, segment=None):
        """
        Insert a segment into the contour.
        """
        if segment is not None:
            if type is not None:
                type = segment.type
            if points is None:
                points = [(point.x, point.y) for point in segment.points]
            smooth = segment.smooth
        index = normalizers.normalizeIndex(index)
        type = normalizers.normalizeSegmentType(type)
        pts = []
        for pt in points:
            pt = normalizers.normalizeCoordinateTuple(pt)
            pts.append(pt)
        points = pts
        smooth = normalizers.normalizeBoolean(smooth)
        self._insertSegment(index=index, type=type,
                            points=points, smooth=smooth)

    def _insertSegment(self, index=None, type=None, points=None,
                       smooth=False, **kwargs):
        """
        Subclasses may override this method.
        """
        onCurve = points[-1]
        offCurve = points[:-1]
        segments = self.segments
        ptCount = sum([len(segments[s].points) for s in range(index)]) + 1
        self.insertPoint(ptCount, onCurve, type=type, smooth=smooth)
        for offCurvePoint in reversed(offCurve):
            self.insertPoint(ptCount, offCurvePoint, type="offcurve")

    def removeSegment(self, segment, preserveCurve=False):
        """
        Remove segment from the contour.
        If ``preserveCurve`` is set to ``True`` an attempt
        will be made to preserve the shape of the curve
        if the environment supports that functionality.
        """
        if not isinstance(segment, int):
            segment = self.segments.index(segment)
        segment = normalizers.normalizeIndex(segment)
        if segment >= self._len__segments():
            raise ValueError("No segment located at index %d." % segment)
        preserveCurve = normalizers.normalizeBoolean(preserveCurve)
        self._removeSegment(segment, preserveCurve)

    def _removeSegment(self, segment, preserveCurve, **kwargs):
        """
        segment will be a valid segment index.
        preserveCurve will be a boolean.

        Subclasses may override this method.
        """
        segment = self.segments[segment]
        for point in segment.points:
            self.removePoint(point, preserveCurve)

    def setStartSegment(self, segment):
        """
        Set the first segment on the contour.
        segment can be a segment object or an index.
        """
        segments = self.segments
        if not isinstance(segment, int):
            segmentIndex = segments.index(segment)
        else:
            segmentIndex = segment
        if len(self.segments) < 2:
            return
        if segmentIndex == 0:
            return
        if segmentIndex >= len(segments):
            raise ValueError(("The contour does not contain a segment "
                              "at index %d" % segmentIndex))
        self._setStartSegment(segmentIndex)

    def _setStartSegment(self, segmentIndex, **kwargs):
        """
        Subclasses may override this method.
        """
        segments = self.segments
        oldStart = segments[-1]
        oldLast = segments[0]
        # If the contour ends with a curve on top of a move,
        # delete the move.
        if oldLast.type == "curve" or oldLast.type == "qcurve":
            startOn = oldStart.onCurve
            lastOn = oldLast.onCurve
            if startOn.x == lastOn.x and startOn.y == lastOn.y:
                self.removeSegment(0)
                # Shift new the start index.
                segmentIndex = segmentIndex - 1
                segments = self.segments
        # If the first point is a move, convert it to a line.
        if segments[0].type == "move":
            segments[0].type = "line"
        # Reorder the points internally.
        segments = segments[segmentIndex - 1:] + segments[:segmentIndex - 1]
        points = []
        for segment in segments:
            for point in segment:
                points.append(((point.x, point.y), point.type,
                               point.smooth, point.name, point.identifier))
        # Clear the points.
        for point in self.points:
            self.removePoint(point)
        # Add the points.
        for point in points:
            position, type, smooth, name, identifier = point
            self.appendPoint(
                position,
                type=type,
                smooth=smooth,
                name=name,
                identifier=identifier
            )

    # -------
    # bPoints
    # -------

    bPoints = dynamicProperty("bPoints")

    def _get_bPoints(self):
        bPoints = []
        for point in self.points:
            if point.type not in ("move", "line", "curve"):
                continue
            bPoint = self.bPointClass()
            bPoint.contour = self
            bPoint._setPoint(point)
            bPoints.append(bPoint)
        return tuple(bPoints)

    def appendBPoint(self, type=None, anchor=None, bcpIn=None, bcpOut=None, bPoint=None):
        """
        Append a bPoint to the contour.
        """
        if bPoint is not None:
            if type is None:
                type = bPoint.type
            if anchor is None:
                anchor = bPoint.anchor
            if bcpIn is None:
                bcpIn = bPoint.bcpIn
            if bcpOut is None:
                bcpOut = bPoint.bcpOut
        type = normalizers.normalizeBPointType(type)
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._appendBPoint(type, anchor, bcpIn=bcpIn, bcpOut=bcpOut)

    def _appendBPoint(self, type, anchor, bcpIn=None, bcpOut=None, **kwargs):
        """
        Subclasses may override this method.
        """
        self.insertBPoint(
            len(self.bPoints),
            type,
            anchor,
            bcpIn=bcpIn,
            bcpOut=bcpOut
        )

    def insertBPoint(self, index, type=None, anchor=None, bcpIn=None, bcpOut=None, bPoint=None):
        """
        Insert a bPoint at index in the contour.
        """
        if bPoint is not None:
            if type is None:
                type = bPoint.type
            if anchor is None:
                anchor = bPoint.anchor
            if bcpIn is None:
                bcpIn = bPoint.bcpIn
            if bcpOut is None:
                bcpOut = bPoint.bcpOut
        index = normalizers.normalizeIndex(index)
        type = normalizers.normalizeBPointType(type)
        anchor = normalizers.normalizeCoordinateTuple(anchor)
        if bcpIn is None:
            bcpIn = (0, 0)
        bcpIn = normalizers.normalizeCoordinateTuple(bcpIn)
        if bcpOut is None:
            bcpOut = (0, 0)
        bcpOut = normalizers.normalizeCoordinateTuple(bcpOut)
        self._insertBPoint(index=index, type=type, anchor=anchor,
                           bcpIn=bcpIn, bcpOut=bcpOut)

    def _insertBPoint(self, index, type, anchor, bcpIn, bcpOut, **kwargs):
        """
        Subclasses may override this method.
        """
        # insert a simple line segment at the given anchor
        # look it up as a bPoint and change the bcpIn and bcpOut there
        # this avoids code duplication
        self._insertSegment(index=index, type="line",
                            points=[anchor], smooth=False)
        bPoints = self.bPoints
        index += 1
        if index >= len(bPoints):
            # its an append instead of an insert
            # so take the last bPoint
            index = -1
        bPoint = bPoints[index]
        bPoint.bcpIn = bcpIn
        bPoint.bcpOut = bcpOut
        bPoint.type = type

    def removeBPoint(self, bPoint):
        """
        Remove the bpoint from the contour.
        bpoint can be a point object or an index.
        """
        if not isinstance(bPoint, int):
            bPoint = bPoint.index
        bPoint = normalizers.normalizeIndex(bPoint)
        if bPoint >= self._len__points():
            raise ValueError("No bPoint located at index %d." % bPoint)
        self._removeBPoint(bPoint)

    def _removeBPoint(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses may override this method.
        """
        bPoint = self.bPoints[index]

        nextSegment = bPoint._nextSegment
        offCurves = nextSegment.offCurve
        if offCurves:
            offCurve = offCurves[0]
            self.removePoint(offCurve)

        segment = bPoint._segment
        offCurves = segment.offCurve
        if offCurves:
            offCurve = offCurves[-1]
            self.removePoint(offCurve)

        self.removePoint(bPoint._point)

    # ------
    # Points
    # ------

    def _setContourInPoint(self, point):
        if point.contour is None:
            point.contour = self

    points = dynamicProperty("points")

    def _get_points(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__points(i)
                     for i in range(self._len__points())])

    def _len__points(self):
        return self._lenPoints()

    def _lenPoints(self, **kwargs):
        """
        This must return an integer indicating
        the number of points in the contour.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__points(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__points():
            raise ValueError("No point located at index %d." % index)
        point = self._getPoint(index)
        self._setContourInPoint(point)
        return point

    def _getPoint(self, index, **kwargs):
        """
        This must return a wrapped point.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getPointIndex(self, point):
        for i, other in enumerate(self.points):
            if point == other:
                return i
        raise FontPartsError("The point could not be found.")

    def appendPoint(self, position=None, type="line", smooth=False, name=None, identifier=None, point=None):
        """
        Append a point to the contour.
        """
        if point is not None:
            if position is None:
                position = point.position
            type = point.type
            smooth = point.smooth
            if name is None:
                name = point.name
            if identifier is not None:
                identifier = point.identifier
        self.insertPoint(
            len(self.points),
            position=position,
            type=type,
            smooth=smooth,
            name=name,
            identifier=identifier
        )

    def insertPoint(self, index, position=None, type="line", smooth=False, name=None, identifier=None, point=None):
        """
        Insert a point into the contour.
        """
        if point is not None:
            if position is None:
                position = point.position
            type = point.type
            smooth = point.smooth
            if name is None:
                name = point.name
            if identifier is not None:
                identifier = point.identifier
        index = normalizers.normalizeIndex(index)
        position = normalizers.normalizeCoordinateTuple(position)
        type = normalizers.normalizePointType(type)
        smooth = normalizers.normalizeBoolean(smooth)
        if name is not None:
            name = normalizers.normalizePointName(name)
        if identifier is not None:
            identifier = normalizers.normalizeIdentifier(identifier)
        self._insertPoint(
            index,
            position=position,
            type=type,
            smooth=smooth,
            name=name,
            identifier=identifier
        )

    def _insertPoint(self, index, position, type="line",
                     smooth=False, name=None, identifier=None, **kwargs):
        """
        position will be a valid position (x, y).
        type will be a valid type.
        smooth will be a valid boolean.
        name will be a valid name or None.
        identifier will be a valid identifier or None.
        The identifier will not have been tested for uniqueness.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def removePoint(self, point, preserveCurve=False):
        """
        Remove the point from the contour.
        point can be a point object or an index.
        If ``preserveCurve`` is set to ``True`` an attempt
        will be made to preserve the shape of the curve
        if the environment supports that functionality.
        """
        if not isinstance(point, int):
            point = self.points.index(point)
        point = normalizers.normalizeIndex(point)
        if point >= self._len__points():
            raise ValueError("No point located at index %d." % point)
        preserveCurve = normalizers.normalizeBoolean(preserveCurve)
        self._removePoint(point, preserveCurve)

    def _removePoint(self, index, preserveCurve, **kwargs):
        """
        index will be a valid index. preserveCurve will be a boolean.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---------
    # Selection
    # ---------

    # segments

    selectedSegments = dynamicProperty(
        "base_selectedSegments",
        """
        A list of segments selected in the contour.

        Getting selected segment objects:

            >>> for segment in contour.selectedSegments:
            ...     segment.move((10, 20))

        Setting selected segment objects:

            >>> contour.selectedSegments = someSegments

        Setting also supports segment indexes:

            >>> contour.selectedSegments = [0, 2]
        """
    )

    def _get_base_selectedSegments(self):
        selected = tuple([normalizers.normalizeSegment(segment)
                         for segment in self._get_selectedSegments()])
        return selected

    def _get_selectedSegments(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.segments)

    def _set_base_selectedSegments(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeSegmentIndex(i)
            else:
                i = normalizers.normalizeSegment(i)
            normalized.append(i)
        self._set_selectedSegments(normalized)

    def _set_selectedSegments(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.segments, value)

    # points

    selectedPoints = dynamicProperty(
        "base_selectedPoints",
        """
        A list of points selected in the contour.

        Getting selected point objects:

            >>> for point in contour.selectedPoints:
            ...     point.move((10, 20))

        Setting selected point objects:

            >>> contour.selectedPoints = somePoints

        Setting also supports point indexes:

            >>> contour.selectedPoints = [0, 2]
        """
    )

    def _get_base_selectedPoints(self):
        selected = tuple([normalizers.normalizePoint(point)
                         for point in self._get_selectedPoints()])
        return selected

    def _get_selectedPoints(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.points)

    def _set_base_selectedPoints(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizePointIndex(i)
            else:
                i = normalizers.normalizePoint(i)
            normalized.append(i)
        self._set_selectedPoints(normalized)

    def _set_selectedPoints(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.points, value)

    # bPoints

    selectedBPoints = dynamicProperty(
        "base_selectedBPoints",
        """
        A list of bPoints selected in the contour.

        Getting selected bPoint objects:

            >>> for bPoint in contour.selectedBPoints:
            ...     bPoint.move((10, 20))

        Setting selected bPoint objects:

            >>> contour.selectedBPoints = someBPoints

        Setting also supports bPoint indexes:

            >>> contour.selectedBPoints = [0, 2]
        """
    )

    def _get_base_selectedBPoints(self):
        selected = tuple([normalizers.normalizeBPoint(bPoint)
                         for bPoint in self._get_selectedBPoints()])
        return selected

    def _get_selectedBPoints(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.bPoints)

    def _set_base_selectedBPoints(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeBPointIndex(i)
            else:
                i = normalizers.normalizeBPoint(i)
            normalized.append(i)
        self._set_selectedBPoints(normalized)

    def _set_selectedBPoints(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.bPoints, value)

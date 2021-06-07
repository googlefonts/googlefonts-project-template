try:
    from itertools import zip_longest as zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
import collections
import os
from copy import deepcopy
from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    dynamicProperty,
    interpolate
)
from fontParts.base import normalizers
from fontParts.base.compatibility import GlyphCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedGlyph, RemovedGlyph


class BaseGlyph(BaseObject,
                TransformationMixin,
                InterpolationMixin,
                SelectionMixin,
                DeprecatedGlyph,
                RemovedGlyph
                ):

    """
    A glyph object. This object will almost always
    be created by retrieving it from a font object.
    """

    copyAttributes = (
        "name",
        "unicodes",
        "width",
        "height",
        "note",
        "markColor",
        "lib"
    )

    def _reprContents(self):
        contents = [
            "'%s'" % self.name,
        ]
        if self.layer is not None:
            contents.append("('%s')" % self.layer.name)
        return contents

    def copy(self):
        """
        Copy this glyph's data into a new glyph object.
        This new glyph object will not belong to a font.

            >>> copiedGlyph = glyph.copy()

        This will copy:

        - name
        - unicodes
        - width
        - height
        - note
        - markColor
        - lib
        - contours
        - components
        - anchors
        - guidelines
        - image
        """
        return super(BaseGlyph, self).copy()

    def copyData(self, source):
        super(BaseGlyph, self).copyData(source)
        for contour in source.contours:
            self.appendContour(contour)
        for component in source.components:
            self.appendComponent(component=component)
        for anchor in source.anchors:
            self.appendAnchor(anchor=anchor)
        for guideline in source.guidelines:
            self.appendGuideline(guideline=guideline)
        sourceImage = source.image
        if sourceImage.data is not None:
            selfImage = self.addImage(data=sourceImage.data)
            selfImage.transformation = sourceImage.transformation
            selfImage.color = sourceImage.color

    # -------
    # Parents
    # -------

    # Layer

    _layer = None

    layer = dynamicProperty(
        "layer",
        """
        The glyph's parent layer.

            >>> layer = glyph.layer
        """
    )

    def _get_layer(self):
        if self._layer is None:
            return None
        return self._layer

    def _set_layer(self, layer):
        self._layer = layer

    # Font

    font = dynamicProperty(
        "font",
        """
        The glyph's parent font.

            >>> font = glyph.font
        """
    )

    def _get_font(self):
        if self._layer is None:
            return None
        return self.layer.font

    # --------------
    # Identification
    # --------------

    # Name

    name = dynamicProperty(
        "base_name",
        """
        The glyph's name. This will be a :ref:`type-string`.

            >>> glyph.name
            "A"
            >>> glyph.name = "A.alt"
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeGlyphName(value)
        return value

    def _set_base_name(self, value):
        if value == self.name:
            return
        value = normalizers.normalizeGlyphName(value)
        layer = self.layer
        if layer is not None and value in layer:
            raise ValueError("A glyph with the name '%s' already exists."
                             % value)
        self._set_name(value)

    def _get_name(self):
        """
        Get the name of the glyph.
        This must return a unicode string.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value):
        """
        Set the name of the glyph.
        This will be a unicode string.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # Unicodes

    unicodes = dynamicProperty(
        "base_unicodes",
        """
        The glyph's unicode values in order from most to least important.

            >>> glyph.unicodes
            (65,)
            >>> glyph.unicodes = [65, 66]
            >>> glyph.unicodes = []

        The values in the returned tuple will be :ref:`type-int`.
        When setting you may use a list of :ref:`type-int` or
        :ref:`type-hex` values.
        """
    )

    def _get_base_unicodes(self):
        value = self._get_unicodes()
        value = normalizers.normalizeGlyphUnicodes(value)
        return value

    def _set_base_unicodes(self, value):
        value = list(value)
        value = normalizers.normalizeGlyphUnicodes(value)
        self._set_unicodes(value)

    def _get_unicodes(self):
        """
        Get the unicodes assigned to the glyph.
        This must return a tuple of zero or more integers.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_unicodes(self, value):
        """
        Assign the unicodes to the glyph.
        This will be a list of zero or more integers.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    unicode = dynamicProperty(
        "base_unicode",
        """
        The glyph's primary unicode value.

            >>> glyph.unicode
            65
            >>> glyph.unicode = None

        This is equivalent to ``glyph.unicodes[0]``. Setting a
        ``glyph.unicode`` value will reset ``glyph.unicodes`` to a tuple
        containing that value or an empty tuple if ``value`` is ``None``.

            >>> glyph.unicodes
            (65, 67)
            >>> glyph.unicode = 65
            >>> glyph.unicodes
            (65,)
            >>> glyph.unicode = None
            >>> glyph.unicodes
            ()

        The returned value will be an :ref:`type-int` or ``None``.
        When setting you may send :ref:`type-int` or :ref:`type-hex`
        values or ``None``.
        """
    )

    def _get_base_unicode(self):
        value = self._get_unicode()
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
        return value

    def _set_base_unicode(self, value):
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
            self._set_unicode(value)
        else:
            self._set_unicodes(())

    def _get_unicode(self):
        """
        Get the primary unicode assigned to the glyph.
        This must return an integer or None.

        Subclasses may override this method.
        """
        values = self.unicodes
        if values:
            return values[0]
        return None

    def _set_unicode(self, value):
        """
        Assign the primary unicode to the glyph.
        This will be an integer or None.

        Subclasses may override this method.
        """
        if value is None:
            self.unicodes = []
        else:
            self.unicodes = [value]

    def autoUnicodes(self):
        """
        Use heuristics to set the Unicode values in the glyph.

            >>> glyph.autoUnicodes()

        Environments will define their own heuristics for
        automatically determining values.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -------
    # Metrics
    # -------

    # horizontal

    width = dynamicProperty(
        "base_width",
        """
        The glyph's width.

            >>> glyph.width
            500
            >>> glyph.width = 200

        The value will be a :ref:`type-int-float`.
        """
    )

    def _get_base_width(self):
        value = self._get_width()
        value = normalizers.normalizeGlyphWidth(value)
        return value

    def _set_base_width(self, value):
        value = normalizers.normalizeGlyphWidth(value)
        self._set_width(value)

    def _get_width(self):
        """
        This must return an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_width(self, value):
        """
        value will be an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    leftMargin = dynamicProperty(
        "base_leftMargin",
        """
        The glyph's left margin.

            >>> glyph.leftMargin
            35
            >>> glyph.leftMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_leftMargin(self):
        value = self._get_leftMargin()
        value = normalizers.normalizeGlyphLeftMargin(value)
        return value

    def _set_base_leftMargin(self, value):
        value = normalizers.normalizeGlyphLeftMargin(value)
        self._set_leftMargin(value)

    def _get_leftMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return xMin

    def _set_leftMargin(self, value):
        """
        value will be an int or float.

        Subclasses may override this method.
        """
        diff = value - self.leftMargin
        self.moveBy((diff, 0))
        self.width += diff

    rightMargin = dynamicProperty(
        "base_rightMargin",
        """
        The glyph's right margin.

            >>> glyph.rightMargin
            35
            >>> glyph.rightMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_rightMargin(self):
        value = self._get_rightMargin()
        value = normalizers.normalizeGlyphRightMargin(value)
        return value

    def _set_base_rightMargin(self, value):
        value = normalizers.normalizeGlyphRightMargin(value)
        self._set_rightMargin(value)

    def _get_rightMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return self.width - xMax

    def _set_rightMargin(self, value):
        """
        value will be an int or float.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            self.width = value
        else:
            xMin, yMin, xMax, yMax = bounds
            self.width = xMax + value

    # vertical

    height = dynamicProperty(
        "base_height",
        """
        The glyph's height.

            >>> glyph.height
            500
            >>> glyph.height = 200

        The value will be a :ref:`type-int-float`.
        """
    )

    def _get_base_height(self):
        value = self._get_height()
        value = normalizers.normalizeGlyphHeight(value)
        return value

    def _set_base_height(self, value):
        value = normalizers.normalizeGlyphHeight(value)
        self._set_height(value)

    def _get_height(self):
        """
        This must return an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_height(self, value):
        """
        value will be an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    bottomMargin = dynamicProperty(
        "base_bottomMargin",
        """
        The glyph's bottom margin.

            >>> glyph.bottomMargin
            35
            >>> glyph.bottomMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_bottomMargin(self):
        value = self._get_bottomMargin()
        value = normalizers.normalizeGlyphBottomMargin(value)
        return value

    def _set_base_bottomMargin(self, value):
        value = normalizers.normalizeGlyphBottomMargin(value)
        self._set_bottomMargin(value)

    def _get_bottomMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return yMin

    def _set_bottomMargin(self, value):
        """
        value will be an int or float.

        Subclasses may override this method.
        """
        diff = value - self.bottomMargin
        self.moveBy((0, diff))
        self.height += diff

    topMargin = dynamicProperty(
        "base_topMargin",
        """
        The glyph's top margin.

            >>> glyph.topMargin
            35
            >>> glyph.topMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_topMargin(self):
        value = self._get_topMargin()
        value = normalizers.normalizeGlyphTopMargin(value)
        return value

    def _set_base_topMargin(self, value):
        value = normalizers.normalizeGlyphTopMargin(value)
        self._set_topMargin(value)

    def _get_topMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return self.height - yMax

    def _set_topMargin(self, value):
        """
        value will be an int or float.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            self.height = value
        else:
            xMin, yMin, xMax, yMax = bounds
            self.height = yMax + value

    # ----
    # Pens
    # ----

    def getPen(self):
        """
        Return a :ref:`type-pen` object for adding outline data
        to the glyph.

            >>> pen = glyph.getPen()
        """
        self.raiseNotImplementedError()

    def getPointPen(self):
        """
        Return a :ref:`type-pointpen` object for adding outline data
        to the glyph.

            >>> pointPen = glyph.getPointPen()
        """
        self.raiseNotImplementedError()

    def draw(self, pen, contours=True, components=True):
        """
        Draw the glyph's outline data (contours and components) to
        the given :ref:`type-pen`.

            >>> glyph.draw(pen)

        If ``contours`` is set to ``False``, the glyph's
        contours will not be drawn.

            >>> glyph.draw(pen, contours=False)

        If ``components`` is set to ``False``, the glyph's
        components will not be drawn.

            >>> glyph.draw(pen, components=False)
        """
        if contours:
            for contour in self:
                contour.draw(pen)
        if components:
            for component in self.components:
                component.draw(pen)

    def drawPoints(self, pen, contours=True, components=True):
        """
        Draw the glyph's outline data (contours and components) to
        the given :ref:`type-pointpen`.

            >>> glyph.drawPoints(pointPen)

        If ``contours`` is set to ``False``, the glyph's
        contours will not be drawn.

            >>> glyph.drawPoints(pointPen, contours=False)

        If ``components`` is set to ``False``, the glyph's
        components will not be drawn.

            >>> glyph.drawPoints(pointPen, components=False)
        """
        if contours:
            for contour in self:
                contour.drawPoints(pen)
        if components:
            for component in self.components:
                component.drawPoints(pen)

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    def clear(self, contours=True, components=True, anchors=True,
              guidelines=True, image=True):
        """
        Clear the glyph.

            >>> glyph.clear()

        This clears:

        - contours
        - components
        - anchors
        - guidelines
        - image

        It's possible to turn off the clearing of portions of
        the glyph with the listed arguments.

            >>> glyph.clear(guidelines=False)
        """
        self._clear(contours=contours, components=components,
                    anchors=anchors, guidelines=guidelines, image=image)

    def _clear(self, contours=True, components=True, anchors=True,
               guidelines=True, image=True):
        """
        Subclasses may override this method.
        """
        if contours:
            self.clearContours()
        if components:
            self.clearComponents()
        if anchors:
            self.clearAnchors()
        if guidelines:
            self.clearGuidelines()
        if image:
            self.clearImage()

    def appendGlyph(self, other, offset=None):
        """
        Append the data from ``other`` to new objects in this glyph.
        This will append:

        - contours
        - components
        - anchors
        - guidelines

            >>> glyph.appendGlyph(otherGlyph)

        ``offset`` indicates the x and y shift values that should
        be applied to the appended data. It must be a :ref:`type-coordinate`
        value or ``None``. If ``None`` is given, the offset will be ``(0, 0)``.

            >>> glyph.appendGlyph(otherGlyph, (100, 0))
        """
        if offset is None:
            offset = (0, 0)
        offset = normalizers.normalizeTransformationOffset(offset)
        self._appendGlyph(other, offset)

    def _appendGlyph(self, other, offset=None):
        """
        Subclasses may override this method.
        """
        other = other.copy()
        if offset != (0, 0):
            other.moveBy(offset)
        for contour in other.contours:
            self.appendContour(contour)
        for component in other.components:
            self.appendComponent(component=component)
        for anchor in other.anchors:
            self.appendAnchor(anchor=anchor)
        for guideline in other.guidelines:
            self.appendGuideline(guideline=guideline)

    # Contours

    def _setGlyphInContour(self, contour):
        if contour.glyph is None:
            contour.glyph = self

    contours = dynamicProperty(
        "contours",
        """
        An :ref:`type-immutable-list` of all contours in the glyph.

            >>> contours = glyph.contours

        The list will contain :class:`BaseContour` objects.
        """
    )

    def _get_contours(self):
        """
        Subclasses may override this method.
        """
        return tuple([self[i] for i in range(len(self))])

    def __len__(self):
        """
        The number of contours in the glyph.

            >>> len(glyph)
            2
        """
        return self._lenContours()

    def _lenContours(self, **kwargs):
        """
        This must return an integer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __iter__(self):
        """
        Iterate through all contours in the glyph.

            >>> for contour in glyph:
            ...     contour.reverse()
        """
        return self._iterContours()

    def _iterContours(self, **kwargs):
        """
        This must return an iterator that returns wrapped contours.

        Subclasses may override this method.
        """
        count = len(self)
        index = 0
        while count:
            yield self[index]
            count -= 1
            index += 1

    def __getitem__(self, index):
        """
        Get the contour located at ``index`` from the glyph.

            >>> contour = glyph[0]

        The returned value will be a :class:`BaseContour` object.
        """
        index = normalizers.normalizeIndex(index)
        if index >= len(self):
            raise ValueError("No contour located at index %d." % index)
        contour = self._getContour(index)
        self._setGlyphInContour(contour)
        return contour

    def _getContour(self, index, **kwargs):
        """
        This must return a wrapped contour.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getContourIndex(self, contour):
        for i, other in enumerate(self.contours):
            if contour == other:
                return i
        raise FontPartsError("The contour could not be found.")

    def appendContour(self, contour, offset=None):
        """
        Append a contour containing the same data as ``contour``
        to this glyph.

            >>> contour = glyph.appendContour(contour)

        This will return a :class:`BaseContour` object representing
        the new contour in the glyph. ``offset`` indicates the x and
        y shift values that should be applied to the appended data.
        It must be a :ref:`type-coordinate` value or ``None``. If
        ``None`` is given, the offset will be ``(0, 0)``.

            >>> contour = glyph.appendContour(contour, (100, 0))
        """
        contour = normalizers.normalizeContour(contour)
        if offset is None:
            offset = (0, 0)
        offset = normalizers.normalizeTransformationOffset(offset)
        return self._appendContour(contour, offset)

    def _appendContour(self, contour, offset=None, **kwargs):
        """
        contour will be an object with a drawPoints method.

        offset will be a valid offset (x, y).

        This must return the new contour.

        Subclasses may override this method.
        """
        pointPen = self.getPointPen()
        if offset != (0, 0):
            copy = contour.copy()
            copy.moveBy(offset)
            copy.drawPoints(pointPen)
        else:
            contour.drawPoints(pointPen)
        return self[-1]

    def removeContour(self, contour):
        """
        Remove ``contour`` from the glyph.

            >>> glyph.removeContour(contour)

        ``contour`` may be a :ref:`BaseContour` or an :ref:`type-int`
        representing a contour index.
        """
        if isinstance(contour, int):
            index = contour
        else:
            index = self._getContourIndex(contour)
        index = normalizers.normalizeIndex(index)
        if index >= len(self):
            raise ValueError("No contour located at index %d." % index)
        self._removeContour(index)

    def _removeContour(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearContours(self):
        """
        Clear all contours in the glyph.

            >>> glyph.clearContours()
        """
        self._clearContours()

    def _clearContours(self):
        """
        Subclasses may override this method.
        """
        for _ in range(len(self)):
            self.removeContour(-1)

    def removeOverlap(self):
        """
        Perform a remove overlap operation on the contours.

            >>> glyph.removeOverlap()

        The behavior of this may vary across environments.
        """
        self._removeOverlap()

    def _removeOverlap(self):
        """
        Subclasses must implement this method.
        """
        self.raiseNotImplementedError()

    # Components

    def _setGlyphInComponent(self, component):
        if component.glyph is None:
            component.glyph = self

    components = dynamicProperty(
        "components",
        """
        An :ref:`type-immutable-list` of all components in the glyph.

            >>> components = glyph.components

        The list will contain :class:`BaseComponent` objects.
        """
    )

    def _get_components(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__components(i) for
                     i in range(self._len__components())])

    def _len__components(self):
        return self._lenComponents()

    def _lenComponents(self, **kwargs):
        """
        This must return an integer indicating
        the number of components in the glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__components(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__components():
            raise ValueError("No component located at index %d." % index)
        component = self._getComponent(index)
        self._setGlyphInComponent(component)
        return component

    def _getComponent(self, index, **kwargs):
        """
        This must return a wrapped component.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getComponentIndex(self, component):
        for i, other in enumerate(self.components):
            if component == other:
                return i
        raise FontPartsError("The component could not be found.")

    def appendComponent(self, baseGlyph=None, offset=None, scale=None, component=None):
        """
        Append a component to this glyph.

            >>> component = glyph.appendComponent("A")

        This will return a :class:`BaseComponent` object representing
        the new component in the glyph. ``offset`` indicates the x and
        y shift values that should be applied to the appended component.
        It must be a :ref:`type-coordinate` value or ``None``. If
        ``None`` is given, the offset will be ``(0, 0)``.

            >>> component = glyph.appendComponent("A", offset=(10, 20))

        ``scale`` indicates the x and y scale values that should be
        applied to the appended component. It must be a
        :ref:`type-scale` value or ``None``. If ``None`` is given,
        the scale will be ``(1.0, 1.0)``.

            >>> component = glyph.appendComponent("A", scale=(1.0, 2.0))

        ``component`` may be a :class:`BaseComponent` object from which
        attribute values will be copied. If ``baseGlyph``, ``offset``
        or ``scale`` are specified as arguments, those values will be used
        instead of the values in the given component object.
        """
        identifier = None
        sxy = 0
        syx = 0
        if component is not None:
            component = normalizers.normalizeComponent(component)
            if baseGlyph is None:
                baseGlyph = component.baseGlyph
            sx, sxy, syx, sy, ox, oy = component.transformation
            if offset is None:
                offset = (ox, oy)
            if scale is None:
                scale = (sx, sy)
            if baseGlyph is None:
                baseGlyph = component.baseGlyph
            if component.identifier is not None:
                existing = set([c.identifier for c in self.components if c.identifier is not None])
                if component.identifier not in existing:
                    identifier = component.identifier
        baseGlyph = normalizers.normalizeGlyphName(baseGlyph)
        if self.name == baseGlyph:
            raise FontPartsError(("A glyph cannot contain a component referencing itself."))
        if offset is None:
            offset = (0, 0)
        if scale is None:
            scale = (1, 1)
        offset = normalizers.normalizeTransformationOffset(offset)
        scale = normalizers.normalizeTransformationScale(scale)
        ox, oy = offset
        sx, sy = scale
        transformation = (sx, sxy, syx, sy, ox, oy)
        identifier = normalizers.normalizeIdentifier(identifier)
        return self._appendComponent(baseGlyph, transformation=transformation, identifier=identifier)

    def _appendComponent(self, baseGlyph, transformation=None, identifier=None, **kwargs):
        """
        baseGlyph will be a valid glyph name.
        The baseGlyph may or may not be in the layer.

        offset will be a valid offset (x, y).
        scale will be a valid scale (x, y).
        identifier will be a valid, nonconflicting identifier.

        This must return the new component.

        Subclasses may override this method.
        """
        pointPen = self.getPointPen()
        pointPen.addComponent(baseGlyph, transformation=transformation, identifier=identifier)
        return self.components[-1]

    def removeComponent(self, component):
        """
        Remove ``component`` from the glyph.

            >>> glyph.removeComponent(component)

        ``component`` may be a :ref:`BaseComponent` or an
        :ref:`type-int` representing a component index.
        """
        if isinstance(component, int):
            index = component
        else:
            index = self._getComponentIndex(component)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__components():
            raise ValueError("No component located at index %d." % index)
        self._removeComponent(index)

    def _removeComponent(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearComponents(self):
        """
        Clear all components in the glyph.

            >>> glyph.clearComponents()
        """
        self._clearComponents()

    def _clearComponents(self):
        """
        Subclasses may override this method.
        """
        for _ in range(self._len__components()):
            self.removeComponent(-1)

    def decompose(self):
        """
        Decompose all components in the glyph to contours.

            >>> glyph.decompose()
        """
        self._decompose()

    def _decompose(self):
        """
        Subclasses may override this method.
        """
        for component in self.components:
            component.decompose()

    # Anchors

    def _setGlyphInAnchor(self, anchor):
        if anchor.glyph is None:
            anchor.glyph = self

    anchors = dynamicProperty(
        "anchors",
        """
        An :ref:`type-immutable-list` of all anchors in the glyph.

            >>> anchors = glyph.anchors

        The list will contain :class:`BaseAnchor` objects.
        """
    )

    def _get_anchors(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__anchors(i) for
                     i in range(self._len__anchors())])

    def _len__anchors(self):
        return self._lenAnchors()

    def _lenAnchors(self, **kwargs):
        """
        This must return an integer indicating
        the number of anchors in the glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__anchors(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__anchors():
            raise ValueError("No anchor located at index %d." % index)
        anchor = self._getAnchor(index)
        self._setGlyphInAnchor(anchor)
        return anchor

    def _getAnchor(self, index, **kwargs):
        """
        This must return a wrapped anchor.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getAnchorIndex(self, anchor):
        for i, other in enumerate(self.anchors):
            if anchor == other:
                return i
        raise FontPartsError("The anchor could not be found.")

    def appendAnchor(self, name=None, position=None, color=None, anchor=None):
        """
        Append an anchor to this glyph.

            >>> anchor = glyph.appendAnchor("top", (10, 20))

        This will return a :class:`BaseAnchor` object representing
        the new anchor in the glyph. ``name`` indicated the name to
        be assigned to the anchor. It must be a :ref:`type-string`
        or ``None``. ``position`` indicates the x and y location
        to be applied to the anchor. It must be a
        :ref:`type-coordinate` value. ``color`` indicates the color
        to be applied to the anchor. It must be a :ref:`type-color`
        or ``None``.

            >>> anchor = glyph.appendAnchor("top", (10, 20), color=(1, 0, 0, 1))

        ``anchor`` may be a :class:`BaseAnchor` object from which
        attribute values will be copied. If ``name``, ``position``
        or ``color`` are specified as arguments, those values will
        be used instead of the values in the given anchor object.
        """
        identifier = None
        if anchor is not None:
            anchor = normalizers.normalizeAnchor(anchor)
            if name is None:
                name = anchor.name
            if position is None:
                position = anchor.position
            if color is None:
                color = anchor.color
            if anchor.identifier is not None:
                existing = set([a.identifier for a in self.anchors if a.identifier is not None])
                if anchor.identifier not in existing:
                    identifier = anchor.identifier
        name = normalizers.normalizeAnchorName(name)
        position = normalizers.normalizeCoordinateTuple(position)
        if color is not None:
            color = normalizers.normalizeColor(color)
        identifier = normalizers.normalizeIdentifier(identifier)
        return self._appendAnchor(name, position=position, color=color, identifier=identifier)

    def _appendAnchor(self, name, position=None, color=None, identifier=None, **kwargs):
        """
        name will be a valid anchor name.
        position will be a valid position (x, y).
        color will be None or a valid color.
        identifier will be a valid, nonconflicting identifier.

        This must return the new anchor.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeAnchor(self, anchor):
        """
        Remove ``anchor`` from the glyph.

            >>> glyph.removeAnchor(anchor)

        ``anchor`` may be an :ref:`BaseAnchor` or an
        :ref:`type-int` representing an anchor index.
        """
        if isinstance(anchor, int):
            index = anchor
        else:
            index = self._getAnchorIndex(anchor)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__anchors():
            raise ValueError("No anchor located at index %d." % index)
        self._removeAnchor(index)

    def _removeAnchor(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearAnchors(self):
        """
        Clear all anchors in the glyph.

            >>> glyph.clearAnchors()
        """
        self._clearAnchors()

    def _clearAnchors(self):
        """
        Subclasses may override this method.
        """
        for _ in range(self._len__anchors()):
            self.removeAnchor(-1)

    # ----------
    # Guidelines
    # ----------

    def _setGlyphInGuideline(self, guideline):
        if guideline.glyph is None:
            guideline.glyph = self

    guidelines = dynamicProperty(
        "guidelines",
        """
        An :ref:`type-immutable-list` of all guidelines in the glyph.

            >>> guidelines = glyph.guidelines

        The list will contain :class:`BaseGuideline` objects.
        """
    )

    def _get_guidelines(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__guidelines(i) for
                     i in range(self._len__guidelines())])

    def _len__guidelines(self):
        return self._lenGuidelines()

    def _lenGuidelines(self, **kwargs):
        """
        This must return an integer indicating
        the number of guidelines in the glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__guidelines(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__guidelines():
            raise ValueError("No guideline located at index %d." % index)
        guideline = self._getGuideline(index)
        self._setGlyphInGuideline(guideline)
        return guideline

    def _getGuideline(self, index, **kwargs):
        """
        This must return a wrapped guideline.

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getGuidelineIndex(self, guideline):
        for i, other in enumerate(self.guidelines):
            if guideline == other:
                return i
        raise FontPartsError("The guideline could not be found.")

    def appendGuideline(self, position=None, angle=None, name=None, color=None, guideline=None):
        """
        Append a guideline to this glyph.

            >>> guideline = glyph.appendGuideline((100, 0), 90)

        This will return a :class:`BaseGuideline` object representing
        the new guideline in the glyph. ``position`` indicates the
        x and y location to be used as the center point of the anchor.
        It must be a :ref:`type-coordinate` value. ``angle`` indicates
        the angle of the guideline, in degrees. This must be a
        :ref:`type-int-float` between 0 and 360. ``name`` indicates
        an name to be assigned to the guideline. It must be a
        :ref:`type-string` or ``None``.

            >>> guideline = glyph.appendGuideline((100, 0), 90, name="left")

        ``color`` indicates the color to be applied to the guideline.
        It must be a :ref:`type-color` or ``None``.

            >>> guideline = glyph.appendGuideline((100, 0), 90, color=(1, 0, 0, 1))

        ``guideline`` may be a :class:`BaseGuideline` object from which
        attribute values will be copied. If ``position``, ``angle``, ``name``
        or ``color`` are specified as arguments, those values will be used
        instead of the values in the given guideline object.
        """
        identifier = None
        if guideline is not None:
            guideline = normalizers.normalizeGuideline(guideline)
            if position is None:
                position = guideline.position
            if angle is None:
                angle = guideline.angle
            if name is None:
                name = guideline.name
            if color is None:
                color = guideline.color
            if guideline.identifier is not None:
                existing = set([g.identifier for g in self.guidelines if g.identifier is not None])
                if guideline.identifier not in existing:
                    identifier = guideline.identifier
        position = normalizers.normalizeCoordinateTuple(position)
        angle = normalizers.normalizeRotationAngle(angle)
        if name is not None:
            name = normalizers.normalizeGuidelineName(name)
        if color is not None:
            color = normalizers.normalizeColor(color)
        identifier = normalizers.normalizeIdentifier(identifier)
        guideline = self._appendGuideline(position, angle, name=name, color=color, identifier=identifier)
        guideline.glyph = self
        return guideline

    def _appendGuideline(self, position, angle, name=None, color=None, identifier=None, **kwargs):
        """
        position will be a valid position (x, y).
        angle will be a valid angle.
        name will be a valid guideline name or None.
        color will be a valid color or None .
        identifier will be a valid, nonconflicting identifier.

        This must return the new guideline.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline):
        """
        Remove ``guideline`` from the glyph.

            >>> glyph.removeGuideline(guideline)

        ``guideline`` may be a :ref:`BaseGuideline` or an
        :ref:`type-int` representing an guideline index.
        """
        if isinstance(guideline, int):
            index = guideline
        else:
            index = self._getGuidelineIndex(guideline)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__guidelines():
            raise ValueError("No guideline located at index %d." % index)
        self._removeGuideline(index)

    def _removeGuideline(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearGuidelines(self):
        """
        Clear all guidelines in the glyph.

            >>> glyph.clearGuidelines()
        """
        self._clearGuidelines()

    def _clearGuidelines(self):
        """
        Subclasses may override this method.
        """
        for _ in range(self._len__guidelines()):
            self.removeGuideline(-1)

    # ------------------
    # Data Normalization
    # ------------------

    def round(self):
        """
        Round coordinates to the nearest integer.

            >>> glyph.round()

        This applies to the following:

        - width
        - height
        - contours
        - components
        - anchors
        - guidelines
        """
        self._round()

    def _round(self):
        """
        Subclasses may override this method.
        """
        for contour in self.contours:
            contour.round()
        for component in self.components:
            component.round()
        for anchor in self.anchors:
            anchor.round()
        for guideline in self.guidelines:
            guideline.round()
        self.width = normalizers.normalizeVisualRounding(self.width)
        self.height = normalizers.normalizeVisualRounding(self.height)

    def correctDirection(self, trueType=False):
        """
        Correct the winding direction of the contours following
        the PostScript recommendations.

            >>> glyph.correctDirection()

        If ``trueType`` is ``True`` the TrueType recommendations
        will be followed.
        """
        self._correctDirection(trueType=trueType)

    def _correctDirection(self, trueType=False, **kwargs):
        """
        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def autoContourOrder(self):
        """
        Automatically order the contours based on heuristics.

            >>> glyph.autoContourOrder()

        The results of this may vary across environments.
        """
        self._autoContourOrder()

    def _autoContourOrder(self, **kwargs):
        """
        XXX

        This can be ported from RoboFab.

        XXX
        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, **kwargs):
        """
        Subclasses may override this method.
        """
        for contour in self.contours:
            contour.transformBy(matrix)
        for component in self.components:
            component.transformBy(matrix)
        for anchor in self.anchors:
            anchor.transformBy(matrix)
        for guideline in self.guidelines:
            guideline.transformBy(matrix)

    def scaleBy(self, value, origin=None, width=False, height=False):
        """
        %s
        **width** indicates if the glyph's width should be scaled.
        **height** indicates if the glyph's height should be scaled.

        The origin must not be specified when scaling the width or height.
        """
        value = normalizers.normalizeTransformationScale(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        if origin != (0, 0) and (width or height):
            raise FontPartsError(("The origin must not be set when "
                                  "scaling the width or height."))
        super(BaseGlyph, self).scaleBy(value, origin=origin)
        sX, sY = value
        if width:
            self._scaleWidthBy(sX)
        if height:
            self._scaleHeightBy(sY)

    scaleBy.__doc__ %= TransformationMixin.scaleBy.__doc__

    def _scaleWidthBy(self, value):
        """
        Subclasses may override this method.
        """
        self.width *= value

    def _scaleHeightBy(self, value):
        """
        Subclasses may override this method.
        """
        self.height *= value

    # --------------------
    # Interpolation & Math
    # --------------------

    def toMathGlyph(self):
        """
        Returns the glyph as an object that follows the
        `MathGlyph protocol <https://github.com/typesupply/fontMath>`_.

            >>> mg = glyph.toMathGlyph()
        """
        return self._toMathGlyph()

    def _toMathGlyph(self):
        """
        Subclasses may override this method.
        """
        import fontMath
        mathGlyph = fontMath.MathGlyph(None)
        pen = mathGlyph.getPointPen()
        self.drawPoints(pen)
        for anchor in self.anchors:
            d = dict(
                x=anchor.x,
                y=anchor.y,
                name=anchor.name,
                identifier=anchor.identifier,
                color=anchor.color
            )
            mathGlyph.anchors.append(d)
        for guideline in self.guidelines:
            d = dict(
                x=guideline.x,
                y=guideline.y,
                angle=guideline.angle,
                name=guideline.name,
                identifier=guideline.identifier,
                color=guideline.color
            )
            mathGlyph.guidelines.append(d)
        mathGlyph.lib = deepcopy(self.lib)
        mathGlyph.name = self.name
        mathGlyph.unicodes = self.unicodes
        mathGlyph.width = self.width
        mathGlyph.height = self.height
        mathGlyph.note = self.note
        return mathGlyph

    def fromMathGlyph(self, mathGlyph):
        """
        Replaces the contents of this glyph with the contents of ``mathGlyph``.

            >>> glyph.fromMathGlyph(mg)

        ``mathGlyph`` must be an object following the
        `MathGlyph protocol <https://github.com/typesupply/fontMath>`_.
        """
        return self._fromMathGlyph(mathGlyph, toThisGlyph=True)

    def _fromMathGlyph(self, mathGlyph, toThisGlyph=False):
        # make the destination
        if toThisGlyph:
            copied = self
            copied.clear()
        else:
            copyClass = self.copyClass
            if copyClass is None:
                copyClass = self.__class__
            copied = copyClass()
        # populate
        pen = copied.getPointPen()
        mathGlyph.drawPoints(pen, filterRedundantPoints=True)
        for anchor in mathGlyph.anchors:
            a = copied.appendAnchor(
                name=anchor["name"],
                position=(anchor["x"], anchor["y"]),
                color=anchor["color"]
            )
            identifier = anchor.get("identifier")
            if identifier is not None:
                a._setIdentifier(identifier)
        for guideline in mathGlyph.guidelines:
            g = copied.appendGuideline(
                position=(guideline["x"], guideline["y"]),
                angle=guideline["angle"],
                name=guideline["name"],
                color=guideline["color"]
            )
            identifier = guideline.get("identifier")
            if identifier is not None:
                g._setIdentifier(identifier)
        copied.lib.update(mathGlyph.lib)
        if not toThisGlyph:
            copied.name = mathGlyph.name
            copied.unicodes = mathGlyph.unicodes
        copied.width = mathGlyph.width
        copied.height = mathGlyph.height
        copied.note = mathGlyph.note
        return copied

    def __mul__(self, factor):
        """
        Subclasses may override this method.
        """
        mathGlyph = self._toMathGlyph()
        result = mathGlyph * factor
        copied = self._fromMathGlyph(result)
        return copied

    __rmul__ = __mul__

    def __truediv__(self, factor):
        """
        Subclasses may override this method.
        """
        mathGlyph = self._toMathGlyph()
        result = mathGlyph / factor
        copied = self._fromMathGlyph(result)
        return copied

    # py2 support
    __div__ = __truediv__

    def __add__(self, other):
        """
        Subclasses may override this method.
        """
        selfMathGlyph = self._toMathGlyph()
        otherMathGlyph = other._toMathGlyph()
        result = selfMathGlyph + otherMathGlyph
        copied = self._fromMathGlyph(result)
        return copied

    def __sub__(self, other):
        """
        Subclasses may override this method.
        """
        selfMathGlyph = self._toMathGlyph()
        otherMathGlyph = other._toMathGlyph()
        result = selfMathGlyph - otherMathGlyph
        copied = self._fromMathGlyph(result)
        return copied

    def interpolate(self, factor, minGlyph, maxGlyph,
                    round=True, suppressError=True):
        """
        Interpolate the contents of this glyph at location ``factor``
        in a linear interpolation between ``minGlyph`` and ``maxGlyph``.

            >>> glyph.interpolate(0.5, otherGlyph1, otherGlyph2)

        ``factor`` may be a :ref:`type-int-float` or a tuple containing
        two :ref:`type-int-float` values representing x and y factors.

            >>> glyph.interpolate((0.5, 1.0), otherGlyph1, otherGlyph2)

        ``minGlyph`` must be a :class:`BaseGlyph` and will be located at 0.0
        in the interpolation range. ``maxGlyph`` must be a :class:`BaseGlyph`
        and will be located at 1.0 in the interpolation range. If ``round``
        is ``True``, the contents of the glyph will be rounded to integers
        after the interpolation is performed.

            >>> glyph.interpolate(0.5, otherGlyph1, otherGlyph2, round=True)

        This method assumes that ``minGlyph`` and ``maxGlyph`` are completely
        compatible with each other for interpolation. If not, any errors
        encountered will raise a :class:`FontPartsError`. If ``suppressError``
        is ``True``, no exception will be raised and errors will be silently
        ignored.
        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minGlyph, BaseGlyph):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__,
                               minGlyph.__class__.__name__))
        if not isinstance(maxGlyph, BaseGlyph):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__,
                               maxGlyph.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(factor, minGlyph, maxGlyph,
                          round=round, suppressError=suppressError)

    def _interpolate(self, factor, minGlyph, maxGlyph,
                     round=True, suppressError=True):
        """
        Subclasses may override this method.
        """
        from fontMath.mathFunctions import setRoundIntegerFunction

        setRoundIntegerFunction(normalizers.normalizeVisualRounding)
        
        minGlyph = minGlyph._toMathGlyph()
        maxGlyph = maxGlyph._toMathGlyph()
        try:
            result = interpolate(minGlyph, maxGlyph, factor)
        except IndexError:
            result = None
        if result is None and not suppressError:
            raise FontPartsError(("Glyphs '%s' and '%s' could not be "
                                  "interpolated.")
                                 % (minGlyph.name, maxGlyph.name))
        if result is not None:
            if round:
                result = result.round()
            self._fromMathGlyph(result, toThisGlyph=True)

    compatibilityReporterClass = GlyphCompatibilityReporter

    @staticmethod
    def _checkPairs(object1, object2, reporter, reporterObject):
        compatibility = object1.isCompatible(object2)[1]
        if compatibility.fatal or compatibility.warning:
            if compatibility.fatal:
                reporter.fatal = True
            if compatibility.warning:
                reporter.warning = True
            reporterObject.append(compatibility)

    def isCompatible(self, other):
        """
        Evaluate the interpolation compatibility of this glyph
        and ``other``.

            >>> compatible, report = self.isCompatible(otherGlyph)
            >>> compatible
            False

        This will return a :ref:`type-bool` indicating if this glyph is
        compatible with ``other`` and a :class:`GlyphCompatibilityReporter`
        containing a detailed report about compatibility errors.
        """
        return super(BaseGlyph, self).isCompatible(other, BaseGlyph)

    def _isCompatible(self, other, reporter):
        """
        This is the environment implementation of
        :meth:`BaseGlyph.isCompatible`.

        Subclasses may override this method.
        """
        glyph1 = self
        glyph2 = other
        # contour count
        if len(self.contours) != len(glyph2.contours):
            reporter.fatal = True
            reporter.contourCountDifference = True
        # contour pairs
        for i in range(min(len(glyph1), len(glyph2))):
            contour1 = glyph1[i]
            contour2 = glyph2[i]
            self._checkPairs(contour1, contour2, reporter, reporter.contours)
        # component count
        if len(glyph1.components) != len(glyph2.components):
            reporter.fatal = True
            reporter.componentCountDifference = True
        # component check
        component_diff = []
        selfComponents = [component.baseGlyph for component in glyph1.components]
        otherComponents = [component.baseGlyph for component in glyph2.components]
        for index, (left, right) in enumerate(
            zip_longest(selfComponents, otherComponents)
        ):
            if left != right:
                component_diff.append((index, left, right))

        if component_diff:
            reporter.warning = True
            reporter.componentDifferences = component_diff
            if not reporter.componentCountDifference and set(selfComponents) == set(
                otherComponents
            ):
                reporter.componentOrderDifference = True

            selfComponents_counted_set = collections.Counter(selfComponents)
            otherComponents_counted_set = collections.Counter(otherComponents)
            missing_from_glyph1 = (
                otherComponents_counted_set - selfComponents_counted_set
            )
            if missing_from_glyph1:
                reporter.fatal = True
                reporter.componentsMissingFromGlyph1 = sorted(
                    missing_from_glyph1.elements()
                )
            missing_from_glyph2 = (
                selfComponents_counted_set - otherComponents_counted_set
            )
            if missing_from_glyph2:
                reporter.fatal = True
                reporter.componentsMissingFromGlyph2 = sorted(
                    missing_from_glyph2.elements()
                )
        # guideline count
        if len(self.guidelines) != len(glyph2.guidelines):
            reporter.warning = True
            reporter.guidelineCountDifference = True
        # guideline check
        selfGuidelines = []
        otherGuidelines = []
        for source, names in ((self, selfGuidelines),
                              (other, otherGuidelines)):
            for i, guideline in enumerate(source.guidelines):
                names.append((guideline.name, i))
        guidelines1 = set(selfGuidelines)
        guidelines2 = set(otherGuidelines)
        if len(guidelines1.difference(guidelines2)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingFromGlyph2 = list(
                guidelines1.difference(guidelines2))
        if len(guidelines2.difference(guidelines1)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingFromGlyph1 = list(
                guidelines2.difference(guidelines1))
        # anchor count
        if len(self.anchors) != len(glyph2.anchors):
            reporter.warning = True
            reporter.anchorCountDifference = True
        # anchor check
        anchor_diff = []
        selfAnchors = [anchor.name for anchor in glyph1.anchors]
        otherAnchors = [anchor.name for anchor in glyph2.anchors]
        for index, (left, right) in enumerate(zip_longest(selfAnchors, otherAnchors)):
            if left != right:
                anchor_diff.append((index, left, right))

        if anchor_diff:
            reporter.warning = True
            reporter.anchorDifferences = anchor_diff
            if not reporter.anchorCountDifference and set(selfAnchors) == set(
                otherAnchors
            ):
                reporter.anchorOrderDifference = True

            selfAnchors_counted_set = collections.Counter(selfAnchors)
            otherAnchors_counted_set = collections.Counter(otherAnchors)
            missing_from_glyph1 = otherAnchors_counted_set - selfAnchors_counted_set
            if missing_from_glyph1:
                reporter.anchorsMissingFromGlyph1 = sorted(
                    missing_from_glyph1.elements()
                )
            missing_from_glyph2 = selfAnchors_counted_set - otherAnchors_counted_set
            if missing_from_glyph2:
                reporter.anchorsMissingFromGlyph2 = sorted(
                    missing_from_glyph2.elements()
                )

    # ------------
    # Data Queries
    # ------------

    def pointInside(self, point):
        """
        Determine if ``point`` is in the black or white of the glyph.

            >>> glyph.pointInside((40, 65))
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

    bounds = dynamicProperty(
        "bounds",
        """
        The bounds of the glyph in the form
        ``(x minimum, y minimum, x maximum, y maximum)`` or,
        in the case of empty glyphs ``None``.

            >>> glyph.bounds
            (10, 30, 765, 643)
        """
    )

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

    area = dynamicProperty(
        "area",
        """
        The area of the glyph as a :ref:`type-int-float` or,
        in the case of empty glyphs ``None``.

            >>> glyph.area
            583
        """
    )

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

    # -----------------
    # Layer Interaction
    # -----------------

    layers = dynamicProperty(
        "layers",
        """
        Immutable tuple of the glyph's layers.

            >>> glyphLayers = glyph.layers

        This will return a tuple of all :ref:`type-glyph-layer` in the glyph.
        """
    )

    def _get_layers(self, **kwargs):
        font = self.font
        if font is None:
            return tuple()
        glyphs = []
        for layer in font.layers:
            if self.name in layer:
                glyphs.append(layer[self.name])
        return tuple(glyphs)

    # get

    def getLayer(self, name):
        """
        Get the :ref:`type-glyph-layer` with ``name`` in this glyph.

            >>> glyphLayer = glyph.getLayer("foreground")
        """
        name = normalizers.normalizeLayerName(name)
        return self._getLayer(name)

    def _getLayer(self, name, **kwargs):
        """
        name will be a string, but there may not be a
        layer with a name matching the string. If not,
        a ``ValueError`` must be raised.

        Subclasses may override this method.
        """
        for glyph in self.layers:
            if glyph.layer.name == name:
                return glyph
        raise ValueError("No layer named '%s' in glyph '%s'."
                         % (name, self.name))

    # new

    def newLayer(self, name):
        """
        Make a new layer with ``name`` in this glyph.

            >>> glyphLayer = glyph.newLayer("background")

        This will return the new :ref:`type-glyph-layer`.
        If the layer already exists in this glyph, it
        will be cleared.
        """
        layerName = name
        glyphName = self.name
        layerName = normalizers.normalizeLayerName(layerName)
        for glyph in self.layers:
            if glyph.layer.name == layerName:
                layer = glyph.layer
                layer.removeGlyph(glyphName)
                break
        glyph = self._newLayer(name=layerName)
        layer = self.font.getLayer(layerName)
        # layer._setLayerInGlyph(glyph)
        return glyph

    def _newLayer(self, name, **kwargs):
        """
        name will be a string representing a valid layer
        name. The name will have been tested to make sure
        that no layer in the glyph already has the name.

        This must returned the new glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, layer):
        """
        Remove ``layer`` from this glyph.

            >>> glyph.removeLayer("background")

        Layer can be a :ref:`type-glyph-layer` or a :ref:`type-string`
        representing a layer name.
        """
        if isinstance(layer, BaseGlyph):
            layer = layer.layer.name
        layerName = layer
        layerName = normalizers.normalizeLayerName(layerName)
        if self._getLayer(layerName).layer.name == layerName:
            self._removeLayer(layerName)

    def _removeLayer(self, name, **kwargs):
        """
        name will be a valid layer name. It will
        represent an existing layer in the font.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    # -----
    # Image
    # -----

    image = dynamicProperty(
        "base_image",
        "The :class:`BaseImage` for the glyph."
    )

    def _get_base_image(self):
        image = self._get_image()
        if image.glyph is None:
            image.glyph = self
        return image

    def _get_image(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def addImage(self, path=None, data=None, scale=None,
                 position=None, color=None):
        """
        Set the image in the glyph. This will return the
        assigned :class:`BaseImage`. The image data can be
        defined via ``path`` to an image file:

            >>> image = glyph.addImage(path="/path/to/my/image.png")

        The image data can be defined with raw image data
        via ``data``.

            >>> image = glyph.addImage(data=someImageData)

        If ``path`` and ``data`` are both provided, a
        :class:`FontPartsError` will be raised. The supported
        image formats will vary across environments. Refer
        to :class:`BaseImage` for complete details.

        ``scale`` indicates the x and y scale values that should be
        applied to the image. It must be a :ref:`type-scale` value
        or ``None``.

            >>> image = glyph.addImage(path="/p/t/image.png", scale=(0.5, 1.0))

        ``position`` indicates the x and y location of the lower left
        point of the image.

            >>> image = glyph.addImage(path="/p/t/image.png", position=(10, 20))

        ``color`` indicates the color to be applied to the image. It must
        be a :ref:`type-color` or ``None``.

            >>> image = glyph.addImage(path="/p/t/image.png", color=(1, 0, 0, 0.5))
        """
        if path is not None and data is not None:
            raise FontPartsError("Only path or data may be defined, not both.")
        if scale is None:
            scale = (1, 1)
        if position is None:
            position = (0, 0)
        scale = normalizers.normalizeTransformationScale(scale)
        position = normalizers.normalizeTransformationOffset(position)
        if color is not None:
            color = normalizers.normalizeColor(color)
        sx, sy = scale
        ox, oy = position
        transformation = (sx, 0, 0, sy, ox, oy)
        if path is not None:
            if not os.path.exists(path):
                raise IOError("No image located at '%s'." % path)
            f = open(path, "rb")
            data = f.read()
            f.close()
        self._addImage(data=data, transformation=transformation, color=color)
        return self.image

    def _addImage(self, data, transformation=None, color=None):
        """
        data will be raw, unnormalized image data.
        Each environment may have different possible
        formats, so this is unspecified.

        transformation will be a valid transformation matrix.

        color will be a color tuple or None.

        This must return an Image object. Assigning it
        to the glyph will be handled by the base class.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearImage(self):
        """
        Remove the image from the glyph.

            >>> glyph.clearImage()
        """
        if self.image is not None:
            self._clearImage()

    def _clearImage(self, **kwargs):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ----------
    # Mark color
    # ----------

    markColor = dynamicProperty(
        "base_markColor",
        """
        The glyph's mark color.

            >>> glyph.markColor
            (1, 0, 0, 0.5)
            >>> glyph.markColor = None

        The value may be a :ref:`type-color` or ``None``.
        """
    )

    def _get_base_markColor(self):
        value = self._get_markColor()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_markColor(self, value):
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_markColor(value)

    def _get_markColor(self):
        """
        Return the mark color value as a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_markColor(self, value):
        """
        value will be a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ----
    # Note
    # ----

    note = dynamicProperty(
        "base_note",
        """
        The glyph's note.

            >>> glyph.note
            "P.B. said this looks 'awesome.'"
            >>> glyph.note = "P.B. said this looks 'AWESOME.'"

        The value may be a :ref:`type-string` or ``None``.
        """
    )

    def _get_base_note(self):
        value = self._get_note()
        if value is not None:
            value = normalizers.normalizeGlyphNote(value)
        return value

    def _set_base_note(self, value):
        if value is not None:
            value = normalizers.normalizeGlyphNote(value)
        self._set_note(value)

    def _get_note(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_note(self, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---
    # Lib
    # ---

    lib = dynamicProperty(
        "base_lib",
        """
        The :class:`BaseLib` for the glyph.

            >>> lib = glyph.lib
        """
    )

    def _get_base_lib(self):
        lib = self._get_lib()
        lib.glyph = self
        return lib

    def _get_lib(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---
    # API
    # ---

    def isEmpty(self):
        """
        This will return :ref:`type-bool` indicating if there are contours and/or
        components in the glyph.

            >>> glyph.isEmpty()

        Note: This method only checks for the presence of contours and components.
        Other attributes (guidelines, anchors, a lib, etc.) will not affect what
        this method returns.
        """
        if self.contours:
            return False
        if self.components:
            return False
        return True

    def loadFromGLIF(self, glifData):
        """
        Reads ``glifData``, in
        `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_,
        into this glyph.

            >>> glyph.readGlyphFromString(xmlData)
        """
        self._loadFromGLIF(glifData)

    def _loadFromGLIF(self, glifData):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def dumpToGLIF(self, glyphFormatVersion=2):
        """
        This will return the glyph's contents as a string in
        `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_.

            >>> xml = glyph.writeGlyphToString()

        ``glyphFormatVersion`` must be a :ref:`type-int` that defines
        the preferred GLIF format version.
        """
        glyphFormatVersion = normalizers.normalizeGlyphFormatVersion(
            glyphFormatVersion)
        return self._dumpToGLIF(glyphFormatVersion)

    def _dumpToGLIF(self, glyphFormatVersion):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---------
    # Selection
    # ---------

    # contours

    selectedContours = dynamicProperty(
        "base_selectedContours",
        """
        An :ref:`type-immutable-list` of contours selected in the glyph.

            >>> contours = glyph.selectedContours:
            >>> glyph.selectedContours = otherContours

        It is possible to use a list of :ref:`type-int` representing
        contour indexes when setting the selected contours.

            >>> glyph.selectedContours = [0, 2]
        """
    )

    def _get_base_selectedContours(self):
        selected = tuple([normalizers.normalizeContour(contour) for
                         contour in self._get_selectedContours()])
        return selected

    def _get_selectedContours(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.contours)

    def _set_base_selectedContours(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeContour(i)
            normalized.append(i)
        self._set_selectedContours(normalized)

    def _set_selectedContours(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.contours, value)

    # components

    selectedComponents = dynamicProperty(
        "base_selectedComponents",
        """
        An :ref:`type-immutable-list` of components selected in the glyph.

            >>> components = glyph.selectedComponents:
            >>> glyph.selectedComponents = otherComponents

        It is possible to use a list of :ref:`type-int` representing
        component indexes when setting the selected components.

            >>> glyph.selectedComponents = [0, 2]
        """
    )

    def _get_base_selectedComponents(self):
        selected = tuple([normalizers.normalizeComponent(component) for
                         component in self._get_selectedComponents()])
        return selected

    def _get_selectedComponents(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.components)

    def _set_base_selectedComponents(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeComponent(i)
            normalized.append(i)
        self._set_selectedComponents(normalized)

    def _set_selectedComponents(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.components, value)

    # anchors

    selectedAnchors = dynamicProperty(
        "base_selectedAnchors",
        """
        An :ref:`type-immutable-list` of anchors selected in the glyph.

            >>> anchors = glyph.selectedAnchors:
            >>> glyph.selectedAnchors = otherAnchors

        It is possible to use a list of :ref:`type-int` representing
        anchor indexes when setting the selected anchors.

            >>> glyph.selectedAnchors = [0, 2]
        """
    )

    def _get_base_selectedAnchors(self):
        selected = tuple([normalizers.normalizeAnchor(anchor) for
                         anchor in self._get_selectedAnchors()])
        return selected

    def _get_selectedAnchors(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.anchors)

    def _set_base_selectedAnchors(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeAnchor(i)
            normalized.append(i)
        self._set_selectedAnchors(normalized)

    def _set_selectedAnchors(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.anchors, value)

    # guidelines

    selectedGuidelines = dynamicProperty(
        "base_selectedGuidelines",
        """
        An :ref:`type-immutable-list` of guidelines selected in the glyph.

            >>> guidelines = glyph.selectedGuidelines:
            >>> glyph.selectedGuidelines = otherGuidelines

        It is possible to use a list of :ref:`type-int` representing
        guidelines indexes when setting the selected guidelines.

            >>> glyph.selectedGuidelines = [0, 2]
        """
    )

    def _get_base_selectedGuidelines(self):
        selected = tuple([normalizers.normalizeGuideline(guideline) for
                         guideline in self._get_selectedGuidelines()])
        return selected

    def _get_selectedGuidelines(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.guidelines)

    def _set_base_selectedGuidelines(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeGuideline(i)
            normalized.append(i)
        self._set_selectedGuidelines(normalized)

    def _set_selectedGuidelines(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.guidelines, value)

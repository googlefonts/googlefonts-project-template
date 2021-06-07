import math
from fontTools.misc import transform
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    PointPositionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference
)
from fontParts.base import normalizers
from fontParts.base.compatibility import GuidelineCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedGuideline, RemovedGuideline


class BaseGuideline(
                    BaseObject,
                    TransformationMixin,
                    DeprecatedGuideline,
                    RemovedGuideline,
                    PointPositionMixin,
                    InterpolationMixin,
                    IdentifierMixin,
                    SelectionMixin
                    ):

    """
    A guideline object. This object is almost always
    created with :meth:`BaseGlyph.appendGuideline`.
    An orphan guideline can be created like this::

        >>> guideline = RGuideline()
    """

    copyAttributes = (
        "x",
        "y",
        "angle",
        "name",
        "color"
    )

    def _reprContents(self):
        contents = []
        if self.name is not None:
            contents.append("'%s'" % self.name)
        if self.layer is not None:
            contents.append("('%s')" % self.layer.name)
        return contents

    # -------
    # Parents
    # -------

    # Glyph

    _glyph = None

    glyph = dynamicProperty("glyph", "The guideline's parent :class:`BaseGlyph`.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph):
        if self._font is not None:
            raise AssertionError("font for guideline already set")
        if self._glyph is not None:
            raise AssertionError("glyph for guideline already set")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Layer

    layer = dynamicProperty("layer", "The guideline's parent :class:`BaseLayer`.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    _font = None

    font = dynamicProperty("font", "The guideline's parent :class:`BaseFont`.")

    def _get_font(self):
        if self._font is not None:
            return self._font()
        elif self._glyph is not None:
            return self.glyph.font
        return None

    def _set_font(self, font):
        if self._font is not None:
            raise AssertionError("font for guideline already set")
        if self._glyph is not None:
            raise AssertionError("glyph for guideline already set")
        if font is not None:
            font = reference(font)
        self._font = font

    # --------
    # Position
    # --------

    # x

    x = dynamicProperty(
        "base_x",
        """
        The x coordinate of the guideline.
        It must be an :ref:`type-int-float`. ::

            >>> guideline.x
            100
            >>> guideline.x = 101
        """
    )

    def _get_base_x(self):
        value = self._get_x()
        if value is None:
            return 0
        value = normalizers.normalizeX(value)
        return value

    def _set_base_x(self, value):
        if value is None:
            value = 0
        else:
            value = normalizers.normalizeX(value)
        self._set_x(value)

    def _get_x(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.x`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_x(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.x`. **value** will be
        an :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # y

    y = dynamicProperty(
        "base_y",
        """
        The y coordinate of the guideline.
        It must be an :ref:`type-int-float`. ::

            >>> guideline.y
            100
            >>> guideline.y = 101
        """
    )

    def _get_base_y(self):
        value = self._get_y()
        if value is None:
            return 0
        value = normalizers.normalizeY(value)
        return value

    def _set_base_y(self, value):
        if value is None:
            value = 0
        else:
            value = normalizers.normalizeY(value)
        self._set_y(value)

    def _get_y(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.y`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_y(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.y`. **value** will be
        an :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # angle

    angle = dynamicProperty(
        "base_angle",
        """
        The angle of the guideline.
        It must be an :ref:`type-angle`.
        Please check how :func:`normalizers.normalizeRotationAngle`
        handles the angle. There is a special case, when angle is ``None``.
        If so, when x and y are not 0, the angle will be 0. If x is 0 but y
        is not, the angle will be 0. If y is 0 and x is not, the
        angle will be 90. If both x and y are 0, the angle will be 0.
        ::

            >>> guideline.angle
            45.0
            >>> guideline.angle = 90
        """
    )

    def _get_base_angle(self):
        value = self._get_angle()
        if value is None:
            if self._get_x() != 0 and self._get_y() != 0:
                value = 0
            elif self._get_x() != 0 and self._get_y() == 0:
                value = 90
            elif self._get_x() == 0 and self._get_y() != 0:
                value = 0
            else:
                value = 0
        value = normalizers.normalizeRotationAngle(value)
        return value

    def _set_base_angle(self, value):
        if value is None:
            if self._get_x() != 0 and self._get_y() != 0:
                value = 0
            elif self._get_x() != 0 and self._get_y() == 0:
                value = 90
            elif self._get_x() == 0 and self._get_y() != 0:
                value = 0
            else:
                value = 0
        value = normalizers.normalizeRotationAngle(value)
        self._set_angle(value)

    def _get_angle(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.angle`. This must return an
        :ref:`type-angle`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_angle(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.angle`. **value** will be
        an :ref:`type-angle`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Identification
    # --------------

    # index

    index = dynamicProperty(
        "base_index",
        """
        The index of the guideline within the ordered
        list of the parent glyph's guidelines. This
        attribute is read only. ::

            >>> guideline.index
            0
        """
    )

    def _get_base_index(self):
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self):
        """
        Get the guideline's index.
        This must return an ``int``.

        Subclasses may override this method.
        """
        glyph = self.glyph
        if glyph is not None:
            parent = glyph
        else:
            parent = self.font
        if parent is None:
            return None
        return parent.guidelines.index(self)

    # name

    name = dynamicProperty(
        "base_name",
        """
        The name of the guideline. This will be a
        :ref:`type-string` or ``None``.

            >>> guideline.name
            'my guideline'
            >>> guideline.name = None
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeGuidelineName(value)
        return value

    def _set_base_name(self, value):
        if value is not None:
            value = normalizers.normalizeGuidelineName(value)
        self._set_name(value)

    def _get_name(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.name`. This must return a
        :ref:`type-string` or ``None``. The returned
        value will be normalized with
        :func:`normalizers.normalizeGuidelineName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.name`. **value** will be
        a :ref:`type-string` or ``None``. It will
        have been normalized with
        :func:`normalizers.normalizeGuidelineName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # color

    color = dynamicProperty(
        "base_color",
        """"
        The guideline's color. This will be a
        :ref:`type-color` or ``None``. ::

            >>> guideline.color
            None
            >>> guideline.color = (1, 0, 0, 0.5)
        """
    )

    def _get_base_color(self):
        value = self._get_color()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value):
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

    def _get_color(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.color`. This must return
        a :ref:`type-color` or ``None``. The
        returned value will be normalized with
        :func:`normalizers.normalizeColor`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_color(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.color`. **value** will
        be a :ref:`type-color` or ``None``.
        It will have been normalized with
        :func:`normalizers.normalizeColor`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseGuideline.transformBy`.

        **matrix** will be a :ref:`type-transformation`.
        that has been normalized with :func:`normalizers.normalizeTransformationMatrix`.

        Subclasses may override this method.
        """
        t = transform.Transform(*matrix)
        # coordinates
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y
        # angle
        angle = math.radians(-self.angle)
        dx = math.cos(angle)
        dy = math.sin(angle)
        tdx, tdy = t.transformPoint((dx, dy))
        ta = math.atan2(tdy - t[5], tdx - t[4])
        self.angle = -math.degrees(ta)

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = GuidelineCompatibilityReporter

    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with **other**. ::

            >>> compatible, report = self.isCompatible(otherGuideline)
            >>> compatible
            True
            >>> compatible
            [Warning] Guideline: "xheight" + "cap_height"
            [Warning] Guideline: "xheight" has name xheight | "cap_height" has
                                  name cap_height

        This will return a ``bool`` indicating if the guideline is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        return super(BaseGuideline, self).isCompatible(other, BaseGuideline)

    def _isCompatible(self, other, reporter):
        """
        This is the environment implementation of
        :meth:`BaseGuideline.isCompatible`.

        Subclasses may override this method.
        """
        guideline1 = self
        guideline2 = other
        # guideline names
        if guideline1.name != guideline2.name:
            reporter.nameDifference = True
            reporter.warning = True

    # -------------
    # Normalization
    # -------------

    def round(self):
        """
        Round the guideline's coordinate.

            >>> guideline.round()

        This applies to the following:

        * x
        * y

        It does not apply to

        * angle
        """
        self._round()

    def _round(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseGuideline.round`.

        Subclasses may override this method.
        """
        self.x = normalizers.normalizeVisualRounding(self.x)
        self.y = normalizers.normalizeVisualRounding(self.y)

from fontTools.misc import transform
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    PointPositionMixin,
    SelectionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference
)
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedPoint, RemovedPoint


class BasePoint(
                BaseObject,
                TransformationMixin,
                PointPositionMixin,
                SelectionMixin,
                IdentifierMixin,
                DeprecatedPoint,
                RemovedPoint
                ):

    """
    A point object. This object is almost always
    created with :meth:`BaseContour.appendPoint`,
    the pen returned by :meth:`BaseGlyph.getPen`
    or the point pen returned by :meth:`BaseGLyph.getPointPen`.
    An orphan point can be created like this::

        >>> point = RPoint()
    """

    copyAttributes = (
        "type",
        "smooth",
        "x",
        "y",
        "name"
    )

    def _reprContents(self):
        contents = [
            "%s" % self.type,
            ("({x}, {y})".format(x=self.x, y=self.y)),
        ]
        if self.name is not None:
            contents.append("name='%s'" % self.name)
        if self.smooth:
            contents.append("smooth=%r" % self.smooth)
        return contents

    # -------
    # Parents
    # -------

    # Contour

    _contour = None

    contour = dynamicProperty("contour",
                              "The point's parent :class:`BaseContour`.")

    def _get_contour(self):
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour):
        if self._contour is not None:
            raise AssertionError("contour for point already set")
        if contour is not None:
            contour = reference(contour)
        self._contour = contour

    # Glyph

    glyph = dynamicProperty("glyph", "The point's parent :class:`BaseGlyph`.")

    def _get_glyph(self):
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

    layer = dynamicProperty("layer", "The point's parent :class:`BaseLayer`.")

    def _get_layer(self):
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

    font = dynamicProperty("font", "The point's parent :class:`BaseFont`.")

    def _get_font(self):
        if self._contour is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # type

    type = dynamicProperty(
        "base_type",
        """
        The point type defined with a :ref:`type-string`.
        The possible types are:

        +----------+---------------------------------+
        | move     | An on-curve move to.            |
        +----------+---------------------------------+
        | line     | An on-curve line to.            |
        +----------+---------------------------------+
        | curve    | An on-curve cubic curve to.     |
        +----------+---------------------------------+
        | qcurve   | An on-curve quadratic curve to. |
        +----------+---------------------------------+
        | offcurve | An off-curve.                   |
        +----------+---------------------------------+
        """)

    def _get_base_type(self):
        value = self._get_type()
        value = normalizers.normalizePointType(value)
        return value

    def _set_base_type(self, value):
        value = normalizers.normalizePointType(value)
        self._set_type(value)

    def _get_type(self):
        """
        This is the environment implementation
        of :attr:`BasePoint.type`. This must
        return a :ref:`type-string` defining
        the point type.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_type(self, value):
        """
        This is the environment implementation
        of :attr:`BasePoint.type`. **value**
        will be a :ref:`type-string` defining
        the point type. It will have been normalized
        with :func:`normalizers.normalizePointType`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # smooth

    smooth = dynamicProperty(
        "base_smooth",
        """
        A ``bool`` indicating if the point is smooth or not. ::

            >>> point.smooth
            False
            >>> point.smooth = True

        """
    )

    def _get_base_smooth(self):
        value = self._get_smooth()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_smooth(self, value):
        value = normalizers.normalizeBoolean(value)
        self._set_smooth(value)

    def _get_smooth(self):
        """
        This is the environment implementation of
        :attr:`BasePoint.smooth`. This must return
        a ``bool`` indicating the smooth state.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_smooth(self, value):
        """
        This is the environment implementation of
        :attr:`BasePoint.smooth`. **value** will
        be a ``bool`` indicating the smooth state.
        It will have been normalized with
        :func:`normalizers.normalizeBoolean`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # x

    x = dynamicProperty(
        "base_x",
        """
        The x coordinate of the point.
        It must be an :ref:`type-int-float`. ::

            >>> point.x
            100
            >>> point.x = 101
        """
    )

    def _get_base_x(self):
        value = self._get_x()
        value = normalizers.normalizeX(value)
        return value

    def _set_base_x(self, value):
        value = normalizers.normalizeX(value)
        self._set_x(value)

    def _get_x(self):
        """
        This is the environment implementation of
        :attr:`BasePoint.x`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_x(self, value):
        """
        This is the environment implementation of
        :attr:`BasePoint.x`. **value** will be
        an :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # y

    y = dynamicProperty(
        "base_y",
        """
        The y coordinate of the point.
        It must be an :ref:`type-int-float`. ::

            >>> point.y
            100
            >>> point.y = 101
        """
    )

    def _get_base_y(self):
        value = self._get_y()
        value = normalizers.normalizeY(value)
        return value

    def _set_base_y(self, value):
        value = normalizers.normalizeY(value)
        self._set_y(value)

    def _get_y(self):
        """
        This is the environment implementation of
        :attr:`BasePoint.y`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_y(self, value):
        """
        This is the environment implementation of
        :attr:`BasePoint.y`. **value** will be
        an :ref:`type-int-float`.

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
        The index of the point within the ordered
        list of the parent glyph's point. This
        attribute is read only. ::

            >>> point.index
            0
        """
    )

    def _get_base_index(self):
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self):
        """
        Get the point's index.
        This must return an ``int``.

        Subclasses may override this method.
        """
        contour = self.contour
        if contour is None:
            return None
        return contour.points.index(self)

    # name

    name = dynamicProperty(
        "base_name",
        """
        The name of the point. This will be a
        :ref:`type-string` or ``None``.

            >>> point.name
            'my point'
            >>> point.name = None
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizePointName(value)
        return value

    def _set_base_name(self, value):
        if value is not None:
            value = normalizers.normalizePointName(value)
        self._set_name(value)

    def _get_name(self):
        """
        This is the environment implementation of
        :attr:`BasePoint.name`. This must return a
        :ref:`type-string` or ``None``. The returned
        value will be normalized with
        :func:`normalizers.normalizePointName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value):
        """
        This is the environment implementation of
        :attr:`BasePoint.name`. **value** will be
        a :ref:`type-string` or ``None``. It will
        have been normalized with
        :func:`normalizers.normalizePointName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, **kwargs):
        """
        This is the environment implementation of
        :meth:`BasePoint.transformBy`.

        **matrix** will be a :ref:`type-transformation`.
        that has been normalized with
        :func:`normalizers.normalizeTransformationMatrix`.

        Subclasses may override this method.
        """
        t = transform.Transform(*matrix)
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y

    # -------------
    # Normalization
    # -------------

    def round(self):
        """
        Round the point's coordinate.

            >>> point.round()

        This applies to the following:

        * x
        * y
        """
        self._round()

    def _round(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BasePoint.round`.

        Subclasses may override this method.
        """
        self.x = normalizers.normalizeVisualRounding(self.x)
        self.y = normalizers.normalizeVisualRounding(self.y)

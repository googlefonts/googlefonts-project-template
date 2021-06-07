from fontParts.base.base import (
    BaseObject,
    InterpolationMixin,
    SelectionMixin,
    dynamicProperty,
    reference
)
from fontParts.base import normalizers
from fontParts.base.compatibility import LayerCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedLayer, RemovedLayer


class _BaseGlyphVendor(
                       BaseObject,
                       SelectionMixin,
                       ):

    """
    This class exists to provide common glyph
    interaction code to BaseFont and BaseLayer.
    It should not be directly subclassed.
    """

    # -----------------
    # Glyph Interaction
    # -----------------

    def _setLayerInGlyph(self, glyph):
        if glyph.layer is None:
            if isinstance(self, BaseLayer):
                layer = self
            else:
                layer = self.defaultLayer
            glyph.layer = layer

    def __len__(self):
        """
        An ``int`` representing number of glyphs in the layer. ::

            >>> len(layer)
            256
        """
        return self._len()

    def _len(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__len__` and :meth:`BaseFont.__len__`
        This must return an ``int`` indicating
        the number of glyphs in the layer.

        Subclasses may override this method.
        """
        return len(self.keys())

    def __iter__(self):
        """
        Iterate through the :class:`BaseGlyph` objects in the layer. ::

            >>> for glyph in layer:
            ...     glyph.name
            "A"
            "B"
            "C"
        """
        return self._iter()

    def _iter(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__iter__` and :meth:`BaseFont.__iter__`
        This must return an iterator that returns
        instances of a :class:`BaseGlyph` subclass.

        Subclasses may override this method.
        """
        for name in self.keys():
            yield self[name]

    def __getitem__(self, name):
        """
        Get the :class:`BaseGlyph` with name from the layer. ::

            >>> glyph = layer["A"]
        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            raise KeyError("No glyph named '%s'." % name)
        glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _getItem(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__getitem__` and :meth:`BaseFont.__getitem__`
        This must return an instance of a :class:`BaseGlyph`
        subclass. **name** will be a :ref:`type-string` representing
        a name of a glyph that is in the layer. It will have been
        normalized with :func:`normalizers.normalizeGlyphName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __setitem__(self, name, glyph):
        """
        Insert **glyph** into the layer. ::

            >>> glyph = layer["A"] = otherGlyph

        This will not insert the glyph directly. Rather, a
        new glyph will be created and the data from **glyph**
        will be copied to the new glyph. **name** indicates
        the name that should be assigned to the glyph after
        insertion. If **name** is not given, the glyph's original
        name must be used. If the glyph does not have a name,
        an error must be raised. The data that will be inserted
        from **glyph** is the same data as documented in
        :meth:`BaseGlyph.copy`.
        """
        name = normalizers.normalizeGlyphName(name)
        if name in self:
            del self[name]
        return self._insertGlyph(glyph, name=name)

    def __delitem__(self, name):
        """
        Remove the glyph with name from the layer. ::

            >>> del layer["A"]
        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            raise KeyError("No glyph named '%s'." % name)
        self._removeGlyph(name)

    def keys(self):
        """
        Get a list of all glyphs in the layer. ::

            >>> layer.keys()
            ["B", "C", "A"]

        The order of the glyphs is undefined.
        """
        return self._keys()

    def _keys(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.keys` and :meth:`BaseFont.keys`
        This must return an :ref:`type-immutable-list`
        of the names representing all glyphs in the layer.
        The order is not defined.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __contains__(self, name):
        """
        Test if the layer contains a glyph with **name**. ::

            >>> "A" in layer
            True
        """
        name = normalizers.normalizeGlyphName(name)
        return self._contains(name)

    def _contains(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__contains__` and :meth:`BaseFont.__contains__`
        This must return ``bool`` indicating if the
        layer has a glyph with the defined name.
        **name** will be a :ref-type-string` representing
        a glyph name. It will have been normalized with
        :func:`normalizers.normalizeGlyphName`.

        Subclasses may override this method.
        """
        return name in self.keys()

    def newGlyph(self, name, clear=True):
        """
        Make a new glyph with **name** in the layer. ::

            >>> glyph = layer.newGlyph("A")

        The newly created :class:`BaseGlyph` will be returned.

        If the glyph exists in the layer and clear is set to ``False``,
        the existing glyph will be returned, otherwise the default
        behavior is to clear the exisiting glyph.
        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            glyph = self._newGlyph(name)
        elif clear:
            self.removeGlyph(name)
            glyph = self._newGlyph(name)
        else:
            glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _newGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.newGlyph` and :meth:`BaseFont.newGlyph`
        This must return an instance of a :class:`BaseGlyph` subclass.
        **name** will be a :ref:`type-string` representing
        a glyph name. It will have been normalized with
        :func:`normalizers.normalizeGlyphName`. The
        name will have been tested to make sure that
        no glyph with the same name exists in the layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def removeGlyph(self, name):
        """
        Remove the glyph with name from the layer. ::

            >>> layer.removeGlyph("A")

        This method is deprecated. :meth:`BaseFont.__delitem__` instead.
        """
        del self[name]

    def _removeGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.removeGlyph` and :meth:`BaseFont.removeGlyph`.
        **name** will be a :ref:`type-string` representing a
        glyph name of a glyph that is in the layer. It will
        have been normalized with :func:`normalizers.normalizeGlyphName`.
        The newly created :class:`BaseGlyph` must be returned.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def insertGlyph(self, glyph, name=None):
        """
        Insert **glyph** into the layer. ::

            >>> glyph = layer.insertGlyph(otherGlyph, name="A")

        This method is deprecated. :meth:`BaseFont.__setitem__` instead.
        """
        if name is None:
            name = glyph.name
        self[name] = glyph

    def _insertGlyph(self, glyph, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__setitem__` and :meth:`BaseFont.__setitem__`.
        This must return an instance of a :class:`BaseGlyph` subclass.
        **glyph** will be a glyph object with the attributes necessary
        for copying as defined in :meth:`BaseGlyph.copy` An environment
        must not insert **glyph** directly. Instead the data from
        **glyph** should be copied to a new glyph instead. **name**
        will be a :ref:`type-string` representing a glyph name. It
        will have been normalized with :func:`normalizers.normalizeGlyphName`.
        **name** will have been tested to make sure that no glyph with
        the same name exists in the layer.

        Subclasses may override this method.
        """
        if glyph.name is None or (name != glyph.name and glyph.name in self):
            glyph = glyph.copy()
            glyph.name = name
        dest = self.newGlyph(name, clear=kwargs.get("clear", True))
        dest.copyData(glyph)
        return dest

    # ---------
    # Selection
    # ---------

    selectedGlyphs = dynamicProperty(
        "base_selectedGlyphs",
        """
        A list of glyphs selected in the layer.

        Getting selected glyph objects:

            >>> for glyph in layer.selectedGlyphs:
            ...     glyph.markColor = (1, 0, 0, 0.5)

        Setting selected glyph objects:

            >>> layer.selectedGlyphs = someGlyphs
        """
    )

    def _get_base_selectedGlyphs(self):
        selected = tuple([normalizers.normalizeGlyph(glyph) for glyph in
                         self._get_selectedGlyphs()])
        return selected

    def _get_selectedGlyphs(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self)

    def _set_base_selectedGlyphs(self, value):
        normalized = [normalizers.normalizeGlyph(glyph) for glyph in value]
        self._set_selectedGlyphs(normalized)

    def _set_selectedGlyphs(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self, value)

    selectedGlyphNames = dynamicProperty(
        "base_selectedGlyphNames",
        """
        A list of names of glyphs selected in the layer.

        Getting selected glyph names:

            >>> for name in layer.selectedGlyphNames:
            ...     print(name)

        Setting selected glyph names:

            >>> layer.selectedGlyphNames = ["A", "B", "C"]
        """
    )

    def _get_base_selectedGlyphNames(self):
        selected = tuple([normalizers.normalizeGlyphName(name) for name in
                         self._get_selectedGlyphNames()])
        return selected

    def _get_selectedGlyphNames(self):
        """
        Subclasses may override this method.
        """
        selected = [glyph.name for glyph in self.selectedGlyphs]
        return selected

    def _set_base_selectedGlyphNames(self, value):
        normalized = [normalizers.normalizeGlyphName(name) for name in value]
        self._set_selectedGlyphNames(normalized)

    def _set_selectedGlyphNames(self, value):
        """
        Subclasses may override this method.
        """
        select = [self[name] for name in value]
        self.selectedGlyphs = select

    # --------------------
    # Legacy Compatibility
    # --------------------

    has_key = __contains__


class BaseLayer(_BaseGlyphVendor, InterpolationMixin, DeprecatedLayer, RemovedLayer):

    def _reprContents(self):
        contents = [
           "'%s'" % self.name,
        ]
        if self.color:
            contents.append("color=%r" % str(self.color))
        return contents

    # ----
    # Copy
    # ----

    copyAttributes = (
        "name",
        "color",
        "lib"
    )

    def copy(self):
        """
        Copy the layer into a new layer that does not
        belong to a font. ::

            >>> copiedLayer = layer.copy()

        This will copy:

        * name
        * color
        * lib
        * glyphs
        """
        return super(BaseLayer, self).copy()

    def copyData(self, source):
        """
        Copy data from **source** into this layer.
        Refer to :meth:`BaseLayer.copy` for a list
        of values that will be copied.
        """
        super(BaseLayer, self).copyData(source)
        for name in source.keys():
            glyph = self.newGlyph(name)
            glyph.copyData(source[name])

    # -------
    # Parents
    # -------

    # Font

    _font = None

    font = dynamicProperty(
        "font",
        """
        The layer's parent :class:`BaseFont`. ::

            >>> font = layer.font
        """
    )

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        if self._font is not None:
            raise AssertionError("font for layer already set")
        if font is not None:
            font = reference(font)
        self._font = font

    # --------------
    # Identification
    # --------------

    # name

    name = dynamicProperty(
        "base_name",
        """
        The name of the layer. ::

            >>> layer.name
            "foreground"
            >>> layer.name = "top"
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeLayerName(value)
        return value

    def _set_base_name(self, value):
        if value == self.name:
            return
        value = normalizers.normalizeLayerName(value)
        font = self.font
        if font is not None:
            existing = self.font.layerOrder
            if value in existing:
                raise ValueError("A layer with the name '%s' already exists."
                                 % value)
        self._set_name(value)

    def _get_name(self):
        """
        This is the environment implementation of :attr:`BaseLayer.name`.
        This must return a :ref:`type-string` defining the name of the
        layer. If the layer is the default layer, the returned value
        must be ``None``. It will be normalized with
        :func:`normalizers.normalizeLayerName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value, **kwargs):
        """
        This is the environment implementation of :attr:`BaseLayer.name`.
        **value** will be a :ref:`type-string` defining the name of the
        layer. It will have been normalized with
        :func:`normalizers.normalizeLayerName`.
        No layer with the same name will exist.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # color

    color = dynamicProperty(
        "base_color",
        """
        The layer's color. ::

            >>> layer.color
            None
            >>> layer.color = (1, 0, 0, 0.5)
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
        This is the environment implementation of :attr:`BaseLayer.color`.
        This must return a :ref:`type-color` defining the
        color assigned to the layer. If the layer does not
        have an assigned color, the returned value must be
        ``None``. It will be normalized with
        :func:`normalizers.normalizeColor`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_color(self, value, **kwargs):
        """
        This is the environment implementation of :attr:`BaseLayer.color`.
        **value** will be a :ref:`type-color` or ``None`` defining the
        color to assign to the layer. It will have been normalized with
        :func:`normalizers.normalizeColor`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # lib

    lib = dynamicProperty(
        "lib",
        """
        The layer's :class:`BaseLib` object. ::

            >>> layer.lib["org.robofab.hello"]
            "world"
        """
    )

    def _get_base_lib(self):
        lib = self._get_lib()
        lib.font = self
        return lib

    def _get_lib(self):
        """
        This is the environment implementation of :attr:`BaseLayer.lib`.
        This must return an instance of a :class:`BaseLib` subclass.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Global Operations
    # -----------------

    def round(self):
        """
        Round all approriate data to integers. ::

            >>> layer.round()

        This is the equivalent of calling the round method on:

        * all glyphs in the layer
        """
        self._round()

    def _round(self):
        """
        This is the environment implementation of :meth:`BaseLayer.round`.

        Subclasses may override this method.
        """
        for glyph in self:
            glyph.round()

    def autoUnicodes(self):
        """
        Use heuristics to set Unicode values in all glyphs. ::

            >>> layer.autoUnicodes()

        Environments will define their own heuristics for
        automatically determining values.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        This is the environment implementation of
        :meth:`BaseLayer.autoUnicodes`.

        Subclasses may override this method.
        """
        for glyph in self:
            glyph.autoUnicodes()

    # -------------
    # Interpolation
    # -------------

    def interpolate(self, factor, minLayer, maxLayer, round=True,
                    suppressError=True):
        """
        Interpolate all possible data in the layer. ::

            >>> layer.interpolate(0.5, otherLayer1, otherLayer2)
            >>> layer.interpolate((0.5, 2.0), otherLayer1, otherLayer2, round=False)

        The interpolation occurs on a 0 to 1.0 range where **minLayer**
        is located at 0 and **maxLayer** is located at 1.0. **factor**
        is the interpolation value. It may be less than 0 and greater
        than 1.0. It may be a :ref:`type-int-float` or a tuple of
        two :ref:`type-int-float`. If it is a tuple, the first
        number indicates the x factor and the second number indicates
        the y factor. **round** indicates if the result should be
        rounded to integers. **suppressError** indicates if incompatible
        data should be ignored or if an error should be raised when
        such incompatibilities are found.
        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minLayer, BaseLayer):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__, minLayer.__class__.__name__))
        if not isinstance(maxLayer, BaseLayer):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__, maxLayer.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(factor, minLayer, maxLayer,
                          round=round, suppressError=suppressError)

    def _interpolate(self, factor, minLayer, maxLayer, round=True,
                     suppressError=True):
        """
        This is the environment implementation of
        :meth:`BaseLayer.interpolate`.

        Subclasses may override this method.
        """
        for glyphName in self.keys():
            del self[glyphName]
        for glyphName in minLayer.keys():
            if glyphName not in maxLayer:
                continue
            minGlyph = minLayer[glyphName]
            maxGlyph = maxLayer[glyphName]
            dstGlyph = self.newGlyph(glyphName)
            dstGlyph.interpolate(factor, minGlyph, maxGlyph,
                                 round=round, suppressError=suppressError)

    compatibilityReporterClass = LayerCompatibilityReporter

    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with **other**. ::

            >>> compat, report = self.isCompatible(otherLayer)
            >>> compat
            False
            >>> report
            A
            -
            [Fatal] The glyphs do not contain the same number of contours.

        This will return a ``bool`` indicating if the layer is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        return super(BaseLayer, self).isCompatible(other, BaseLayer)

    def _isCompatible(self, other, reporter):
        """
        This is the environment implementation of
        :meth:`BaseLayer.isCompatible`.

        Subclasses may override this method.
        """
        layer1 = self
        layer2 = other

        # incompatible number of glyphs
        glyphs1 = set(layer1.keys())
        glyphs2 = set(layer2.keys())
        if len(glyphs1) != len(glyphs2):
            reporter.glyphCountDifference = True
            reporter.warning = True
        if len(glyphs1.difference(glyphs2)) != 0:
            reporter.warning = True
            reporter.glyphsMissingFromLayer2 = list(glyphs1.difference(glyphs2))
        if len(glyphs2.difference(glyphs1)) != 0:
            reporter.warning = True
            reporter.glyphsMissingInLayer1 = list(glyphs2.difference(glyphs1))
        # test glyphs
        for glyphName in sorted(glyphs1.intersection(glyphs2)):
            glyph1 = layer1[glyphName]
            glyph2 = layer2[glyphName]
            glyphCompatibility = glyph1.isCompatible(glyph2)[1]
            if glyphCompatibility.fatal or glyphCompatibility.warning:
                if glyphCompatibility.fatal:
                    reporter.fatal = True
                if glyphCompatibility.warning:
                    reporter.warning = True
                reporter.glyphs.append(glyphCompatibility)

    # -------
    # mapping
    # -------

    def getReverseComponentMapping(self):
        """
        Create a dictionary of unicode -> [glyphname, ...] mappings.
        All glyphs are loaded. Note that one glyph can have multiple
        unicode values, and a unicode value can have multiple glyphs
        pointing to it.
        """
        return self._getReverseComponentMapping()

    def _getReverseComponentMapping(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getReverseComponentMapping`.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def getCharacterMapping(self):
        """
        Get a reversed map of component references in the font.
        {
        'A' : ['Aacute', 'Aring']
        'acute' : ['Aacute']
        'ring' : ['Aring']
        etc.
        }
        """
        return self._getCharacterMapping()

    def _getCharacterMapping(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getCharacterMapping`.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

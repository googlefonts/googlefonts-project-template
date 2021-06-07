import os
from fontParts.base.errors import FontPartsError
from fontParts.base.base import dynamicProperty, InterpolationMixin
from fontParts.base.layer import _BaseGlyphVendor
from fontParts.base import normalizers
from fontParts.base.compatibility import FontCompatibilityReporter
from fontParts.base.deprecated import DeprecatedFont, RemovedFont


class BaseFont(
               _BaseGlyphVendor,
               InterpolationMixin,
               DeprecatedFont,
               RemovedFont
               ):

    """
    A font object. This object is almost always
    created with one of the font functions in
    :ref:`fontparts-world`.
    """

    def __init__(self, pathOrObject=None, showInterface=True):
        """
        When constructing a font, the object can be created
        in a new file, from an existing file or from a native
        object. This is defined with the **pathOrObjectArgument**.
        If **pathOrObject** is a string, the string must represent
        an existing file. If **pathOrObject** is an instance of the
        environment's unwrapped native font object, wrap it with
        FontParts. If **pathOrObject** is None, create a new,
        empty font. If **showInterface** is ``False``, the font
        should be created without graphical interface. The default
        for **showInterface** is ``True``.
        """
        super(BaseFont, self).__init__(pathOrObject=pathOrObject,
                                       showInterface=showInterface)

    def _reprContents(self):
        contents = [
            "'%s %s'" % (self.info.familyName, self.info.styleName),
        ]
        if self.path is not None:
            contents.append("path=%r" % self.path)
        return contents

    # ----
    # Copy
    # ----

    copyAttributes = (
        "info",
        "groups",
        "kerning",
        "features",
        "lib",
        "layerOrder",
        "defaultLayerName",
        "glyphOrder"
    )

    def copy(self):
        """
        Copy the font into a new font. ::

            >>> copiedFont = font.copy()

        This will copy:

        * info
        * groups
        * kerning
        * features
        * lib
        * layers
        * layerOrder
        * defaultLayerName
        * glyphOrder
        * guidelines
        """
        return super(BaseFont, self).copy()

    def copyData(self, source):
        """
        Copy data from **source** into this font.
        Refer to :meth:`BaseFont.copy` for a list
        of values that will be copied.
        """
        for layerName in source.layerOrder:
            if layerName in self.layerOrder:
                layer = self.getLayer(layerName)
            else:
                layer = self.newLayer(layerName)
            layer.copyData(source.getLayer(layerName))
        for guideline in self.guidelines:
            self.appendGuideline(guideline)
        super(BaseFont, self).copyData(source)

    # ---------------
    # File Operations
    # ---------------

    # Initialize

    def _init(self, pathOrObject=None, showInterface=True, **kwargs):
        """
        Initialize this object. This should wrap a native font
        object based on the values for **pathOrObject**:

        +--------------------+---------------------------------------------------+
        | None               | Create a new font.                                |
        +--------------------+---------------------------------------------------+
        | string             | Open the font file located at the given location. |
        +--------------------+---------------------------------------------------+
        | native font object | Wrap the given object.                            |
        +--------------------+---------------------------------------------------+

        If **showInterface** is ``False``, the font should be
        created without graphical interface.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # path

    path = dynamicProperty(
        "base_path",
        """
        The path to the file this object represents. ::

            >>> print font.path
            "/path/to/my/font.ufo"
        """
    )

    def _get_base_path(self):
        path = self._get_path()
        if path is not None:
            path = normalizers.normalizeFilePath(path)
        return path

    def _get_path(self, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.path`.

        This must return a :ref:`type-string` defining the
        location of the file or ``None`` indicating that the
        font does not have a file representation. If the
        returned value is not ``None`` it will be normalized
        with :func:`normalizers.normalizeFilePath`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # save

    def save(self, path=None, showProgress=False, formatVersion=None, fileStructure=None):
        """
        Save the font to **path**.

            >>> font.save()
            >>> font.save("/path/to/my/font-2.ufo")

        If **path** is None, use the font's original location.
        The file type must be inferred from the file extension
        of the given path. If no file extension is given, the
        environment may fall back to the format of its choice.
        **showProgress** indicates if a progress indicator should
        be displayed during the operation. Environments may or may
        not implement this behavior. **formatVersion** indicates
        the format version that should be used for writing the given
        file type. For example, if 2 is given for formatVersion
        and the file type being written if UFO, the file is to
        be written in UFO 2 format. This value is not limited
        to UFO format versions. If no format version is given,
        the original format version of the file should be preserved.
        If there is no original format version it is implied that
        the format version is the latest version for the file
        type as supported by the environment. **fileStructure** indicates
        the file structure of the written ufo. The **fileStructure** can
        either be None, 'zip' or 'package', None will use the existing file
        strucure or the default one for unsaved font. 'package' is the default
        file structure and 'zip' will save the font to .ufoz.

        .. note::

           Environments may define their own rules governing when
           a file should be saved into its original location and
           when it should not. For example, a font opened from a
           compiled OpenType font may not be written back into
           the original OpenType font.
        """
        if path is None and self.path is None:
            raise IOError(("The font cannot be saved because no file "
                           "location has been given."))
        if path is not None:
            path = normalizers.normalizeFilePath(path)
        showProgress = bool(showProgress)
        if formatVersion is not None:
            formatVersion = normalizers.normalizeFileFormatVersion(
                formatVersion)
        if fileStructure is not None:
            fileStructure = normalizers.normalizeFileStructure(fileStructure)
        self._save(path=path, showProgress=showProgress,
                   formatVersion=formatVersion, fileStructure=fileStructure)

    def _save(self, path=None, showProgress=False,
              formatVersion=None, fileStructure=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.save`. **path** will be a
        :ref:`type-string` or ``None``. If **path**
        is not ``None``, the value will have been
        normalized with :func:`normalizers.normalizeFilePath`.
        **showProgress** will be a ``bool`` indicating if
        the environment should display a progress bar
        during the operation. Environments are not *required*
        to display a progress bar even if **showProgess**
        is ``True``. **formatVersion** will be :ref:`type-int-float`
        or ``None`` indicating the file format version
        to write the data into. It will have been normalized
        with :func:`normalizers.normalizeFileFormatVersion`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # close

    def close(self, save=False):
        """
        Close the font.

            >>> font.close()

        **save** is a boolean indicating if the font
        should be saved prior to closing. If **save**
        is ``True``, the :meth:`BaseFont.save` method
        will be called. The default is ``False``.
        """
        if save:
            self.save()
        self._close()

    def _close(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.close`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # generate

    @staticmethod
    def generateFormatToExtension(format, fallbackFormat):
        """
        +--------------+--------------------------------------------------------------------+
        | mactype1     | Mac Type 1 font (generates suitcase  and LWFN file)                |
        +--------------+--------------------------------------------------------------------+
        | macttf       | Mac TrueType font (generates suitcase)                             |
        +--------------+--------------------------------------------------------------------+
        | macttdfont   | Mac TrueType font (generates suitcase with resources in data fork) |
        +--------------+--------------------------------------------------------------------+
        | otfcff       | PS OpenType (CFF-based) font (OTF)                                 |
        +--------------+--------------------------------------------------------------------+
        | otfttf       | PC TrueType/TT OpenType font (TTF)                                 |
        +--------------+--------------------------------------------------------------------+
        | pctype1      | PC Type 1 font (binary/PFB)                                        |
        +--------------+--------------------------------------------------------------------+
        | pcmm         | PC MultipleMaster font (PFB)                                       |
        +--------------+--------------------------------------------------------------------+
        | pctype1ascii | PC Type 1 font (ASCII/PFA)                                         |
        +--------------+--------------------------------------------------------------------+
        | pcmmascii    | PC MultipleMaster font (ASCII/PFA)                                 |
        +--------------+--------------------------------------------------------------------+
        | ufo1         | UFO format version 1                                               |
        +--------------+--------------------------------------------------------------------+
        | ufo2         | UFO format version 2                                               |
        +--------------+--------------------------------------------------------------------+
        | ufo3         | UFO format version 3                                               |
        +--------------+--------------------------------------------------------------------+
        | unixascii    | UNIX ASCII font (ASCII/PFA)                                        |
        +--------------+--------------------------------------------------------------------+
        """
        formatToExtension = dict(
            # mactype1=None,
            macttf=".ttf",
            macttdfont=".dfont",
            otfcff=".otf",
            otfttf=".ttf",
            # pctype1=None,
            # pcmm=None,
            # pctype1ascii=None,
            # pcmmascii=None,
            ufo1=".ufo",
            ufo2=".ufo",
            ufo3=".ufo",
            unixascii=".pfa",
        )
        return formatToExtension.get(format, fallbackFormat)

    def generate(self, format, path=None, **environmentOptions):
        """
        Generate the font to another format.

            >>> font.generate("otfcff")
            >>> font.generate("otfcff", "/path/to/my/font.otf")

        **format** defines the file format to output.
        Standard format identifiers can be found in :attr:`BaseFont.generateFormatToExtension`:


        Environments are not required to support all of these
        and environments may define their own format types.
        **path** defines the location where the new file should
        be created. If a file already exists at that location,
        it will be overwritten by the new file. If **path** defines
        a directory, the file will be output as the current
        file name, with the appropriate suffix for the format,
        into the given directory. If no **path** is given, the
        file will be output into the same directory as the source
        font with the file named with the current file name,
        with the appropriate suffix for the format.

        Environments may allow unique keyword arguments in this
        method. For example, if a tool allows decomposing components
        during a generate routine it may allow this:

            >>> font.generate("otfcff", "/p/f.otf", decompose=True)
        """
        import warnings
        if format is None:
            raise ValueError("The format must be defined when generating.")
        elif not isinstance(format, str):
            raise TypeError("The format must be defined as a string.")
        env = {}
        for key, value in environmentOptions.items():
            valid = self._isValidGenerateEnvironmentOption(key)
            if not valid:
                warnings.warn("The %s argument is not supported "
                              "in this environment." % key, UserWarning)
            env[key] = value
        environmentOptions = env
        ext = self.generateFormatToExtension(format, "." + format)
        if path is None and self.path is None:
            raise IOError(("The file cannot be generated because an "
                           "output path was not defined."))
        elif path is None:
            path = os.path.splitext(self.path)[0]
            path += ext
        elif os.path.isdir(path):
            if self.path is None:
                raise IOError(("The file cannot be generated because "
                               "the file does not have a path."))
            fileName = os.path.basename(self.path)
            fileName += ext
            path = os.path.join(path, fileName)
        path = normalizers.normalizeFilePath(path)
        return self._generate(
            format=format,
            path=path,
            environmentOptions=environmentOptions
        )

    @staticmethod
    def _isValidGenerateEnvironmentOption(name):
        """
        Any unknown keyword arguments given to :meth:`BaseFont.generate`
        will be passed to this method. **name** will be the name
        used for the argument. Environments may evaluate if **name**
        is a supported option. If it is, they must return `True` if
        it is not, they must return `False`.

        Subclasses may override this method.
        """
        return False

    def _generate(self, format, path, environmentOptions, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.generate`. **format** will be a
        :ref:`type-string` defining the output format.
        Refer to the :meth:`BaseFont.generate` documentation
        for the standard format identifiers. If the value
        given for **format** is not supported by the environment,
        the environment must raise :exc:`FontPartsError`.
        **path** will be a :ref:`type-string` defining the
        location where the file should be created. It
        will have been normalized with :func:`normalizers.normalizeFilePath`.
        **environmentOptions** will be a dictionary of names
        validated with :meth:`BaseFont._isValidGenerateEnvironmentOption`
        nd the given values. These values will not have been passed
        through any normalization functions.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # info

    info = dynamicProperty(
        "base_info",
        """
        The font's :class:`BaseInfo` object.

            >>> font.info.familyName
            "My Family"
        """
    )

    def _get_base_info(self):
        info = self._get_info()
        info.font = self
        return info

    def _get_info(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.info`. This must return an
        instance of a :class:`BaseInfo` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # groups

    groups = dynamicProperty(
        "base_groups",
        """
        The font's :class:`BaseGroups` object.

            >>> font.groups["myGroup"]
            ["A", "B", "C"]
        """
    )

    def _get_base_groups(self):
        groups = self._get_groups()
        groups.font = self
        return groups

    def _get_groups(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.groups`. This must return
        an instance of a :class:`BaseGroups` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # kerning

    kerning = dynamicProperty(
        "base_kerning",
        """
        The font's :class:`BaseKerning` object.

            >>> font.kerning["A", "B"]
            -100
        """
    )

    def _get_base_kerning(self):
        kerning = self._get_kerning()
        kerning.font = self
        return kerning

    def _get_kerning(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.kerning`. This must return
        an instance of a :class:`BaseKerning` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def getFlatKerning(self):
        """
        Get the font's kerning as a flat dictionary.
        """
        return self._getFlatKerning()

    def _getFlatKerning(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getFlatKerning`.

        Subclasses may override this method.
        """
        kernOrder = {
            (True, True): 0,  # group group
            (True, False): 1,  # group glyph
            (False, True): 2,  # glyph group
            (False, False): 3,  # glyph glyph
        }

        def kerningSortKeyFunc(pair):
            g1, g2 = pair
            g1grp = g1.startswith("public.kern1.")
            g2grp = g2.startswith("public.kern2.")
            return (kernOrder[g1grp, g2grp], pair)

        flatKerning = dict()
        kerning = self.kerning
        groups = self.groups

        for pair in sorted(self.kerning.keys(), key=kerningSortKeyFunc):
            kern = kerning[pair]
            (left, right) = pair
            if left.startswith("public.kern1."):
                left = groups.get(left, [])
            else:
                left = [left]

            if right.startswith("public.kern2."):
                right = groups.get(right, [])
            else:
                right = [right]

            for r in right:
                for l in left:
                    flatKerning[(l, r)] = kern

        return flatKerning

    # features

    features = dynamicProperty(
        "base_features",
        """
        The font's :class:`BaseFeatures` object.

            >>> font.features.text
            "include(features/substitutions.fea);"
        """
    )

    def _get_base_features(self):
        features = self._get_features()
        features.font = self
        return features

    def _get_features(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.features`. This must return
        an instance of a :class:`BaseFeatures` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # lib

    lib = dynamicProperty(
        "base_lib",
        """
        The font's :class:`BaseLib` object.

            >>> font.lib["org.robofab.hello"]
            "world"
        """
    )

    def _get_base_lib(self):
        lib = self._get_lib()
        lib.font = self
        return lib

    def _get_lib(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.lib`. This must return an
        instance of a :class:`BaseLib` subclass.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Layer Interaction
    # -----------------

    layers = dynamicProperty(
        "base_layers",
        """
        The font's :class:`BaseLayer` objects.

            >>> for layer in font.layers:
            ...     layer.name
            "My Layer 1"
            "My Layer 2"
        """
    )

    def _get_base_layers(self):
        layers = self._get_layers()
        for layer in layers:
            self._setFontInLayer(layer)
        return tuple(layers)

    def _get_layers(self, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.layers`. This must return an
        :ref:`type-immutable-list` containing
        instances of :class:`BaseLayer` subclasses.
        The items in the list should be in the order
        defined by :attr:`BaseFont.layerOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # order

    layerOrder = dynamicProperty(
        "base_layerOrder",
        """
        A list of layer names indicating order of the layers in the font.

            >>> font.layerOrder = ["My Layer 2", "My Layer 1"]
            >>> font.layerOrder
            ["My Layer 2", "My Layer 1"]
        """
    )

    def _get_base_layerOrder(self):
        value = self._get_layerOrder()
        value = normalizers.normalizeLayerOrder(value, self)
        return list(value)

    def _set_base_layerOrder(self, value):
        value = normalizers.normalizeLayerOrder(value, self)
        self._set_layerOrder(value)

    def _get_layerOrder(self, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.layerOrder`. This must return an
        :ref:`type-immutable-list` defining the order of
        the layers in the font. The contents of the list
        must be layer names as :ref:`type-string`. The
        list will be normalized with :func:`normalizers.normalizeLayerOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_layerOrder(self, value, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.layerOrder`. **value** will
        be a **list** of :ref:`type-string` representing
        layer names. The list will have been normalized
        with :func:`normalizers.normalizeLayerOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # default layer

    def _setFontInLayer(self, layer):
        if layer.font is None:
            layer.font = self

    defaultLayerName = dynamicProperty(
        "base_defaultLayerName",
        """
        The name of the font's default layer.

            >>> font.defaultLayerName = "My Layer 2"
            >>> font.defaultLayerName
            "My Layer 2"
        """
    )

    def _get_base_defaultLayerName(self):
        value = self._get_defaultLayerName()
        value = normalizers.normalizeDefaultLayerName(value, self)
        return value

    def _set_base_defaultLayerName(self, value):
        value = normalizers.normalizeDefaultLayerName(value, self)
        self._set_defaultLayerName(value)

    def _get_defaultLayerName(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.defaultLayerName`. Return the
        name of the default layer as a :ref:`type-string`.
        The name will be normalized with
        :func:`normalizers.normalizeDefaultLayerName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_defaultLayerName(self, value, **kwargs):
        """
        This is the environment implementation of
        :attr:`BaseFont.defaultLayerName`. **value**
        will be a :ref:`type-string`. It will have
        been normalized with :func:`normalizers.normalizeDefaultLayerName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    defaultLayer = dynamicProperty(
        "base_defaultLayer",
        """
        The font's default layer.

            >>> layer = font.defaultLayer
            >>> font.defaultLayer = otherLayer
        """
    )

    def _get_defaultLayer(self):
        layer = self._get_base_defaultLayer()
        layer = normalizers.normalizeLayer(layer)
        return layer

    def _set_defaultLayer(self, layer):
        layer = normalizers.normalizeLayer(layer)
        self._set_base_defaultLayer(layer)

    def _get_base_defaultLayer(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.defaultLayer`. Return the
        default layer as a :class:`BaseLayer` object.
        The layer will be normalized with
        :func:`normalizers.normalizeLayer`.

        Subclasses must override this method.
        """
        name = self.defaultLayerName
        layer = self.getLayer(name)
        return layer

    def _set_base_defaultLayer(self, value):
        """
        This is the environment implementation of
        :attr:`BaseFont.defaultLayer`. **value**
        will be a :class:`BaseLayer`. It will have
        been normalized with :func:`normalizers.normalizeLayer`.

        Subclasses must override this method.
        """
        self.defaultLayerName = value.name

    # get

    def getLayer(self, name):
        """
        Get the :class:`BaseLayer` with **name**.

            >>> layer = font.getLayer("My Layer 2")
        """
        name = normalizers.normalizeLayerName(name)
        if name not in self.layerOrder:
            raise ValueError("No layer with the name '%s' exists." % name)
        layer = self._getLayer(name)
        self._setFontInLayer(layer)
        return layer

    def _getLayer(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.getLayer`. **name** will
        be a :ref:`type-string`. It will have been
        normalized with :func:`normalizers.normalizeLayerName`
        and it will have been verified as an existing layer.
        This must return an instance of :class:`BaseLayer`.

        Subclasses may override this method.
        """
        for layer in self.layers:
            if layer.name == name:
                return layer

    # new

    def newLayer(self, name, color=None):
        """
        Make a new layer with **name** and **color**.
        **name** must be a :ref:`type-string` and
        **color** must be a :ref:`type-color` or ``None``.

            >>> layer = font.newLayer("My Layer 3")

        The will return the newly created
        :class:`BaseLayer`.
        """
        name = normalizers.normalizeLayerName(name)
        if name in self.layerOrder:
            layer = self.getLayer(name)
            if color is not None:
                layer.color = color
            return layer
        if color is not None:
            color = normalizers.normalizeColor(color)
        layer = self._newLayer(name=name, color=color)
        self._setFontInLayer(layer)
        return layer

    def _newLayer(self, name, color, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.newLayer`. **name** will be
        a :ref:`type-string` representing a valid
        layer name. The value will have been normalized
        with :func:`normalizers.normalizeLayerName` and
        **name** will not be the same as the name of
        an existing layer. **color** will be a
        :ref:`type-color` or ``None``. If the value
        is not ``None`` the value will have been
        normalized with :func:`normalizers.normalizeColor`.
        This must return an instance of a :class:`BaseLayer`
        subclass that represents the new layer.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, name):
        """
        Remove the layer with **name** from the font.

            >>> font.removeLayer("My Layer 3")
        """
        name = normalizers.normalizeLayerName(name)
        if name not in self.layerOrder:
            raise ValueError("No layer with the name '%s' exists." % name)
        self._removeLayer(name)

    def _removeLayer(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.removeLayer`. **name** will
        be a :ref:`type-string` defining the name
        of an existing layer. The value will have
        been normalized with :func:`normalizers.normalizeLayerName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # insert

    def insertLayer(self, layer, name=None):
        """
        Insert **layer** into the font. ::

            >>> layer = font.insertLayer(otherLayer, name="layer 2")

        This will not insert the layer directly.
        Rather, a new layer will be created and the data from
        **layer** will be copied to to the new layer. **name**
        indicates the name that should be assigned to the layer
        after insertion. If **name** is not given, the layer's
        original name must be used. If the layer does not have
        a name, an error must be raised. The data that will be
        inserted from **layer** is the same data as documented
        in :meth:`BaseLayer.copy`.
        """
        if name is None:
            name = layer.name
        name = normalizers.normalizeLayerName(name)
        if name in self:
            self.removeLayer(name)
        return self._insertLayer(layer, name=name)

    def _insertLayer(self, layer, name, **kwargs):
        """
        This is the environment implementation of :meth:`BaseFont.insertLayer`.
        This must return an instance of a :class:`BaseLayer` subclass.
        **layer** will be a layer object with the attributes necessary
        for copying as defined in :meth:`BaseLayer.copy` An environment
        must not insert **layer** directly. Instead the data from **layer**
        should be copied to a new layer. **name** will be a :ref:`type-string`
        representing a glyph layer. It will have been normalized with
        :func:`normalizers.normalizeLayerName`. **name** will have been
        tested to make sure that no layer with the same name exists in the font.

        Subclasses may override this method.
        """
        if name != layer.name and layer.name in self.layerOrder:
            layer = layer.copy()
            layer.name = name
        dest = self.newLayer(name)
        dest.copyData(layer)
        return dest

    # duplicate

    def duplicateLayer(self, layerName, newLayerName):
        """
        Duplicate the layer with **layerName**, assign
        **newLayerName** to the new layer and insert the
        new layer into the font. ::

            >>> layer = font.duplicateLayer("layer 1", "layer 2")
        """
        layerOrder = self.layerOrder
        layerName = normalizers.normalizeLayerName(layerName)
        if layerName not in layerOrder:
            raise ValueError("No layer with the name '%s' exists." % layerName)
        newLayerName = normalizers.normalizeLayerName(newLayerName)
        if newLayerName in layerOrder:
            raise ValueError("A layer with the name '%s' already exists." % newLayerName)
        newLayer = self._duplicateLayer(layerName, newLayerName)
        newLayer = normalizers.normalizeLayer(newLayer)
        return newLayer

    def _duplicateLayer(self, layerName, newLayerName):
        """
        This is the environment implementation of :meth:`BaseFont.duplicateLayer`.
        **layerName** will be a :ref:`type-string` representing a valid layer name.
        The value will have been normalized with :func:`normalizers.normalizeLayerName`
        and **layerName** will be a layer that exists in the font. **newLayerName**
        will be a :ref:`type-string` representing a valid layer name. The value will
        have been normalized with :func:`normalizers.normalizeLayerName` and
        **newLayerName** will have been tested to make sure that no layer with
        the same name exists in the font. This must return an instance of a
        :class:`BaseLayer` subclass.

        Subclasses may override this method.
        """
        newLayer = self.getLayer(layerName).copy()
        return self.insertLayer(newLayer, newLayerName)

    def swapLayerNames(self, layerName, otherLayerName):
        """
        Assign **layerName** to the layer currently named
        **otherLayerName** and assign the name **otherLayerName**
        to the layer currently named **layerName**.

            >>> font.swapLayerNames("before drawing revisions", "after drawing revisions")
        """
        layerOrder = self.layerOrder
        layerName = normalizers.normalizeLayerName(layerName)
        if layerName not in layerOrder:
            raise ValueError("No layer with the name '%s' exists." % layerName)
        otherLayerName = normalizers.normalizeLayerName(otherLayerName)
        if otherLayerName not in layerOrder:
            raise ValueError("No layer with the name '%s' exists." % otherLayerName)
        self._swapLayers(layerName, otherLayerName)

    def _swapLayers(self, layerName, otherLayerName):
        """
        This is the environment implementation of :meth:`BaseFont.swapLayerNames`.
        **layerName** will be a :ref:`type-string` representing a valid layer name.
        The value will have been normalized with :func:`normalizers.normalizeLayerName`
        and **layerName** will be a layer that exists in the font. **otherLayerName**
        will be a :ref:`type-string` representing a valid layer name. The value will
        have been normalized with :func:`normalizers.normalizeLayerName` and
        **otherLayerName** will be a layer that exists in the font.

        Subclasses may override this method.
        """
        import random
        layer1 = self.getLayer(layerName)
        layer2 = self.getLayer(otherLayerName)
        # make a temporary name and assign it to
        # the first layer to prevent two layers
        # from having the same name at once.
        layerOrder = self.layerOrder
        for _ in range(50):
            # shout out to PostScript unique IDs
            tempLayerName = str(random.randint(4000000, 4999999))
            if tempLayerName not in layerOrder:
                break
        if tempLayerName in layerOrder:
            raise FontPartsError(("Couldn't find a temporary layer name "
                                  "after 50 tries. Sorry. Please try again."))
        layer1.name = tempLayerName
        # now swap
        layer2.name = layerName
        layer1.name = otherLayerName

    # -----------------
    # Glyph Interaction
    # -----------------

    # base implementation overrides

    def _getItem(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.__getitem__`. **name** will
        be a :ref:`type-string` defining an existing
        glyph in the default layer. The value will
        have been normalized with :func:`normalizers.normalizeGlyphName`.

        Subclasses may override this method.
        """
        layer = self.defaultLayer
        return layer[name]

    def _keys(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.keys`. This must return an
        :ref:`type-immutable-list` of all glyph names
        in the default layer.

        Subclasses may override this method.
        """
        layer = self.defaultLayer
        return layer.keys()

    def _newGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.newGlyph`. **name** will be
        a :ref:`type-string` representing a valid
        glyph name. The value will have been tested
        to make sure that an existing glyph in the
        default layer does not have an identical name.
        The value will have been normalized with
        :func:`normalizers.normalizeGlyphName`. This
        must return an instance of :class:`BaseGlyph`
        representing the new glyph.

        Subclasses may override this method.
        """
        layer = self.defaultLayer
        # clear is False here because the base newFont
        # that has called this method will have already
        # handled the clearing as specified by the caller.
        return layer.newGlyph(name, clear=False)

    def _removeGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.removeGlyph`. **name** will
        be a :ref:`type-string` representing an
        existing glyph in the default layer. The
        value will have been normalized with
        :func:`normalizers.normalizeGlyphName`.

        Subclasses may override this method.
        """
        layer = self.defaultLayer
        layer.removeGlyph(name)

    def __setitem__(self, name, glyph):
        """
        Insert **glyph** into the font. ::

            >>> glyph = font["A"] = otherGlyph

        This will not insert the glyph directly. Rather, a
        new glyph will be created and the data from **glyph**
        will be copied to the new glyph. **name** indicates
        the name that should be assigned to the glyph after
        insertion. The data that will be inserted
        from **glyph** is the same data as documented in
        :meth:`BaseGlyph.copy`.

        On a font level **font.glyphOrder** will be preserved
        if the **name** is already present.
        """
        name = normalizers.normalizeGlyphName(name)
        if name in self:
            # clear the glyph here if the glyph exists
            dest = self._getItem(name)
            dest.clear()
        return self._insertGlyph(glyph, name=name, clear=False)

    # order

    glyphOrder = dynamicProperty(
        "base_glyphOrder",
        """
        The preferred order of the glyphs in the font.

            >>> font.glyphOrder
            ["C", "B", "A"]
            >>> font.glyphOrder = ["A", "B", "C"]
        """
    )

    def _get_base_glyphOrder(self):
        value = self._get_glyphOrder()
        value = normalizers.normalizeGlyphOrder(value)
        return value

    def _set_base_glyphOrder(self, value):
        value = normalizers.normalizeGlyphOrder(value)
        self._set_glyphOrder(value)

    def _get_glyphOrder(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.glyphOrder`. This must return
        an :ref:`type-immutable-list` containing glyph
        names representing the glyph order in the font.
        The value will be normalized with
        :func:`normalizers.normalizeGlyphOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_glyphOrder(self, value):
        """
        This is the environment implementation of
        :attr:`BaseFont.glyphOrder`. **value** will
        be a list of :ref:`type-string`. It will
        have been normalized with
        :func:`normalizers.normalizeGlyphOrder`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------------
    # Global Operations
    # -----------------

    def round(self):
        """
        Round all approriate data to integers.

            >>> font.round()

        This is the equivalent of calling the round method on:

        * info
        * kerning
        * the default layer
        * font-level guidelines

        This applies only to the default layer.
        """
        self._round()

    def _round(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.round`.

        Subclasses may override this method.
        """
        layer = self.defaultLayer
        layer.round()
        self.info.round()
        self.kerning.round()
        for guideline in self.guidelines:
            guideline.round()

    def autoUnicodes(self):
        """
        Use heuristics to set Unicode values in all glyphs.

            >>> font.autoUnicodes()

        Environments will define their own heuristics for
        automatically determining values.

        This applies only to the default layer.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.autoUnicodes`.

        Subclasses may override this method.
        """
        layer = self.defaultLayer
        layer.autoUnicodes()

    # ----------
    # Guidelines
    # ----------

    def _setFontInGuideline(self, guideline):
        if guideline.font is None:
            guideline.font = self

    guidelines = dynamicProperty(
        "guidelines",
        """
        An :ref:`type-immutable-list` of font-level :class:`BaseGuideline` objects.

            >>> for guideline in font.guidelines:
            ...     guideline.angle
            0
            45
            90
        """
    )

    def _get_guidelines(self):
        """
        This is the environment implementation of
        :attr:`BaseFont.guidelines`. This must
        return an :ref:`type-immutable-list` of
        :class:`BaseGuideline` objects.

        Subclasses may override this method.
        """
        return tuple([self._getitem__guidelines(i)
                      for i in range(self._len__guidelines())])

    def _len__guidelines(self):
        return self._lenGuidelines()

    def _lenGuidelines(self, **kwargs):
        """
        This must return an integer indicating
        the number of font-level guidelines
        in the font.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__guidelines(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__guidelines():
            raise ValueError("No guideline located at index %d." % index)
        guideline = self._getGuideline(index)
        self._setFontInGuideline(guideline)
        return guideline

    def _getGuideline(self, index, **kwargs):
        """
        This must return a :class:`BaseGuideline` object.
        **index** will be a valid **index**.

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
        Append a new guideline to the font.

            >>> guideline = font.appendGuideline((50, 0), 90)
            >>> guideline = font.appendGuideline((0, 540), 0, name="overshoot",
            >>> color=(0, 0, 0, 0.2))

        **position** must be a :ref:`type-coordinate`
        indicating the position of the guideline.
        **angle** indicates the :ref:`type-angle` of
        the guideline. **name** indicates the name
        for the guideline. This must be a :ref:`type-string`
        or ``None``. **color** indicates the color for
        the guideline. This must be a :ref:`type-color`
        or ``None``. This will return the newly created
        :class:`BaseGuidline` object.

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
        guideline.font = self
        return guideline

    def _appendGuideline(self, position, angle, name=None, color=None, identifier=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseFont.appendGuideline`. **position**
        will be a valid :ref:`type-coordinate`. **angle**
        will be a valid angle. **name** will be a valid
        :ref:`type-string` or ``None``. **color** will
        be a valid :ref:`type-color` or ``None``.
        This must return the newly created
        :class:`BaseGuideline` object.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline):
        """
        Remove **guideline** from the font.

            >>> font.removeGuideline(guideline)
            >>> font.removeGuideline(2)

        **guideline** can be a guideline object or
        an integer representing the guideline index.
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
        This is the environment implementation of
        :meth:`BaseFont.removeGuideline`. **index**
        will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearGuidelines(self):
        """
        Clear all guidelines.

            >>> font.clearGuidelines()
        """
        self._clearGuidelines()

    def _clearGuidelines(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.clearGuidelines`.

        Subclasses may override this method.
        """
        for _ in range(self._len__guidelines()):
            self.removeGuideline(-1)

    # -------------
    # Interpolation
    # -------------

    def interpolate(self, factor, minFont, maxFont,
                    round=True, suppressError=True):
        """
        Interpolate all possible data in the font.

            >>> font.interpolate(0.5, otherFont1, otherFont2)
            >>> font.interpolate((0.5, 2.0), otherFont1, otherFont2, round=False)

        The interpolation occurs on a 0 to 1.0 range where **minFont**
        is located at 0 and **maxFont** is located at 1.0. **factor**
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
        if not isinstance(minFont, BaseFont):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__, minFont.__class__.__name__))
        if not isinstance(maxFont, BaseFont):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__, maxFont.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(factor, minFont, maxFont,
                          round=round, suppressError=suppressError)

    def _interpolate(self, factor, minFont, maxFont,
                     round=True, suppressError=True):
        """
        This is the environment implementation of
        :meth:`BaseFont.interpolate`.

        Subclasses may override this method.
        """
        # layers
        for layerName in self.layerOrder:
            self.removeLayer(layerName)
        for layerName in minFont.layerOrder:
            if layerName not in maxFont.layerOrder:
                continue
            minLayer = minFont.getLayer(layerName)
            maxLayer = maxFont.getLayer(layerName)
            dstLayer = self.newLayer(layerName)
            dstLayer.interpolate(factor, minLayer, maxLayer,
                                 round=round, suppressError=suppressError)
        if self.layerOrder:
            self.defaultLayer = self.getLayer(self.layerOrder[0])
        # kerning and groups
        self.kerning.interpolate(factor, minFont.kerning, maxFont.kerning,
                                 round=round, suppressError=suppressError)
        # info
        self.info.interpolate(factor, minFont.info, maxFont.info,
                              round=round, suppressError=suppressError)

    compatibilityReporterClass = FontCompatibilityReporter

    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with **other**.

            >>> compatible, report = self.isCompatible(otherFont)
            >>> compatible
            False
            >>> report
            [Fatal] Glyph: "test1" + "test2"
            [Fatal] Glyph: "test1" contains 1 contours | "test2" contains 2 contours

        This will return a ``bool`` indicating if the font is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        return super(BaseFont, self).isCompatible(other, BaseFont)

    def _isCompatible(self, other, reporter):
        """
        This is the environment implementation of
        :meth:`BaseFont.isCompatible`.

        Subclasses may override this method.
        """
        font1 = self
        font2 = other

        # incompatible guidelines
        guidelines1 = set(font1.guidelines)
        guidelines2 = set(font2.guidelines)
        if len(guidelines1) != len(guidelines2):
            reporter.warning = True
            reporter.guidelineCountDifference = True
        if len(guidelines1.difference(guidelines2)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingFromFont2 = list(
                guidelines1.difference(guidelines2))
        if len(guidelines2.difference(guidelines1)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingInFont1 = list(
                guidelines2.difference(guidelines1))
        # incompatible layers
        layers1 = set(font1.layerOrder)
        layers2 = set(font2.layerOrder)
        if len(layers1) != len(layers2):
            reporter.warning = True
            reporter.layerCountDifference = True
        if len(layers1.difference(layers2)) != 0:
            reporter.warning = True
            reporter.layersMissingFromFont2 = list(layers1.difference(layers2))
        if len(layers2.difference(layers1)) != 0:
            reporter.warning = True
            reporter.layersMissingInFont1 = list(layers2.difference(layers1))
        # test layers
        for layerName in sorted(layers1.intersection(layers2)):
            layer1 = font1.getLayer(layerName)
            layer2 = font2.getLayer(layerName)
            layerCompatibility = layer1.isCompatible(layer2)[1]
            if layerCompatibility.fatal or layerCompatibility.warning:
                if layerCompatibility.fatal:
                    reporter.fatal = True
                if layerCompatibility.warning:
                    reporter.warning = True
                reporter.layers.append(layerCompatibility)

    # -------
    # mapping
    # -------

    def getReverseComponentMapping(self):
        """
        Create a dictionary of unicode -> [glyphname, ...] mappings.
        All glyphs are loaded. Note that one glyph can have multiple unicode values,
        and a unicode value can have multiple glyphs pointing to it.
        """
        return self._getReverseComponentMapping()

    def _getReverseComponentMapping(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getReverseComponentMapping`.

        Subclasses may override this method.
        """
        layer = self.defaultLayer
        return layer.getReverseComponentMapping()

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
        layer = self.defaultLayer
        return layer.getCharacterMapping()

    # ---------
    # Selection
    # ---------

    # layers

    selectedLayers = dynamicProperty(
        "base_selectedLayers",
        """
        A list of layers selected in the layer.

        Getting selected layer objects:

            >>> for layer in layer.selectedLayers:
            ...     layer.color = (1, 0, 0, 0.5)

        Setting selected layer objects:

            >>> layer.selectedLayers = someLayers
        """
    )

    def _get_base_selectedLayers(self):
        selected = tuple([normalizers.normalizeLayer(layer) for
                          layer in self._get_selectedLayers()])
        return selected

    def _get_selectedLayers(self):
        """
        Subclasses may override this method.
        """
        return self._getSelectedSubObjects(self.layers)

    def _set_base_selectedLayers(self, value):
        normalized = [normalizers.normalizeLayer(layer) for layer in value]
        self._set_selectedLayers(normalized)

    def _set_selectedLayers(self, value):
        """
        Subclasses may override this method.
        """
        return self._setSelectedSubObjects(self.layers, value)

    selectedLayerNames = dynamicProperty(
        "base_selectedLayerNames",
        """
        A list of names of layers selected in the layer.

        Getting selected layer names:

            >>> for name in layer.selectedLayerNames:
            ...     print(name)

        Setting selected layer names:

            >>> layer.selectedLayerNames = ["A", "B", "C"]
        """
    )

    def _get_base_selectedLayerNames(self):
        selected = tuple([normalizers.normalizeLayerName(name) for
                          name in self._get_selectedLayerNames()])
        return selected

    def _get_selectedLayerNames(self):
        """
        Subclasses may override this method.
        """
        selected = [layer.name for layer in self.selectedLayers]
        return selected

    def _set_base_selectedLayerNames(self, value):
        normalized = [normalizers.normalizeLayerName(name) for name in value]
        self._set_selectedLayerNames(normalized)

    def _set_selectedLayerNames(self, value):
        """
        Subclasses may override this method.
        """
        select = [self.layers(name) for name in value]
        self.selectedLayers = select

    # guidelines

    selectedGuidelines = dynamicProperty(
        "base_selectedGuidelines",
        """
        A list of guidelines selected in the font.

        Getting selected guideline objects:

            >>> for guideline in font.selectedGuidelines:
            ...     guideline.color = (1, 0, 0, 0.5)

        Setting selected guideline objects:

            >>> font.selectedGuidelines = someGuidelines

        Setting also supports guideline indexes:

            >>> font.selectedGuidelines = [0, 2]
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

from fontParts.base.base import BaseDict, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedLib, RemovedLib


class BaseLib(BaseDict, DeprecatedLib, RemovedLib):

    """
    A Lib object. This object normally created as part of a
    :class:`BaseFont`. An orphan Lib object can be created like this::

        >>> lib = RLib()

    This object behaves like a Python dictionary. Most of the dictionary
    functionality comes from :class:`BaseDict`, look at that object for the
    required environment implementation details.

    Lib uses :func:`normalizers.normalizeLibKey` to normalize the key of
    the ``dict``, and :func:`normalizers.normalizeLibValue` to normalize the
    value of the ``dict``.
    """

    keyNormalizer = normalizers.normalizeLibKey
    valueNormalizer = normalizers.normalizeLibValue

    def _reprContents(self):
        contents = []
        if self.glyph is not None:
            contents.append("in glyph")
            contents += self.glyph._reprContents()
        if self.font:
            contents.append("in font")
            contents += self.font._reprContents()
        return contents

    # -------
    # Parents
    # -------

    # Glyph

    _glyph = None

    glyph = dynamicProperty("glyph", "The lib's parent glyph.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph):
        if self._font is not None:
            raise AssertionError("font for lib already set")
        if self._glyph is not None and self._glyph() != glyph:
            raise AssertionError("glyph for lib already set and is not same as glyph")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Font

    _font = None

    font = dynamicProperty("font", "The lib's parent font.")

    def _get_font(self):
        if self._font is not None:
            return self._font()
        elif self._glyph is not None:
            return self.glyph.font
        return None

    def _set_font(self, font):
        if self._font is not None and self._font() != font:
            raise AssertionError("font for lib already set and is not same as font")
        if self._glyph is not None:
            raise AssertionError("glyph for lib already set")
        if font is not None:
            font = reference(font)
        self._font = font

    # Layer

    layer = dynamicProperty("layer", "The lib's parent layer.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def remove(self, key):
        """
        Removes a key from the Lib. **key** will be
        a :ref:`type-string` that is the key to
        be removed.

        This is a backwards compatibility method.
        """
        del self[key]

    def asDict(self):
        """
        Return the Lib as a ``dict``.

        This is a backwards compatibility method.
        """
        d = {}
        for k, v in self.items():
            d[k] = v
        return d

    # -------------------
    # Inherited Functions
    # -------------------

    def __contains__(self, key):
        """
        Tests to see if a lib name is in the Lib.
        **key** will be a :ref:`type-string`.
        This returns a ``bool`` indicating if the **key**
        is in the Lib. ::

            >>> "public.glyphOrder" in font.lib
            True
        """
        return super(BaseLib, self).__contains__(key)

    def __delitem__(self, key):
        """
        Removes **key** from the Lib. **key** is a :ref:`type-string`.::

            >>> del font.lib["public.glyphOrder"]
        """
        super(BaseLib, self).__delitem__(key)

    def __getitem__(self, key):
        """
        Returns the contents of the named lib. **key** is a
        :ref:`type-string`.
        The returned value will be a ``list`` of the lib contents.::

            >>> font.lib["public.glyphOrder"]
            ["A", "B", "C"]

        It is important to understand that any changes to the returned lib
        contents will not be reflected in the Lib object. If one wants to
        make a change to the lib contents, one should do the following::

            >>> lib = font.lib["public.glyphOrder"]
            >>> lib.remove("A")
            >>> font.lib["public.glyphOrder"] = lib
        """
        return super(BaseLib, self).__getitem__(key)

    def __iter__(self):
        """
        Iterates through the Lib, giving the key for each iteration. The
        order that the Lib will iterate though is not fixed nor is it
        ordered.::

            >>> for key in font.lib:
            >>>     print key
            "public.glyphOrder"
            "org.robofab.scripts.SomeData"
            "public.postscriptNames"
        """
        return super(BaseLib, self).__iter__()

    def __len__(self):
        """
        Returns the number of keys in Lib as an ``int``.::

            >>> len(font.lib)
            5
        """
        return super(BaseLib, self).__len__()

    def __setitem__(self, key, items):
        """
        Sets the **key** to the list of **items**. **key**
        is the lib name as a :ref:`type-string` and **items** is a
        ``list`` of items as :ref:`type-string`.

            >>> font.lib["public.glyphOrder"] = ["A", "B", "C"]
        """
        super(BaseLib, self).__setitem__(key, items)

    def clear(self):
        """
        Removes all keys from Lib,
        resetting the Lib to an empty dictionary. ::

            >>> font.lib.clear()
        """
        super(BaseLib, self).clear()

    def get(self, key, default=None):
        """
        Returns the contents of the named key.
        **key** is a :ref:`type-string`, and the returned values will
        either be ``list`` of key contents or ``None`` if no key was
        found. ::

            >>> font.lib["public.glyphOrder"]
            ["A", "B", "C"]

        It is important to understand that any changes to the returned key
        contents will not be reflected in the Lib object. If one wants to
        make a change to the key contents, one should do the following::

            >>> lib = font.lib["public.glyphOrder"]
            >>> lib.remove("A")
            >>> font.lib["public.glyphOrder"] = lib
        """
        return super(BaseLib, self).get(key, default)

    def items(self):
        """
        Returns a list of ``tuple`` of each key name and key items.
        Keys are :ref:`type-string` and key members are a ``list``
        of :ref:`type-string`. The initial list will be unordered.

            >>> font.lib.items()
            [("public.glyphOrder", ["A", "B", "C"]),
             ("public.postscriptNames", {'be': 'uni0431', 'ze': 'uni0437'})]
        """
        return super(BaseLib, self).items()

    def keys(self):
        """
        Returns a ``list`` of all the key names in Lib. This list will be
        unordered.::

            >>> font.lib.keys()
            ["public.glyphOrder", "org.robofab.scripts.SomeData",
             "public.postscriptNames"]
        """
        return super(BaseLib, self).keys()

    def pop(self, key, default=None):
        """
        Removes the **key** from the Lib and returns the ``list`` of
        key members. If no key is found, **default** is returned.
        **key** is a :ref:`type-string`. This must return either
        **default** or a ``list`` of items as :ref:`type-string`.

            >>> font.lib.pop("public.glyphOrder")
            ["A", "B", "C"]
        """
        return super(BaseLib, self).pop(key, default)

    def update(self, otherLib):
        """
        Updates the Lib based on **otherLib**. *otherLib** is a
        ``dict`` of keys. If a key from **otherLib** is in Lib
        the key members will be replaced by the key members from
        **otherLib**. If a key from **otherLib** is not in the Lib,
        it is added to the Lib. If Lib contain a key name that is not
        in *otherLib**, it is not changed.

            >>> font.lib.update(newLib)
        """
        super(BaseLib, self).update(otherLib)

    def values(self):
        """
        Returns a ``list`` of each named key's members. This will be a list
        of lists, the key members will be a ``list`` of :ref:`type-string`.
        The initial list will be unordered.

            >>> font.lib.items()
            [["A", "B", "C"], {'be': 'uni0431', 'ze': 'uni0437'}]
        """
        return super(BaseLib, self).values()

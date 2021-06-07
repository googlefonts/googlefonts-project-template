from fontParts.base.base import BaseObject, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedFeatures, RemovedFeatures


class BaseFeatures(BaseObject, DeprecatedFeatures, RemovedFeatures):

    copyAttributes = ("text",)

    def _reprContents(self):
        contents = []
        if self.font is not None:
            contents.append("for font")
            contents += self.font._reprContents()
        return contents

    # -------
    # Parents
    # -------

    # Font

    _font = None

    font = dynamicProperty("font", "The features' parent :class:`BaseFont`.")

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        if self._font is not None and self._font() != font:
            raise AssertionError("font for features already set and is not same as font")
        if font is not None:
            font = reference(font)
        self._font = font

    # ----
    # Text
    # ----

    text = dynamicProperty(
        "base_text",
        """
        The `.fea formated
        <http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html>`_
        text representing the features.
        It must be a :ref:`type-string`.
        """
    )

    def _get_base_text(self):
        value = self._get_text()
        if value is not None:
            value = normalizers.normalizeFeatureText(value)
        return value

    def _set_base_text(self, value):
        if value is not None:
            value = normalizers.normalizeFeatureText(value)
        self._set_text(value)

    def _get_text(self):
        """
        This is the environment implementation of
        :attr:`BaseFeatures.text`. This must return a
        :ref:`type-string`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_text(self, value):
        """
        This is the environment implementation of
        :attr:`BaseFeatures.text`. **value** will be
        a :ref:`type-string`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

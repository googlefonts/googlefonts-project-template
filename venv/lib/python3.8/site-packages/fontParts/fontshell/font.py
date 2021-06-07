import defcon
import os
from fontParts.base import BaseFont
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.info import RInfo
from fontParts.fontshell.groups import RGroups
from fontParts.fontshell.kerning import RKerning
from fontParts.fontshell.features import RFeatures
from fontParts.fontshell.lib import RLib
from fontParts.fontshell.layer import RLayer
from fontParts.fontshell.guideline import RGuideline


class RFont(RBaseObject, BaseFont):

    wrapClass = defcon.Font
    infoClass = RInfo
    groupsClass = RGroups
    kerningClass = RKerning
    featuresClass = RFeatures
    libClass = RLib
    layerClass = RLayer
    guidelineClass = RGuideline

    # ---------------
    # File Operations
    # ---------------

    # Initialize

    def _init(self, pathOrObject=None, showInterface=True, **kwargs):
        if pathOrObject is None:
            font = self.wrapClass()
        elif isinstance(pathOrObject, str):
            font = self.wrapClass(pathOrObject)
        elif hasattr(pathOrObject, "__fspath__"):
            font = self.wrapClass(os.fspath(pathOrObject))
        else:
            font = pathOrObject
        self._wrapped = font

    # path

    def _get_path(self, **kwargs):
        return self.naked().path

    # save

    def _save(self, path=None, showProgress=False,
              formatVersion=None, fileStructure=None, **kwargs):
        self.naked().save(path=path, formatVersion=formatVersion, structure=fileStructure)

    # close

    def _close(self, **kwargs):
        del self._wrapped

    # -----------
    # Sub-Objects
    # -----------

    # info

    def _get_info(self):
        return self.infoClass(wrap=self.naked().info)

    # groups

    def _get_groups(self):
        return self.groupsClass(wrap=self.naked().groups)

    # kerning

    def _get_kerning(self):
        return self.kerningClass(wrap=self.naked().kerning)

    # features

    def _get_features(self):
        return self.featuresClass(wrap=self.naked().features)

    # lib

    def _get_lib(self):
        return self.libClass(wrap=self.naked().lib)

    # ------
    # Layers
    # ------

    def _get_layers(self, **kwargs):
        return [self.layerClass(wrap=layer) for layer in self.naked().layers]

    # order

    def _get_layerOrder(self, **kwargs):
        return self.naked().layers.layerOrder

    def _set_layerOrder(self, value, **kwargs):
        self.naked().layers.layerOrder = value

    # default layer

    def _get_defaultLayerName(self):
        return self.naked().layers.defaultLayer.name

    def _set_defaultLayerName(self, value, **kwargs):
        for layer in self.layers:
            if layer.name == value:
                break
        layer = layer.naked()
        self.naked().layers.defaultLayer = layer

    # new

    def _newLayer(self, name, color, **kwargs):
        layers = self.naked().layers
        layer = layers.newLayer(name)
        layer.color = color
        return self.layerClass(wrap=layer)

    # remove

    def _removeLayer(self, name, **kwargs):
        layers = self.naked().layers
        del layers[name]

    # ------
    # Glyphs
    # ------

    def _get_glyphOrder(self):
        return self.naked().glyphOrder

    def _set_glyphOrder(self, value):
        self.naked().glyphOrder = value

    # ----------
    # Guidelines
    # ----------

    def _lenGuidelines(self, **kwargs):
        return len(self.naked().guidelines)

    def _getGuideline(self, index, **kwargs):
        guideline = self.naked().guidelines[index]
        return self.guidelineClass(guideline)

    def _appendGuideline(self, position, angle, name=None, color=None, identifier=None, **kwargs):
        guideline = self.guidelineClass().naked()
        guideline.x = position[0]
        guideline.y = position[1]
        guideline.angle = angle
        guideline.name = name
        guideline.color = color
        guideline.identifier = identifier
        self.naked().appendGuideline(guideline)
        return self.guidelineClass(guideline)

    def _removeGuideline(self, index, **kwargs):
        guideline = self.naked().guidelines[index]
        self.naked().removeGuideline(guideline)

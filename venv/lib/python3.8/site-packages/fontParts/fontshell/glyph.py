import defcon
import booleanOperations
from fontParts.base import BaseGlyph
from fontParts.base.errors import FontPartsError
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.contour import RContour
from fontParts.fontshell.component import RComponent
from fontParts.fontshell.anchor import RAnchor
from fontParts.fontshell.guideline import RGuideline
from fontParts.fontshell.image import RImage
from fontParts.fontshell.lib import RLib
from fontTools.ufoLib.glifLib import (GlifLibError, readGlyphFromString,
                                      writeGlyphToString)


class RGlyph(RBaseObject, BaseGlyph):

    wrapClass = defcon.Glyph
    contourClass = RContour
    componentClass = RComponent
    anchorClass = RAnchor
    guidelineClass = RGuideline
    imageClass = RImage
    libClass = RLib

    # --------------
    # Identification
    # --------------

    # Name

    def _get_name(self):
        return self.naked().name

    def _set_name(self, value):
        self.naked().name = value

    # Unicodes

    def _get_unicodes(self):
        return self.naked().unicodes

    def _set_unicodes(self, value):
        self.naked().unicodes = value

    # -------
    # Metrics
    # -------

    # horizontal

    def _get_width(self):
        return self.naked().width

    def _set_width(self, value):
        self.naked().width = value

    def _get_leftMargin(self):
        return self.naked().leftMargin

    def _set_leftMargin(self, value):
        naked = self.naked()
        naked.leftMargin = value

    def _get_rightMargin(self):
        return self.naked().rightMargin

    def _set_rightMargin(self, value):
        naked = self.naked()
        naked.rightMargin = value

    # vertical

    def _get_height(self):
        return self.naked().height

    def _set_height(self, value):
        self.naked().height = value

    def _get_bottomMargin(self):
        return self.naked().bottomMargin

    def _set_bottomMargin(self, value):
        naked = self.naked()
        naked.bottomMargin = value

    def _get_topMargin(self):
        return self.naked().topMargin

    def _set_topMargin(self, value):
        naked = self.naked()
        naked.topMargin = value

    # ------
    # Bounds
    # ------

    def _get_bounds(self):
        return self.naked().bounds

    # ----
    # Area
    # ----

    def _get_area(self):
        return self.naked().area

    # ----
    # Pens
    # ----

    def getPen(self):
        return self.naked().getPen()

    def getPointPen(self):
        return self.naked().getPointPen()

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    # Contours

    def _lenContours(self, **kwargs):
        return len(self.naked())

    def _getContour(self, index, **kwargs):
        glyph = self.naked()
        contour = glyph[index]
        return self.contourClass(contour)

    def _removeContour(self, index, **kwargs):
        glyph = self.naked()
        contour = glyph[index]
        glyph.removeContour(contour)

    def _removeOverlap(self, **kwargs):
        if len(self):
            contours = list(self)
            for contour in contours:
                for point in contour.points:
                    if point.type == "qcurve":
                        raise TypeError("fontshell can't removeOverlap for quadratics")
            self.clear(contours=True, components=False,
                       anchors=False, guidelines=False, image=False)
            booleanOperations.union(contours, self.getPointPen())

    def _correctDirection(self, trueType=False, **kwargs):
        self.naked().correctContourDirection(trueType=trueType)

    # Components

    def _lenComponents(self, **kwargs):
        return len(self.naked().components)

    def _getComponent(self, index, **kwargs):
        glyph = self.naked()
        component = glyph.components[index]
        return self.componentClass(component)

    def _removeComponent(self, index, **kwargs):
        glyph = self.naked()
        component = glyph.components[index]
        glyph.removeComponent(component)

    # Anchors

    def _lenAnchors(self, **kwargs):
        return len(self.naked().anchors)

    def _getAnchor(self, index, **kwargs):
        glyph = self.naked()
        anchor = glyph.anchors[index]
        return self.anchorClass(anchor)

    def _appendAnchor(self, name, position=None, color=None, identifier=None, **kwargs):
        glyph = self.naked()
        anchor = self.anchorClass().naked()
        anchor.name = name
        anchor.x = position[0]
        anchor.y = position[1]
        anchor.color = color
        anchor.identifier = identifier
        glyph.appendAnchor(anchor)
        wrapped = self.anchorClass(anchor)
        wrapped.glyph = self
        return wrapped

    def _removeAnchor(self, index, **kwargs):
        glyph = self.naked()
        anchor = glyph.anchors[index]
        glyph.removeAnchor(anchor)

    # Guidelines

    def _lenGuidelines(self, **kwargs):
        return len(self.naked().guidelines)

    def _getGuideline(self, index, **kwargs):
        glyph = self.naked()
        guideline = glyph.guidelines[index]
        return self.guidelineClass(guideline)

    def _appendGuideline(self, position, angle, name=None, color=None, identifier=None, **kwargs):
        glyph = self.naked()
        guideline = self.guidelineClass().naked()
        guideline.x = position[0]
        guideline.y = position[1]
        guideline.angle = angle
        guideline.name = name
        guideline.color = color
        guideline.identifier = identifier
        glyph.appendGuideline(guideline)
        return self.guidelineClass(guideline)

    def _removeGuideline(self, index, **kwargs):
        glyph = self.naked()
        guideline = glyph.guidelines[index]
        glyph.removeGuideline(guideline)

    # -----------------
    # Layer Interaction
    # -----------------

    # new

    def _newLayer(self, name, **kwargs):
        layerName = name
        glyphName = self.name
        font = self.font
        if layerName not in font.layerOrder:
            layer = font.newLayer(layerName)
        else:
            layer = font.getLayer(layerName)
        glyph = layer.newGlyph(glyphName)
        return glyph

    # remove

    def _removeLayer(self, name, **kwargs):
        layerName = name
        glyphName = self.name
        font = self.font
        layer = font.getLayer(layerName)
        layer.removeGlyph(glyphName)

    # -----
    # Image
    # -----

    def _get_image(self):
        image = self.naked().image
        if image is None:
            return None
        return self.imageClass(image)

    def _addImage(self, data, transformation=None, color=None):
        image = self.naked().image
        image = self.imageClass(image)
        image.glyph = self
        image.data = data
        image.transformation = transformation
        image.color = color

    def _clearImage(self, **kwargs):
        self.naked().image = None

    # ----
    # Note
    # ----

    # Mark

    def _get_markColor(self):
        value = self.naked().markColor
        if value is not None:
            value = tuple(value)
        return value

    def _set_markColor(self, value):
        self.naked().markColor = value

    # Note

    def _get_note(self):
        return self.naked().note

    def _set_note(self, value):
        self.naked().note = value

    # -----------
    # Sub-Objects
    # -----------

    # lib

    def _get_lib(self):
        return self.libClass(wrap=self.naked().lib)

    # ---
    # API
    # ---

    def _loadFromGLIF(self, glifData):
        try:
            readGlyphFromString(
                aString=glifData,
                glyphObject=self.naked(),
                pointPen=self.getPointPen()
            )
        except GlifLibError:
            raise FontPartsError("Not valid glif data")

    def _dumpToGLIF(self, glyphFormatVersion):
        glyph = self.naked()
        return writeGlyphToString(
            glyphName=glyph.name,
            glyphObject=glyph,
            drawPointsFunc=glyph.drawPoints,
            formatVersion=glyphFormatVersion
        )

from fontParts.test import testEnvironment
from fontParts.fontshell.font import RFont
from fontParts.fontshell.info import RInfo
from fontParts.fontshell.groups import RGroups
from fontParts.fontshell.kerning import RKerning
from fontParts.fontshell.features import RFeatures
from fontParts.fontshell.layer import RLayer
from fontParts.fontshell.glyph import RGlyph
from fontParts.fontshell.contour import RContour
from fontParts.fontshell.segment import RSegment
from fontParts.fontshell.bPoint import RBPoint
from fontParts.fontshell.point import RPoint
from fontParts.fontshell.anchor import RAnchor
from fontParts.fontshell.component import RComponent
from fontParts.fontshell.image import RImage
from fontParts.fontshell.lib import RLib
from fontParts.fontshell.guideline import RGuideline


# defcon does not have prebuilt support for
# selection states, so we simulate selection
# behavior with a small subclasses for testing
# purposes only.

def _get_selected(self):
    if isinstance(self, FSTestSegment):
        for point in self.points:
            if point.selected:
                return True
        return False
    elif isinstance(self, FSTestBPoint):
        point = self._point.naked()
        return point.name == "selected"
    elif isinstance(self, FSTestPoint):
        return self.name == "selected"
    else:
        if not hasattr(self.naked(), "_testSelected"):
            return False
        return self.naked()._testSelected


def _set_selected(self, value):
    if isinstance(self, FSTestSegment):
        for point in self.points:
            point.selected = value
    elif isinstance(self, FSTestBPoint):
        point = self._point.naked()
        if value:
            point.name = "selected"
        else:
            point.name = None
    elif isinstance(self, FSTestPoint):
        if value:
            self.name = "selected"
        else:
            self.name = None
    else:
        self.naked()._testSelected = value


class FSTestPoint(RPoint):

    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestBPoint(RBPoint):

    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestSegment(RSegment):

    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestGuideline(RGuideline):

    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestImage(RImage):

    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestAnchor(RAnchor):

    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestComponent(RComponent):

    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestContour(RContour):

    segmentClass = FSTestSegment
    bPointClass = FSTestBPoint
    pointClass = FSTestPoint
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestGlyph(RGlyph):

    contourClass = FSTestContour
    componentClass = FSTestComponent
    anchorClass = FSTestAnchor
    guidelineClass = FSTestGuideline
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestLayer(RLayer):

    glyphClass = FSTestGlyph
    _get_selected = _get_selected
    _set_selected = _set_selected


class FSTestFont(RFont):

    layerClass = FSTestLayer
    guidelineClass = FSTestGuideline
    _get_selected = _get_selected
    _set_selected = _set_selected


classMapping = dict(
    font=FSTestFont,
    info=RInfo,
    groups=RGroups,
    kerning=RKerning,
    features=RFeatures,
    layer=FSTestLayer,
    glyph=FSTestGlyph,
    contour=FSTestContour,
    segment=FSTestSegment,
    bPoint=FSTestBPoint,
    point=FSTestPoint,
    anchor=FSTestAnchor,
    component=FSTestComponent,
    image=FSTestImage,
    lib=RLib,
    guideline=FSTestGuideline,
)


def fontshellObjectGenerator(cls):
    unrequested = []
    obj = classMapping[cls]()
    return obj, unrequested


if __name__ == "__main__":
    import sys
    if {"-v", "--verbose"}.intersection(sys.argv):
        verbosity = 2
    else:
        verbosity = 1
    testEnvironment(fontshellObjectGenerator, verbosity=verbosity)

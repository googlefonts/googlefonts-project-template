from datetime import datetime
from babelfont.font import Font
from babelfont.layer import Layer
from babelfont.lib import Lib
from babelfont.glyph import Glyph
from babelfont.point import Point
from babelfont.contour import Contour
from babelfont.component import Component
from babelfont.anchor import Anchor
import json
from babelfont.utils import _toFlagBits


def can_load(filename):
    return filename.endswith(".vfj")

def can_save(filename):
    return None

def load(filename, **kwargs):
    vfj = json.load(open(filename, "r"))["font"]
    if "master" not in kwargs or not kwargs["master"]:
        wanted = vfj["defaultMaster"]
    else:
        wanted = kwargs["master"]
    master = None
    for m in vfj["masters"]:
        if m["fontMaster"]["name"] == wanted:
            master = m
            break
        if not master:
            raise ValueError(f"Master {wanted} not found in {filename}")
    return _load_vfj(vfj, master["fontMaster"])


def save(font, filename):
    gsfont = _save_gsfont(font)
    gsfont.save(filename)


# vfj -> babelfont


def _load_vfj(vfj, master):
    bbf = Font()

    bbf.info.familyName = vfj["info"]["tfn"]
    # sgn?
    bbf.info.styleName = master["name"]
    bbf.info.copyright = vfj["info"]["copyright"]
    bbf.info.trademark = vfj["info"]["trademark"]

    bbf.lib.glyphOrder = [x["name"] for x in vfj["glyphs"]]
    bbf.lib["com.fontlab.appVersion"] = vfj["meta"]["metaFormatVersion"]
    bbf.lib["com.fontlab.appBuild"] = vfj["meta"]["metaBuild"]

    bbf.info.openTypeHeadCreated = vfj["info"]["creationDate"]
    bbf.info.openTypeNameDesigner = vfj["info"]["designer"]
    bbf.info.openTypeNameDesignerURL = vfj["info"]["designerURL"]
    bbf.info.openTypeNameManufacturer = vfj["info"]["manufacturer"]
    bbf.info.openTypeNameManufacturerURL = vfj["info"]["manufacturerURL"]
    bbf.info.versionMajor = vfj["info"]["versionMajor"]
    bbf.info.versionMinor = vfj["info"]["versionMinor"]
    bbf.info.year = vfj["info"]["year"]
    bbf.info.openTypeNameVersion = vfj["info"]["version"]

    bbf.info.openTypeOS2UnicodeRanges = _toFlagBits(
        int(vfj["info"]["unicodeRange"], 16)
    )
    bbf.info.openTypeOS2CodePageRanges = _toFlagBits(
        int(vfj["info"]["codepageRange"], 16)
    )
    if vfj["info"]["useTypoMetrics"]:
        bbf.info.openTypeOS2Selection = [7]
    bbf.info.openTypeOS2Type = _toFlagBits(int(vfj["info"]["embedding"], 16))

    bbf.info.unitsPerEm = vfj["upm"]

    _load_groups(bbf.groups, vfj["classes"])

    # XXX Add groups here
    bbf.features.text = "\n".join([f["feature"] for f in vfj["openTypeFeatures"]])

    # Only support one layer for now
    layer = Layer()
    layer._name = master["name"]

    bbf.info.ascender = master["ascender"]
    bbf.info.capHeight = master["capsHeight"]
    bbf.info.descender = master["descender"]
    bbf.info.xHeight = master["xHeight"]

    bbf.info.postscriptFontName = master["psn"]

    # measurement, safeTop, safeBottom?
    bbf.info.openTypeOS2WeightClass = master["weight"]
    bbf.info.openTypeOS2WidthClass = master["width"]
    bbf.info.openTypeOS2TypoLineGap = master["lineGap"]
    bbf.info.postscriptUnderlineThickness = master["underlineThickness"]
    bbf.info.postscriptUnderlinePosition = master["underlinePosition"]
    bbf.info.panose = [int(i) for i in master["panose"].split()]
    # guidelines, mask?,
    bbf.info.openTypeHheaAscender = master["otherData"]["hhea_ascender"]
    bbf.info.openTypeHheaDescender = master["otherData"]["hhea_descender"]
    bbf.info.openTypeHheaLineGap = master["otherData"]["hhea_line_gap"]
    bbf.info.openTypeOS2StrikeoutSize = master["otherData"]["strikeout_size"]
    bbf.info.openTypeOS2StrikeoutPosition = master["otherData"]["strikeout_position"]
    # XXX superscripts, subscriptsmas

    bbf._layers.append(layer)
    bbf._layerOrder.append(master["name"])

    for g in vfj["glyphs"]:
        layer._glyphs[g["name"]] = _load_glyph(g, layer, master)

    # if master.kerning:
    #     _load_kerning(bbf.kerning, master)
    return bbf


def _load_glyph(g, layer, master):  # -> Glyph
    glyph = Glyph()
    glyph._layer = layer
    glyph._name = g["name"]
    glayer = None

    for l in g["layers"]:
        if l["name"] == master["name"]:
            glayer = l
    if not glayer:
        raise ValueError

    if "unicode" in g:
        glyph._unicodes = [int(g["unicode"], 16)]
    else:
        glyph._unicodes = []
    glyph._width = glayer["advanceWidth"]
    glyph._height = master["ascender"] - master["descender"]  # ?
    glyph._lib = Lib()
    glyph._lib.glyph = glyph

    if hasattr(g, "openTypeGlyphClass"):
        if g.openTypeGlyphClass == 1:
            glyph._lib["public.openTypeCategory"] = "base"
        if g.openTypeGlyphClass == 2:
            glyph._lib["public.openTypeCategory"] = "ligature"
        if g.openTypeGlyphClass == 3:
            glyph._lib["public.openTypeCategory"] = "mark"

    glyph._contours = []
    glyph._components = []
    if "elements" in glayer:
        for element in glayer["elements"]:
            if "component" in element:
                glyph._components.append(_load_component(element, glyph))
            else:
                for c in element["elementData"]["contours"]:
                    glyph._contours.append(_load_contour(glyph, c["nodes"]))
    # Guidelines

    return glyph


def _load_contour(glyph, segments):
    contour = Contour()
    contour._glyph = glyph
    contour._points = []

    for s in segments:
        if s[-1] == "x":  # sx?
            s = s[:-3]

        if s[-1] == "s":
            smooth = True
            s = s[:-2]
        else:
            smooth = False
        if s[-1] == "c":  # Close
            s = s[:-2]
        points = s.split("  ")
        for ix, position in enumerate(points):
            p = Point()
            p._contour = contour
            p.x, p.y = [float(pos) for pos in position.split(" ")]
            if len(points) == 1:
                p.type = "line"
            elif ix == 2:
                p.type = "curve"
            else:
                p.type = "offcurve"
            if ix == len(points) - 1 and smooth:
                p.smooth = True
            else:
                p.smooth = False
            contour._points.append(p)
        if len(contour._points) and contour._points[-1].type == "offcurve":
            contour._points[0].type = "curve"

    contour._correct_direction()
    return contour


def _load_component(c, glyph):
    component = Component()
    component._glyph = glyph
    component._baseGlyph = c["component"]["glyphName"]
    if "transform" in c:
        component._transformation = tuple(
            (
                1,
                0,
                0,
                1,
                c["transform"].get("xOffset", 0),
                c["transform"].get("yOffset", 0),
            )
        )
    return component


def _load_gsanchor(gsanchor, glyph):
    anchor = Anchor()
    anchor._glyph = glyph
    anchor.x = gsanchor.position.x
    anchor.y = gsanchor.position.y
    anchor.name = gsanchor.name
    return anchor


def _load_groups(groups, classes):
    for c in classes:
        groups[c["name"]] = c["names"]


# def _load_kerning(kerning, gskerning):
#     for left in gskerning.keys():
#         assert left[0] != "@"
#         for right, value in gskerning[left].items():
#             assert right[0] != "@"
#             kerning[(left,right)] = value

# babelfont -> json

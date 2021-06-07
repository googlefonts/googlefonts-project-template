from fontTools.ttLib import TTFont
from babelfont.font import Font
from babelfont.layer import Layer
from babelfont.lib import Lib
from babelfont.glyph import Glyph
from babelfont.point import Point
from babelfont.contour import Contour
from babelfont.component import Component
from babelfont.anchor import Anchor
from copy import copy
from babelfont.convertors.ttf import _load_name_table, _load_other_info, _load_ttanchors, _load_ttcategory, _load_features
from fontTools.pens.recordingPen import RecordingPen


def can_load(filename):
    if not (filename.endswith(".otf") or filename.endswith(".ttf")):
      return False
    font = TTFont(filename)
    return "CFF " in font

def can_save(filename):
    return filename.endswith(".otf")

def load(filename, **kwargs):
    return _load_ttfont(TTFont(filename))

def save(font, filename):
    ttfont = _save_ttfont(font)
    ttfont.save(filename)

def _load_ttfont(ttfont):
    bbf = Font()
    _load_name_table(bbf, ttfont["name"])
    _load_other_info(bbf, ttfont)
    bbf._unicodemap = {}
    bbf._reversedunicodemap = {}
    bbf.lib.glyphOrder = ttfont.getGlyphOrder()
    # Make a layer
    layer = bbf.newLayer("public.default")
    cmap = ttfont["cmap"].buildReversed()
    for glyph in ttfont.getGlyphOrder():
        if glyph in cmap:
            cps = list(cmap[glyph])
            bbf._reversedunicodemap[glyph] = cps[0]
            for cp in cps:
                bbf._unicodemap[cp] = glyph
        layer._glyphs[glyph] = None
        layer._promised_glyphs[
            glyph
        ] = lambda glyph=glyph, ttfont=ttfont, cmap=cmap: _load_otglyph(
            glyph, ttfont, cmap
        )
    bbf._unicodemap[0] = ttfont.getGlyphOrder()[0]

    ff = _load_features(bbf, ttfont)
    _load_ttanchors(bbf, ttfont, ff)
    return bbf

def _load_otglyph(g, ttfont, cmap):
    glyph = Glyph()
    glyph._name = g

    if g in cmap:
        glyph._unicodes = list(cmap[g])
    else:
        glyph._unicodes = []
    glyph._contours = []

    _load_ttcategory(glyph, ttfont, g)

    ttglyph = ttfont.getGlyphSet()[g]
    pen = RecordingPen()
    ttglyph.draw(pen)
    contours = pen.value
    lastcontour = []
    startPt = (0,0)
    lastPt = (0,0)
    index = 0
    for c in contours:
        if c[0] == "moveTo":
            startPt = c[1][0]
        elif c[0] == "closePath":
            if startPt != lastPt:
                lastcontour.append(_load_point(startPt,segmentType = "line"))
            contour = Contour()
            contour._points = lastcontour
            contour._correct_direction()
            glyph._contours.append(contour)
            lastcontour = []
        elif c[0] == "curveTo":
            lastcontour.append(_load_point(c[1][0],segmentType = "offcurve"))
            lastcontour.append(_load_point(c[1][1],segmentType = "offcurve"))
            lastcontour.append(_load_point(c[1][2],segmentType = "curve"))
            lastPt = c[1][2]
        elif c[0] == "lineTo":
            lastcontour.append(_load_point(c[1][0],segmentType = "line"))
            lastPt = c[1][0]
        elif c[0] == "qCurveTo":
            self.raiseNotImplementedError()

    glyph._width       = ttfont["hmtx"][g][0]
    glyph._leftMargin  = ttfont["hmtx"][g][1]
    glyph._height      = ttfont["hhea"].ascent
    if glyph.bounds:
        glyph._rightMargin = glyph._width - glyph.bounds[2]

    # CFF glyphs do not have components as such

    return glyph

def _load_point(xy, segmentType):
    p = Point()
    p.x, p.y = xy
    p.type = segmentType
    p.smooth = False # for testing
    return p


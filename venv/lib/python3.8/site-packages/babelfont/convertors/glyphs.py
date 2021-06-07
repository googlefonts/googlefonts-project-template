import glyphsLib
from datetime import datetime
from babelfont.font import Font
from babelfont.layer import Layer
from babelfont.lib import Lib
from babelfont.glyph import Glyph
from babelfont.point import Point
from babelfont.contour import Contour
from babelfont.component import Component
from babelfont.anchor import Anchor
from glyphsLib.types import Transform

def can_load(filename):
    return filename.endswith(".glyphs")

def can_save(filename):
    return filename.endswith(".glyphs")


def load(filename, **kwargs):
    gsfont = glyphsLib.GSFont(filename)
    gsmaster = None
    if "master" not in kwargs or not kwargs["master"]:
        gsmaster = gsfont.masters[0]
    else:
        wanted = kwargs["master"]
        for m in gsfont.masters:
            if m.name == wanted:
                gsmaster = m
                break
        if not gsmaster:
            raise ValueError(f"Master {wanted} not found in {filename}")
    return _load_gsfont(gsmaster)

def save(font, filename):
    gsfont = _save_gsfont(font)
    gsfont.save(filename)

# glyphsLib -> babelfont


def _load_gsfont(gsfontmaster):
    bbf = Font(gsfontmaster)

    # XXX Create: features

    bbf.info.familyName = gsfontmaster.font.familyName
    bbf.info.styleName = gsfontmaster.name
    bbf.lib.glyphOrder = [x.name for x in gsfontmaster.font.glyphs]
    bbf.lib["com.schriftgestaltung.appVersion"] = gsfontmaster.font.appVersion
    bbf.lib["com.schriftgestaltung.DisplayStrings"] = gsfontmaster.font.DisplayStrings
    bbf.lib["com.schriftgestaltung.fontMasterID"] = gsfontmaster.id

    bbf.info.openTypeHeadCreated = _glyphs_date_to_ufo(gsfontmaster.font.date)
    bbf.info.unitsPerEm = gsfontmaster.font.upm
    bbf.info.copyright = gsfontmaster.font.copyright
    bbf.info.versionMajor = gsfontmaster.font.versionMajor
    bbf.info.versionMinor = gsfontmaster.font.versionMinor
    bbf.info.openTypeNameDesigner = gsfontmaster.font.designer
    bbf.info.openTypeNameDesignerURL = gsfontmaster.font.designerURL
    bbf.info.openTypeNameManufacturer = gsfontmaster.font.manufacturer
    bbf.info.openTypeNameManufacturerURL = gsfontmaster.font.manufacturerURL
    _load_groups(bbf.groups, gsfontmaster.font.classes)


    # Only support one layer for now
    layer = Layer()
    layer._name = gsfontmaster.name

    bbf.info.ascender = gsfontmaster.ascender
    bbf.info.capHeight = gsfontmaster.capHeight
    bbf.info.descender = gsfontmaster.descender
    bbf.info.xHeight = gsfontmaster.xHeight

    bbf._layers.append(layer)
    bbf._layerOrder.append(gsfontmaster.name)

    for g in gsfontmaster.font.glyphs:
        layer._glyphs[g.name] = _load_gslayer(g.layers[gsfontmaster.id], layer)
        if g.leftKerningGroup:
            groupname = "public.kern1."+g.leftKerningGroup
            if not groupname in bbf.groups:
                bbf.groups[groupname] = []
            bbf.groups[groupname] = [*bbf.groups[groupname], g.name]
        if g.rightKerningGroup:
            groupname = "public.kern2."+g.rightKerningGroup
            if not groupname in bbf.groups:
                bbf.groups[groupname] = []
            bbf.groups[groupname] = [*bbf.groups[groupname], g.name]


    for g in gsfontmaster.font.glyphs:
        _finalise_glyph(g.layers[gsfontmaster.id], layer._glyphs[g.name])

    if gsfontmaster.id in gsfontmaster.font.kerning:
        _load_kerning(bbf.kerning, gsfontmaster.font.kerning[gsfontmaster.id], gsfontmaster.font)
    return bbf


def _load_gslayer(gslayer, layer):  # -> Glyph
    glyph = Glyph()
    glyph._layer = layer
    glyph._name = gslayer.parent.name
    if gslayer.parent.unicode:
        glyph._unicodes = [int(gslayer.parent.unicode,16)]
    else:
        glyph._unicodes = []
    glyph._width = gslayer.width
    glyph._height = gslayer.master.ascender - gslayer.master.descender  # ?
    glyph.exported = gslayer.parent.export
    glyph._lib = Lib()
    glyph._lib.glyph = glyph
    if gslayer.parent.lastChange:
        glyph._lib["com.schriftgestaltung.lastChange"] = gslayer.parent.lastChange

    c = gslayer.parent.category
    sc = gslayer.parent.subCategory
    if c:
        glyph._lib["com.schriftgestaltung.Glyphs.category"] = c
    if sc:
        glyph._lib["com.schriftgestaltung.Glyphs.subcategory"] = sc
    if sc == "Ligature":
        glyph._lib["public.openTypeCategory"] = "ligature"
    if c == "Mark":
        glyph._lib["public.openTypeCategory"] = "mark"
    else:
        glyph._lib["public.openTypeCategory"] = "base"
    glyph._contours = [_load_gspath(p, glyph) for p in gslayer.paths]
    glyph._anchors = [_load_gsanchor(a, glyph) for a in gslayer.anchors]
    return glyph

# Have to load components after all glyphs are processed
def _finalise_glyph(gslayer, glyph):
    # XXX guidelines, image
    glyph._components = [_load_gscomponent(c, glyph) for c in gslayer.components]
    return glyph

def _load_gspath(gspath, glyph):
    contour = Contour()
    contour._glyph = glyph
    contour._points = [_load_gspoint(p, contour) for p in gspath.nodes]
    contour._clockwise = gspath.direction == 1
    return contour


def _load_gscomponent(gscomponent, glyph):
    component = Component()
    component._glyph = glyph
    component._baseGlyph = gscomponent.componentName
    component._transformation = tuple(gscomponent.transform.value)
    return component


def _load_gsanchor(gsanchor, glyph):
    anchor = Anchor()
    anchor._glyph = glyph
    anchor.x = gsanchor.position.x
    anchor.y = gsanchor.position.y
    anchor.name = gsanchor.name
    return anchor


def _load_gspoint(gspoint, contour):
    point = Point()
    point._contour = contour
    point._x = gspoint.position.x
    point._y = gspoint.position.y
    point.type = gspoint.type
    point.smooth = gspoint.smooth
    return point


def _load_groups(groups, classes):
    for c in classes:
        groups[c.name] = c.code.split() # Urgh

def _load_kerning(kerning, gskerning, gsfont):
    for left in gskerning.keys():
        if "@" in left:
            ufoleft = "public.kern1."+left[7:]
        else:
            ufoleft = left
        for right, value in gskerning[left].items():
            if "@" in right:
                right = "public.kern2."+right[7:]
            kerning[(ufoleft,right)] = value

# babelfont -> glyphsLib


def _save_point(point):
    p = glyphsLib.GSNode ((point.x, point.y), point.type)
    p.smooth = point.smooth
    return p


def _save_contour(contour):
    path = glyphsLib.GSPath()
    path.nodes = [_save_point(p) for p in contour._points]
    # Check node order
    # XXX closed
    return path

def _save_anchor(anchor):
    gsanchor = glyphsLib.GSAnchor()
    gsanchor.position.x = anchor.x
    gsanchor.position.y = anchor.y
    gsanchor.name = anchor.name
    return gsanchor

def _save_component(component):
    c = glyphsLib.GSComponent(component.baseGlyph)
    if component.transformation != (1,0,0,1,0,0):
        c.transform = Transform(*component.transformation)
    return c

def _save_glyph(glyph, gsfont, bbf):
    # This needs to go into a layer and a glyph
    masterId = gsfont.masters[0].id
    gslayer = glyphsLib.GSLayer()
    gsglyph = glyphsLib.GSGlyph()
    gslayer.layerId = masterId
    gsglyph.layers.append(gslayer)
    if glyph._unicodes:
        gsglyph.unicode = "%04x" % glyph._unicodes[0]
    if "com.schriftgestaltung.lastChange" in glyph.lib:
        gsglyph.lastChange = glyph.lib["com.schriftgestaltung.lastChange"]
    if "com.schriftgestaltung.Glyphs.category" in glyph.lib:
        gsglyph.category = glyph._lib["com.schriftgestaltung.Glyphs.category"]
    if "com.schriftgestaltung.Glyphs.subcategory" in glyph.lib:
        gsglyph.subCategory = glyph._lib["com.schriftgestaltung.Glyphs.subcategory"]

    gslayer.paths = [_save_contour(c) for c in glyph.contours]
    gslayer.components = [_save_component(c) for c in glyph.components]
    gslayer.anchors = [_save_anchor(a) for a in glyph.anchors]
    gslayer.name = glyph.name
    gslayer.RSB = glyph.rightMargin
    gslayer.LSB = glyph.leftMargin
    gslayer.width = glyph.width
    # Attach to master ID
    gsglyph.name = glyph.name
    gsfont.glyphs.append(gsglyph)
    # Set kerning groups
    for name, contents in bbf.groups.items():
        if not "public.kern" in name: continue
        if glyph.name in contents:
            if "public.kern1" in name:
                gsglyph.leftKerningGroup = name[13:]
            else:
                gsglyph.rightKerningGroup = name[13:]

def _save_gsfont(font):
    f = glyphsLib.GSFont()
    f.familyName = font.info.familyName
    if "com.schriftgestaltung.appVersion" in font.lib:
        f.appVersion = font.lib["com.schriftgestaltung.appVersion"]
    if "com.schriftgestaltung.DisplayStrings" in font.lib:
        f.DisplayStrings = font.lib["com.schriftgestaltung.DisplayStrings"]
    if font.info.openTypeHeadCreated:
        f.date = _ufo_date_to_glyphs(font.info.openTypeHeadCreated)
    f.upm = font.info.unitsPerEm
    fontmaster = glyphsLib.GSFontMaster()
    if "com.schriftgestaltung.fontMasterID" in font.lib:
        fontmaster.id = font.lib["com.schriftgestaltung.fontMasterID"]

    f.masters = [fontmaster]
    # f.instances = [glyphsLib.GSInstance()]
    # f.instances[0].instanceInterpolations = {}
    fontmaster.ascender = font.info.ascender
    fontmaster.xHeight = font.info.xHeight
    fontmaster.capHeight = font.info.capHeight
    fontmaster.descender = font.info.descender
    for glyph in font.defaultLayer:
        _save_glyph(glyph, f, bbf=font)
    for g in font.groups:
        if "public.kern" in g:
            continue
        f.classes.append(glyphsLib.GSClass(g, " ".join(font.groups[g])))
    _save_kerning(font.kerning, f, fontmaster.id)
    return f

def _save_kerning(kerning, font, mid):
    for (l,r), value in kerning.items():
        if "public.kern1" in l:
            l = "@MMK_L_"+l[13:]
        if "public.kern2" in r:
            r = "@MMK_R_"+r[13:]

        font.setKerningForPair(mid,l,r,value)

# Random stuff

def _glyphs_date_to_ufo(d):
    if d:
        return d.strftime('%Y/%m/%d %H:%M:%S')
    return None

def _ufo_date_to_glyphs(d):
    return datetime.strptime(d, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S +0000')

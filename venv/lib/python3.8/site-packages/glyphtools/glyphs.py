from beziers.path import BezierPath


def isglyphs(fontmaster):
    return hasattr(fontmaster, "userData")


def categorize_glyph(fontmaster, glyphname):
    c = fontmaster.font.glyphs[glyphname].category
    sc = fontmaster.font.glyphs[glyphname].subCategory
    if sc == "Ligature":
        return ("ligature", None)
    if c == "Mark":
        return ("mark", None)
    return ("base", None)


def set_glyph_category(fontmaster, glyphname, category):
    glyph = fontmaster.font.glyphs[glyphname]
    if category == "ligature":
        glyph.storeSubCategory = True
        glyph.subCategory = "Ligature"
    elif category == "mark":
        glyph.storeCategory = True
        glyph.category = "Mark"
    else:
        glyph.storeCategory = True
        glyph.category = "Letter"


def get_glyph_metrics(fontmaster, glyphname):
    glyph = fontmaster.font.glyphs[glyphname]
    layer = glyph.layers[fontmaster.id]
    metrics = {"width": layer.width}
    # If it's a nonspacing mark then its advance width is really zero
    if glyph.subCategory == "Nonspacing":
        metrics["width"] = 0

    bounds = layer.bounds
    if bounds:
        metrics["lsb"] = bounds.origin.x
        metrics["xMin"] = bounds.origin.x  # That doesn't look right
        metrics["yMin"] = bounds.origin.y
        metrics["xMax"] = bounds.origin.x + bounds.size.width
        metrics["yMax"] = bounds.origin.y + bounds.size.height
    else:
        metrics["lsb"], metrics["xMin"], metrics["xMax"] = 0,0,0
        metrics["yMin"], metrics["yMax"] = 0,0
    metrics["rsb"] = metrics["width"] - metrics["xMax"]
    metrics["rise"] = get_rise(fontmaster, glyphname)
    metrics["run"] = get_run(fontmaster, glyphname)
    metrics["fullwidth"] = metrics["xMax"] - metrics["xMin"]
    return metrics


def get_rise(fontmaster, glyphname):
    # Don't import glyphsLib until we know we're dealing with a glyphs obj
    from glyphsLib import GSAnchor
    from glyphsLib.types import Point

    layer = fontmaster.font.glyphs[glyphname].layers[fontmaster.id]
    entry = layer.anchors["entry"] or GSAnchor("entry", Point(0, 0))
    exit = layer.anchors["exit"] or GSAnchor("exit", Point(0, 0))
    return entry.position.y - exit.position.y

def get_run(fontmaster, glyphname):
    from glyphsLib import GSAnchor
    from glyphsLib.types import Point
    layer = fontmaster.font.glyphs[glyphname].layers[fontmaster.id]
    entry = layer.anchors["entry"] or GSAnchor("entry", Point(layer.width, 0))
    exit = layer.anchors["exit"] or GSAnchor("exit", Point(0, 0))
    return entry.position.x - exit.position.x



def beziers(fontmaster, glyphname):
    layer = fontmaster.font.glyphs[glyphname].layers[fontmaster.id]
    return BezierPath.fromGlyphsLayer(layer)

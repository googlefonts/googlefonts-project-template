"""glyphtools is a set of routines for extracting information from font glyphs."""

import statistics
from .ckmeans import ckmeans
from beziers.path import BezierPath
from beziers.point import Point
import glyphtools.glyphs
import glyphtools.babelfont
import warnings
from beziers.path.representations.fontparts import FontParts


__author__ = """Simon Cozens"""
__email__ = "simon@simon-cozens.org"
__version__ = "__version__ = '0.7.1'"


def categorize_glyph(font, glyphname):
    """Return the category of the given glyph.

    Args:
        font: a ``fontTools`` TTFont object OR a ``glyphsLib`` GSFontMaster
            object OR a ``babelfont`` Font object.
        glyphname: name of the glyph.

    Returns:
        A two-element tuple. The first element is one of the following
        strings: ``unknown``, ``base``, ``mark``, ``ligature``, ``component``.
        If the glyph is a mark, the second element is the mark attachment
        class number.
    """
    if glyphtools.glyphs.isglyphs(font):
        return glyphtools.glyphs.categorize_glyph(font, glyphname)
    if glyphtools.babelfont.isbabelfont(font):
        return (font[glyphname].category, None)
    if "GDEF" not in font:
        return ("unknown", None)
    gdef = font["GDEF"].table
    classdefs = gdef.GlyphClassDef.classDefs
    if glyphname not in classdefs:
        return ("unknown", None)
    if classdefs[glyphname] == 1:
        return ("base", None)
    if classdefs[glyphname] == 2:
        return ("ligature", None)
    if classdefs[glyphname] == 3:
        # Now find attachment class
        mclass = None
        if gdef.MarkAttachClassDef:
            classdef = gdef.MarkAttachClassDef.classDefs
            if glyphname in classdef:
                mclass = classdef[glyphname]
        return ("mark", mclass)
    if classdefs[glyphname] == 4:
        return ("component", None)
    return ("unknown", None)


def set_glyph_category(font, glyphname, category, maClass=None):
    """Set the category of the glyph in the font.

    Args:
        font: a ``fontTools`` TTFont object or a ``glyphsLib`` GSFontMaster
              object OR a ``babelfont`` Font object.
        glyphname: name of the glyph.
        category: one of ``base``, ``mark``, ``ligature``, ``component``.
        maClass: If the category is ``base``, the mark attachment class number.
    """
    if glyphtools.glyphs.isglyphs(font):
        return glyphtools.glyphs.set_glyph_category(font, glyphname, category)
    if glyphtools.babelfont.isbabelfont(font):
        font[glyphname].category = category
        return

    gdef = font["GDEF"].table
    classdefs = gdef.GlyphClassDef.classDefs
    if category == "base":
        classdefs[glyphname] = 1
    elif category == "ligature":
        classdefs[glyphname] = 2
    elif category == "mark":
        classdefs[glyphname] = 3
        if maClass and gdef.MarkAttachClassDef:
            gdef.MarkAttachClassDef.classDefs[glyphname] = maClass
    elif category == "component":
        classdefs[glyphname] = 4
    else:
        raise ValueError("Unknown category")


def get_glyph_metrics(font, glyphname, **kwargs):
    """Return glyph metrics as a dictionary.

    Args:
        font: a ``fontTools`` TTFont object or a ``glyphsLib`` GSFontMaster
              object OR a ``babelfont`` Font object.
        glyphname: name of the glyph.

    Returns: A dictionary with the following keys:
            - ``width``: Advance width of the glyph.
            - ``lsb``: Left side-bearing
            - ``rsb``: Right side-bearing
            - ``xMin``: minimum X coordinate
            - ``xMax``: maximum X coordinate
            - ``yMin``: minimum Y coordinate
            - ``yMax``: maximum Y coordinate
            - ``fullwidth``: xMax - xMin
            - ``rise``: difference in Y coordinate between cursive entry and exit
    """
    if glyphtools.glyphs.isglyphs(font):
        return glyphtools.glyphs.get_glyph_metrics(font, glyphname, **kwargs)
    if glyphtools.babelfont.isbabelfont(font):
        return glyphtools.babelfont.get_glyph_metrics(font, glyphname, **kwargs)
    metrics = {}
    if "hmtx" in font:
        metrics = {
            "width": font["hmtx"][glyphname][0],
            "lsb": font["hmtx"][glyphname][1],
        }
    else:
        warnings.warn("No hmtx table in this font!")
        metrics = {"width": font["head"].unitsPerEm, "lsb": 0}
    if "glyf" in font:
        glyf = font["glyf"][glyphname]
        try:
            metrics["xMin"], metrics["xMax"], metrics["yMin"], metrics["yMax"] = (
                glyf.xMin,
                glyf.xMax,
                glyf.yMin,
                glyf.yMax,
            )
        except Exception:
            metrics["xMin"], metrics["xMax"], metrics["yMin"], metrics["yMax"] = (
                0,
                0,
                0,
                0,
            )
    else:
        bounds = font.getGlyphSet()[glyphname]._glyph.calcBounds(font.getGlyphSet())
        try:
            metrics["xMin"], metrics["yMin"], metrics["xMax"], metrics["yMax"] = bounds
        except Exception:
            metrics["xMin"], metrics["xMax"], metrics["yMin"], metrics["yMax"] = (
                0,
                0,
                0,
                0,
            )
    metrics["rise"] = get_rise(font, glyphname)
    metrics["run"] = get_run(font, glyphname)
    metrics["rsb"] = metrics["width"] - metrics["xMax"]
    metrics["fullwidth"] = metrics["xMax"] - metrics["xMin"]
    return metrics


def get_rise(font, glyphname, **kwargs):
    """Return the Arabic rise of the glyph (Y difference between entry and exit)."""
    if glyphtools.glyphs.isglyphs(font):
        return glyphtools.glyphs.get_rise(font, glyphname, **kwargs)
    if glyphtools.babelfont.isbabelfont(font):
        return glyphtools.babelfont.get_rise(font[glyphname])
    # Find a cursive positioning feature or it's game over
    if "GPOS" not in font:
        return 0
    cursives = filter(lambda x: x.LookupType == 3, font["GPOS"].table.LookupList.Lookup)
    entry, exit = None, None
    for c in cursives:
        for s in c.SubTable:
            for glyph, record in zip(s.Coverage.glyphs, s.EntryExitRecord):
                if glyph != glyphname:
                    continue
                if record.EntryAnchor:
                    entry = (
                        record.EntryAnchor.XCoordinate,
                        record.EntryAnchor.YCoordinate,
                    )
                if record.ExitAnchor:
                    exit = (
                        record.ExitAnchor.XCoordinate,
                        record.ExitAnchor.YCoordinate,
                    )
    if not entry and not exit:
        return 0
    if entry and not exit:
        return entry[1]
    if exit and not entry:
        return 0
    return entry[1] - exit[1]


def get_run(font, glyphname, **kwargs):
    """Return the Arabic run of the glyph (X difference between entry and exit)."""
    if glyphtools.glyphs.isglyphs(font):
        return glyphtools.glyphs.get_run(font, glyphname, **kwargs)
    if glyphtools.babelfont.isbabelfont(font):
        return glyphtools.babelfont.get_run(font[glyphname])
    # Find a cursive positioning feature or it's game over
    width = font["hmtx"][glyphname][0]
    if "GPOS" not in font:
        return width
    cursives = filter(lambda x: x.LookupType == 3, font["GPOS"].table.LookupList.Lookup)
    entry, exit = None, None
    for c in cursives:
        for s in c.SubTable:
            for glyph, record in zip(s.Coverage.glyphs, s.EntryExitRecord):
                if glyph != glyphname:
                    continue
                if record.EntryAnchor:
                    entry = (
                        record.EntryAnchor.XCoordinate,
                        record.EntryAnchor.YCoordinate,
                    )
                if record.ExitAnchor:
                    exit = (
                        record.ExitAnchor.XCoordinate,
                        record.ExitAnchor.YCoordinate,
                    )
    if not entry and not exit:
        return width
    if entry and not exit:
        return entry[0]
    if exit and not entry:
        return width - exit[0]
    return entry[0] - exit[0]


def bin_dictionary(d, bincount=5):
    """Organise a dictionary into a number of bins.

    The bins are not guaranteed to contain the same number of entries; the
    one-dimensional ckmeans clustering algorithm is used to cluster entries
    based on value similarity. For example, if there are five entries in the
    dictionary with values of 100, 102, 105, 210, and 220 respectively, and
    you ask for two bins, the first bin will contain three entries and the
    second will contain two. This is usually what you want.

    Returns: An list ``bincount`` two-element tuples. The first element is a
        list of dictionary keys in this bin; the second is the average
        value of the items in this bin.
    """
    justvalues = d.values()
    if bincount > len(d.keys()):
        bincount = len(d.keys())
    clusters = ckmeans(list(justvalues), bincount)
    binned = []
    for c in clusters:
        thiscluster = []
        for k, v in d.items():
            if v in c:
                thiscluster.append((k, v))
        thiscluster = (
            [x[0] for x in thiscluster],
            int(statistics.mean([x[1] for x in thiscluster])),
        )
        binned.append(thiscluster)
    return binned


def bin_glyphs_by_metric(font, glyphs, category, bincount=5):
    """Organise glyphs according to a given metric.

    Organises similar glyphs into a number of bins. See documentation for
    :func:`bin_dictionary` above.

    Args:
        font: a ``fontTools`` TTFont object or a ``glyphsLib`` GSFontMaster
              object OR a ``babelfont`` Font object.
        glyphs: a collection of glyph names
        category: the metric (see metric keys in :func:`get_glyph_metrics`.)
        bincount: number of bins to return

    Returns:
        A list of
    """
    metrics = {g: get_glyph_metrics(font, g)[category] for g in glyphs}
    return bin_dictionary(metrics, bincount)


def get_beziers(font, glyph):
    """Return the glyph as a set of ``beziers.BezierPath`` objects.

    Args:
        font: a ``fontTools`` TTFont object or a ``glyphsLib`` GSFontMaster
              object OR a ``babelfont`` Font object.
        glyph: name of the glyph.

    Returns: A list of ``BezierPath`` objects.

    """
    if glyphtools.glyphs.isglyphs(font):
        return glyphtools.glyphs.beziers(font, glyph)
    elif glyphtools.babelfont.isbabelfont2(font):
        return BezierPath.fromDrawable(glyphtools.babelfont.get_glyph(font, glyph))
    elif glyphtools.babelfont.isbabelfont(font):
        return BezierPath.fromDrawable(font[glyph], font)
    else:
        return BezierPath.fromFonttoolsGlyph(font, glyph)


def determine_kern(
    font, glyph1, glyph2, targetdistance, offset1=(0, 0), offset2=(0, 0), maxtuck=0.4
):
    """Determine a kerning value required to set two glyphs at given ink-to-ink distance.

    The value is bounded by the ``maxtuck`` parameter. For example, if
    ``maxtuck`` is 0.20, the right glyph will not be placed any further
    left than 80% of the width of left glyph, even if this places the
    ink further than ``targetdistance`` units away.

    Args:
        font: a ``fontTools`` TTFont object or a ``glyphsLib`` GSFontMaster
              object OR a ``babelfont`` Font object.
        glyph1: name of the left glyph.
        glyph2: name of the right glyph.
        targetdistance: distance to set the glyphs apart.
        offset1: offset (X-coordinate, Y-coordinate) to place left glyph.
        offset2: offset (X-coordinate, Y-coordinate) to place right glyph.
        maxtuck: maximum proportion of the left glyph's width to kern.

    Returns: A kerning value, in units.
    """
    paths1 = get_beziers(font, glyph1)
    paths2 = get_beziers(font, glyph2)
    metrics1 = get_glyph_metrics(font, glyph1)
    offset1 = Point(*offset1)
    offset2 = Point(offset2[0] + metrics1["width"], offset2[1])
    kern = 0
    last_best = None

    iterations = 0
    while True:
        # Compute min distance
        min_distance = None
        for p1 in paths1:
            p1 = p1.clone().translate(offset1)
            for p2 in paths2:
                p2 = p2.clone().translate(Point(offset2.x + kern, offset2.y))
                d = p1.distanceToPath(p2, samples=3)
                if not min_distance or d[0] < min_distance:
                    min_distance = d[0]
        if not last_best or min_distance < last_best:
            last_best = min_distance
        else:
            break  # Nothing helped
        if abs(min_distance - targetdistance) < 1 or iterations > 10:
            break
        iterations = iterations + 1
        kern = kern + (targetdistance - min_distance)

    kern = kern -  metrics1["rsb"]
    if maxtuck:
        kern = max(kern, -(metrics1["xMax"] * (1+maxtuck)) + metrics1["rsb"])
    else:
        kern = max(kern, -(metrics1["xMax"]) + metrics1["rsb"])
    kern = max(kern, -metrics1["width"])
    return int(kern)


def duplicate_glyph(babelfont, existing, new):
    """Add a new glyph to the font duplicating an existing one.

    Args:
        font: a ``babelfont``/``fontParts`` Font object.
        existing: name of the glyph to duplicate.
        new: name of the glyph to add.
    """
    existing_glyph = glyphtools.layers[0][existing]
    new_glyph = glyphtools.layers[0].newGlyph(new)

    for c in existing_glyph.contours:
        new_glyph.appendContour(c)
    for c in existing_glyph.components:
        new_glyph.appendComponent(c)
    new_glyph.width = existing_glyph.width
    old_category = babelfont[existing].category  # babelfont only
    set_glyph_category(babelfont, new, old_category[0], old_category[1])

def isbabelfont(font):
    if hasattr(font, "_set_kerning"):  # BBF 1
        return True
    if isbabelfont2(font):
        return True
    return False


def isbabelfont2(font):
    if hasattr(font, "_master_map"):  # BBF 2 Font
        return True
    if hasattr(font, "get_glyph_layer"): # BBF 2 Master
        return True
    return False


def get_glyph(font, glyphname):
    if hasattr(font, "_master_map"):  # BBF 2 Font
        return font.default_master.get_glyph_layer(glyphname)
    if hasattr(font, "get_glyph_layer"): # BBF 2 Master
        return font.get_glyph_layer(glyphname)
    return font[glyphname]

def get_glyph_metrics(font, glyphname):
    g = get_glyph(font, glyphname)
    if isbabelfont2(font):
        metrics = {"width": g.width, "lsb": g.lsb, "rsb": g.rsb}
    else:
        metrics = {"width": g.width, "lsb": g.leftMargin, "rsb": g.rightMargin}
    bounds = g.bounds
    if bounds:
        (metrics["xMin"], metrics["yMin"], metrics["xMax"], metrics["yMax"]) = g.bounds
    else:
        (metrics["xMin"], metrics["yMin"], metrics["xMax"], metrics["yMax"]) = (0,0,0,0)
    metrics["rise"] = get_rise(g)
    metrics["run"] = get_run(g)
    metrics["fullwidth"] = metrics["xMax"] - metrics["xMin"]
    return metrics


def get_rise(glyph):
    entry = [a.y for a in glyph.anchors if a.name == "entry"]
    entry.append(0)  # In case there isn't one
    exit = [a.y for a in glyph.anchors if a.name == "exit"]
    exit.append(0)

    return entry[0] - exit[0]

def get_run(glyph):
    entry = [a.x for a in glyph.anchors if a.name == "entry"]
    entry.append(glyph.width)  # In case there isn't one
    exit = [a.x for a in glyph.anchors if a.name == "exit"]
    exit.append(0)

    return entry[0] - exit[0]

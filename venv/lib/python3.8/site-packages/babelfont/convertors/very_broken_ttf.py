from fontTools.ttLib import TTFont
from babelfont.font import Font


def can_load(filename):
    if not (filename.endswith(".otf") or filename.endswith(".ttf")):
      return False
    font = TTFont(filename)
    return ("glyf" not in font and "CFF " not in font)

def can_save(filename):
    return False

def load(filename, **kwargs):
    return _load_ttfont(TTFont(filename))

def _load_ttfont(ttfont):
    bbf = Font()
    bbf.lib.glyphOrder = ttfont.getGlyphOrder()
    # That's it.

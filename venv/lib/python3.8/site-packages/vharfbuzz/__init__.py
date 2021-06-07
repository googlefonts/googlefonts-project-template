__author__ = """Simon Cozens"""
__email__ = "simon@simon-cozens.org"
__version__ = '0.1.0'

import uharfbuzz as hb
from fontTools.ttLib import TTFont
import re

class FakeBuffer():
    def __init__(self):
        pass

class FakeItem():
    def __init__(self):
        pass


class Vharfbuzz:
    """A user-friendlier way to use Harfbuzz in Python.

    Args:
        filename (str): A path to a TrueType font file.
    """

    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, "rb") as fontfile:
            self.fontdata = fontfile.read()
        self.ttfont = TTFont(filename)
        self.glyphOrder = self.ttfont.getGlyphOrder()
        self.prepare_shaper()
        self.shapers = None
        self.drawfuncs = None

    def prepare_shaper(self):
        face = hb.Face(self.fontdata)
        font = hb.Font(face)
        upem = face.upem
        font.scale = (upem, upem)
        hb.ot_font_set_funcs(font)
        self.hbfont = font

    def make_message_handling_function(self, buf, onchange):
        self.history = {"GSUB": [], "GPOS": []}
        self.lastLookupID = None

        def handle_message(msg, buf2):
            m = re.match("start lookup (\\d+)", msg)
            if m:
                lookupid = int(m[1])
                self.history[self.stage].append(self.serialize_buf(buf2))

            m = re.match("end lookup (\\d+)", msg)
            if m:
                lookupid = int(m[1])
                if self.serialize_buf(buf2) != self.history[self.stage][-1]:
                    onchange(self, self.stage, lookupid, self._copy_buf(buf2))
                self.history[self.stage].pop()
            if msg.startswith("start GPOS stage"):
                self.stage = "GPOS"

        return handle_message

    def shape(self, text, parameters=None, onchange=None):
        """Shapes a text

    This shapes a piece of text.

    Args:
        text (str): A string of text
        parameters: A dictionary containing parameters to pass to Harfbuzz.
            Relevant keys include ``script``, ``direction``, ``language``
            (these three are normally guessed from the string contents),
            ``features``, ``variations`` and ``shaper``.
        onchange: An optional function with three parameters. See below.

    Additionally, if an `onchange` function is provided, this will be called
    every time the buffer changes *during* shaping, with the following arguments:

    - ``self``: the vharfbuzz object.
    - ``stage``: either "GSUB" or "GPOS"
    - ``lookupid``: the current lookup ID
    - ``buffer``: a copy of the buffer as a list of lists (glyphname, cluster, position)

    Returns:
        A uharfbuzz ``hb.Buffer`` object
    """
        if not parameters:
            parameters = {}
        self.prepare_shaper()
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        if "script" in parameters and parameters["script"]:
            buf.script = parameters["script"]
        if "direction" in parameters and parameters["direction"]:
            buf.direction = parameters["direction"]
        if "language" in parameters and parameters["language"]:
            buf.language = parameters["language"]
        shapers = self.shapers
        if "shaper" in parameters and parameters["shaper"]:
            shapers = [parameters["shaper"]]

        features = parameters.get("features")
        if "variations" in parameters:
            self.hbfont.set_variations(parameters["variations"])
        self.stage = "GSUB"
        if onchange:
            f = self.make_message_handling_function(buf, onchange)
            buf.set_message_func(f)
        hb.shape(self.hbfont, buf, features, shapers=shapers)
        self.stage = "GPOS"
        return buf

    def _copy_buf(self, buf):
        # Or at least the bits we care about
        outs = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            l = [self.glyphOrder[info.codepoint], info.cluster]
            if self.stage == "GPOS":
                l.append(pos.position)
            else:
                l.append(None)
            outs.append(l)
        return outs

    def serialize_buf(self, buf, glyphsonly=False):
        """Serializes a buffer to a string

        Returns the contents of the given buffer in a string format similar to
        that used by ``hb-shape``.

        Args:
            buf: The ``hb.Buffer`` object.

        Returns: A serialized string.

       """
        outs = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyphname = self.glyphOrder[info.codepoint]
            if glyphsonly:
                outs.append(glyphname)
                continue
            outs.append("%s=%i" % (glyphname, info.cluster))
            if self.stage == "GPOS" and (pos.position[0] != 0 or pos.position[1] != 0):
                outs[-1] = outs[-1] + "@%i,%i" % (pos.position[0], pos.position[1])
            if self.stage == "GPOS":
                outs[-1] = outs[-1] + "+%i" % (pos.position[2])
        return "|".join(outs)

    def buf_from_string(self, s):
        """Deserializes a string.

        This attempts to perform the inverse operation to :py:meth:`serialize_buf`,
        turning a serialized buffer back into an object. The object is not a
        ``hb.Buffer``, but has a similar structure (``glyph_infos`` and ``glyph_positions``)
        so can be passed to code which expects a ``hb.Buffer``, such as
        :py:meth:`buf_to_svg` below.

        Args:
            s (str): A string produced by :py:meth:`serialize_buf`

        Returns a ``FakeBuffer`` object.
        """
        buf = FakeBuffer()
        buf.glyph_infos = []
        buf.glyph_positions = []
        for item in s.split("|"):
            m = re.match(r"^(.*)=(\d+)(@(-?\d+),(-?\d+))?(\+(-?\d+))?$", item)
            if not m:
                raise ValueError("Couldn't parse glyph %s in %s" % (item,s))
            groups = m.groups()
            info = FakeItem()
            info.codepoint = self.ttfont.getGlyphID(groups[0])
            info.cluster = int(groups[1])
            buf.glyph_infos.append(info)
            pos = FakeItem()
            pos.position = [ int(x or 0) for x in (groups[3], groups[4], groups[6], 0) ]  # Sorry, vertical scripts
            buf.glyph_positions.append(pos)
        return buf

    def setup_svg_draw_funcs(self):
        if self.drawfuncs:
            return

        def move_to(x, y, c):
            c["output_string"] = c["output_string"] + f"M{x},{y}"

        def line_to(x, y, c):
            c["output_string"] = c["output_string"] + f"L{x},{y}"

        def cubic_to(c1x, c1y, c2x, c2y, x, y, c):
            c["output_string"] = (
                c["output_string"] + f"C{c1x},{c1y} {c2x},{c2y} {x},{y}"
            )

        def quadratic_to(c1x, c1y, x, y, c):
            c["output_string"] = c["output_string"] + f"Q{c1x},{c1y} {x},{y}"

        def close_path(c):
            c["output_string"] = c["output_string"] + "Z"

        self.drawfuncs = hb.DrawFuncs()
        self.drawfuncs.set_move_to_func(move_to)
        self.drawfuncs.set_line_to_func(line_to)
        self.drawfuncs.set_cubic_to_func(cubic_to)
        self.drawfuncs.set_quadratic_to_func(quadratic_to)
        self.drawfuncs.set_close_path_func(close_path)

    def glyph_to_svg_path(self, gid):
        """Converts a glyph to SVG

        Args:
            gid (int): Glyph ID to render

        Returns: An SVG string containing a path to represent the glyph.
        """
        if not hasattr(hb, "DrawFuncs"):
            raise ValueError(
                "glyph_to_svg_path requires uharfbuzz with draw function support"
            )

        self.setup_svg_draw_funcs()
        container = {"output_string": ""}
        self.drawfuncs.draw_glyph(self.hbfont, gid, container)
        return container["output_string"]

    def buf_to_svg(self, buf):
        """Converts a buffer to SVG

        Args:
            buf (hb.Buffer): uharfbuzz ``hb.Buffer``

        Returns: An SVG string containing a rendering of the buffer
        """
        x_cursor = 0
        paths = []
        svg = ""
        if "hhea" in self.ttfont:
            ascender = self.ttfont["hhea"].ascender + 500
            descender = self.ttfont["hhea"].descender - 500
            fullheight = ascender - descender
        elif "OS/2":
            ascender = self.ttfont["OS/2"].sTypoAscender + 500
            descender = self.ttfont["OS/2"].sTypoDescender - 500
            fullheight = ascender - descender
        else:
            fullheight = 1500
            descender = 500
        y_cursor = -descender

        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyph_path = self.glyph_to_svg_path(info.codepoint)
            dx, dy = pos.position[0], pos.position[1]
            p = (
                f'<path d="{glyph_path}" '
                + f' transform="translate({x_cursor+dx}, {y_cursor+dy})"/>\n'
            )
            svg += p
            x_cursor += pos.position[2]
            y_cursor += pos.position[3]

        svg = (
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x_cursor} {fullheight}"'
                + ' transform="matrix(1 0 0 -1 0 0)">\n'
            )
            + svg
            + "</svg>\n"
        )
        return svg


# v = Vharfbuzz("/Users/simon/Library/Fonts/SourceSansPro-Regular.otf")
# buf = v.shape("ABCj")
# svg = v.buf_to_svg(buf)
# import cairosvg
# cairosvg.svg2png(bytestring=svg, write_to="foo.png")

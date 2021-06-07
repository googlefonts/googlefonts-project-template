import unittest
import tempfile
import os
from fontParts.world import RFont, FontList, OpenFont

class TestFontList(unittest.TestCase):

    def getFont(self):
        font, _ = self.objectGenerator("font")
        return font

    # ----
    # Sort
    # ----

    def getFonts_sortBy(self, attr, values):
        fonts = FontList()
        for value in values:
            font = self.getFont()
            setattr(font.info, attr, value)
            if attr != "familyName":
                font.info.familyName = "%s %s" % (attr, repr(value))
            fonts.append(font)
        return fonts

    # Sort Description Strings
    # ------------------------

    def getFont_sortBy_monospaceGlyphs(self):
        font = self.getFont()
        font.info.familyName = "monospace %s" % str(id(font))
        glyph1 = font.newGlyph("a")
        glyph1.width = 100
        glyph2 = font.newGlyph("b")
        glyph2.width = 100
        return font

    def getFont_sortBy_proportionalGlyphs(self):
        font = self.getFont()
        font.info.familyName = "proportional %s" % str(id(font))
        glyph1 = font.newGlyph("a")
        glyph1.width = 100
        glyph2 = font.newGlyph("b")
        glyph2.width = 200
        return font

    # familyName

    def test_sortBy_familyName(self):
        fonts = self.getFonts_sortBy(
            "familyName",
            ["aaa", "bbb", "ccc", None]
        )
        font1, font2, font3, font4 = fonts
        fonts.sortBy("familyName")
        expected = [font4, font1, font2, font3]
        self.assertEqual(fonts, expected)

    # styleName

    def test_sortBy_styleName(self):
        fonts = self.getFonts_sortBy(
            "styleName",
            ["aaa", "bbb", "ccc", None]
        )
        font1, font2, font3, font4 = fonts
        fonts.sortBy("styleName")
        expected = [font4, font1, font2, font3]
        self.assertEqual(fonts, expected)

    # isRoman

    def test_sortBy_isRoman_styleMapStyleName(self):
        fonts = self.getFonts_sortBy(
            "styleMapStyleName",
            ["regular", "italic", "bold", "bold italic"]
        )
        font1, font2, font3, font4 = fonts
        fonts.reverse()
        fonts.sortBy("isRoman")
        expected = [font3, font1, font4, font2]
        self.assertEqual(fonts, expected)

    def test_sortBy_isRoman_italicAngle(self):
        fonts = self.getFonts_sortBy(
            "italicAngle",
            [1, 2, 3, 0]
        )
        font1, font2, font3, font4 = fonts
        fonts.sortBy("isRoman")
        expected = [font4, font1, font2, font3]
        self.assertEqual(fonts, expected)

    # isItalic

    def test_sortBy_isItalic_styleMapStyleName(self):
        fonts = self.getFonts_sortBy(
            "styleMapStyleName",
            ["regular", "italic", "bold", "bold italic"]
        )
        font1, font2, font3, font4 = fonts
        fonts.sortBy("isItalic")
        expected = [font2, font4, font1, font3]
        self.assertEqual(fonts, expected)

    def test_sortBy_isItalic_italicAngle(self):
        fonts = self.getFonts_sortBy(
            "italicAngle",
            [0, 1, 2, 3]
        )
        font1, font2, font3, font4 = fonts
        fonts.sortBy("isItalic")
        expected = [font2, font3, font4, font1]
        self.assertEqual(fonts, expected)

    # widthValue

    def test_sortBy_widthValue(self):
        fonts = self.getFonts_sortBy(
            "openTypeOS2WidthClass",
            [1, 2, 3, None]
        )
        font1, font2, font3, font4 = fonts
        fonts.sortBy("widthValue")
        expected = [font4, font1, font2, font3]
        self.assertEqual(fonts, expected)

    # weightValue

    def test_sortBy_weightValue(self):
        fonts = self.getFonts_sortBy(
            "openTypeOS2WeightClass",
            [100, 200, 300, None]
        )
        font1, font2, font3, font4 = fonts
        fonts.sortBy("weightValue")
        expected = [font4, font1, font2, font3]
        self.assertEqual(fonts, expected)

    # isMonospace

    def test_sortBy_isMonospace_postscriptIsFixedPitch(self):
        fonts = self.getFonts_sortBy(
            "postscriptIsFixedPitch",
            [True, True, False, False]
        )
        font1, font2, font3, font4 = fonts
        fonts.reverse()
        fonts.sortBy("isMonospace")
        expected = [font2, font1, font4, font3]
        self.assertEqual(fonts, expected)

    def test_sortBy_isMonospace_glyphs(self):
        font1 = self.getFont_sortBy_monospaceGlyphs()
        font2 = self.getFont_sortBy_monospaceGlyphs()
        font3 = self.getFont_sortBy_proportionalGlyphs()
        font4 = self.getFont_sortBy_proportionalGlyphs()
        fonts = FontList()
        fonts.extend([font1, font2, font3, font4])
        fonts.reverse()
        fonts.sortBy("isMonospace")
        expected = [font2, font1, font4, font3]
        self.assertEqual(fonts, expected)

    # isProportional

    def test_sortBy_isProportional_postscriptIsFixedPitch(self):
        fonts = self.getFonts_sortBy(
            "postscriptIsFixedPitch",
            [False, False, True, True]
        )
        font1, font2, font3, font4 = fonts
        fonts.reverse()
        fonts.sortBy("isProportional")
        expected = [font2, font1, font4, font3]
        self.assertEqual(fonts, expected)

    def test_sortBy_isProportional_glyphs(self):
        font1 = self.getFont_sortBy_monospaceGlyphs()
        font2 = self.getFont_sortBy_monospaceGlyphs()
        font3 = self.getFont_sortBy_proportionalGlyphs()
        font4 = self.getFont_sortBy_proportionalGlyphs()
        fonts = FontList()
        fonts.extend([font1, font2, font3, font4])
        fonts.sortBy("isProportional")
        expected = [font3, font4, font1, font2]
        self.assertEqual(fonts, expected)

    # font.info Attributes

    def test_sortBy_fontInfoAttribute_xHeight(self):
        fonts = self.getFonts_sortBy(
            "xHeight",
            [10, 20, 30, 40]
        )
        font1, font2, font3, font4 = fonts
        fonts.reverse()
        fonts.sortBy("xHeight")
        expected = [font1, font2, font3, font4]
        self.assertEqual(fonts, expected)

    # Sort Value Function
    # -------------------

    def getFont_withGlyphCount(self, count):
        font = self.getFont()
        for i in range(count):
            font.newGlyph("glyph%d" % i)
        font.info.familyName = str(count)
        return font

    def test_sortBy_sortValueFunction(self):
        font1 = self.getFont_withGlyphCount(10)
        font2 = self.getFont_withGlyphCount(20)
        font3 = self.getFont_withGlyphCount(30)
        font4 = self.getFont_withGlyphCount(40)
        fonts = FontList()
        fonts.extend([font1, font2, font3, font4])
        fonts.reverse()
        def glyphCountSortValue(font):
            return len(font)
        fonts.sortBy(glyphCountSortValue)
        expected = [font1, font2, font3, font4]
        self.assertEqual(fonts, expected)


    # ------
    # Search
    # ------

    # family name

    def test_getFontsByFamilyName(self):
        font1 = self.getFont()
        font1.info.familyName = "A"
        font2 = self.getFont()
        font2.info.familyName = "B"
        font3 = self.getFont()
        font3.info.familyName = "C"
        font4 = self.getFont()
        font4.info.familyName = "A"
        fonts = FontList()
        fonts.extend([font1, font2, font3, font4])
        found = fonts.getFontsByFamilyName("A")
        self.assertEqual(found, [font1, font4])

    # style name

    def test_getFontsByStyleName(self):
        font1 = self.getFont()
        font1.info.styleName = "A"
        font2 = self.getFont()
        font2.info.styleName = "B"
        font3 = self.getFont()
        font3.info.styleName = "C"
        font4 = self.getFont()
        font4.info.styleName = "A"
        fonts = FontList()
        fonts.extend([font1, font2, font3, font4])
        found = fonts.getFontsByStyleName("A")
        self.assertEqual(found, [font1, font4])

    # family name, style name

    def test_getFontsByFamilyNameStyleName(self):
        font1 = self.getFont()
        font1.info.familyName = "A"
        font1.info.styleName = "1"
        font2 = self.getFont()
        font2.info.familyName = "A"
        font2.info.styleName = "2"
        font3 = self.getFont()
        font3.info.familyName = "B"
        font3.info.styleName = "1"
        font4 = self.getFont()
        font4.info.familyName = "A"
        font4.info.styleName = "1"
        fonts = FontList()
        fonts.extend([font1, font2, font3, font4])
        found = fonts.getFontsByFamilyNameStyleName("A", "1")
        self.assertEqual(found, [font1, font4])

class TestFontOpen(unittest.TestCase):

    def setUp(self):
        font, _ = self.objectGenerator("font")
        self.font_dir = tempfile.mkdtemp()
        self.font_path = os.path.join(self.font_dir, "test.ufo")
        font.save(self.font_path)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.font_dir)

    def test_font_open(self):
        OpenFont(self.font_path)


class TestFontShell_RFont(unittest.TestCase):

    def test_fontshell_RFont_empty(self):
        RFont()

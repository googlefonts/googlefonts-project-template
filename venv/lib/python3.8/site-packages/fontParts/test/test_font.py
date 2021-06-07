import unittest
import collections
import tempfile
import os
import shutil


class TestFont(unittest.TestCase):

    # ------
    # Layers
    # ------

    def getFont_layers(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newLayer("layer " + name)
        return font

    def test_getLayer_unknown(self):
        font = self.getFont_layers()
        with self.assertRaises(ValueError):
            font.getLayer("There is no layer with this name.")

    # ------
    # Glyphs
    # ------

    def getFont_glyphs(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newGlyph(name)
        return font

    def getFont_guidelines(self):
        font, _ = self.objectGenerator("font")
        font.appendGuideline((1, 2), 0, "Test Guideline 1")
        font.appendGuideline((3, 4), 90, "Test Guideline 2")
        return font

    def test_appendGuideline_valid_object(self):
        font, _ = self.objectGenerator("font")
        src, _ = self.objectGenerator("guideline")
        src.position = (1, 2)
        src.angle = 123
        src.name = "test"
        src.color = (1, 1, 1, 1)
        src.getIdentifier()
        dst = font.appendGuideline(guideline=src)
        self.assertNotEqual(src, dst)
        self.assertEqual(src.position, dst.position)
        self.assertEqual(src.angle, dst.angle)
        self.assertEqual(src.name, dst.name)
        self.assertEqual(src.color, dst.color)
        self.assertEqual(src.identifier, dst.identifier)

    # glyphOrder

    def test_glyphOrder(self):
        font = self.getFont_glyphs()
        expectedGlyphOrder = ["A", "B", "C", "D"]
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # reverse the excepected glyph order and set it
        expectedGlyphOrder.reverse()
        font.glyphOrder = expectedGlyphOrder
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # add a glyph
        expectedGlyphOrder.append("newGlyph")
        font.newGlyph("newGlyph")
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # remove a glyph
        expectedGlyphOrder.remove("newGlyph")
        del font["newGlyph"]
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # insert a glyph, where the glyph is at the beginning of the glyph order
        glyph, _ = self.objectGenerator("glyph")
        font["D"] = glyph
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # insert a glyph, where the glyph is at the end of the glyph order
        glyph, _ = self.objectGenerator("glyph")
        font["A"] = glyph
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))

    # len

    def test_len_initial(self):
        font = self.getFont_glyphs()
        self.assertEqual(
            len(font),
            4
        )

    def test_len_two_layers(self):
        font = self.getFont_glyphs()
        layer = font.newLayer("test")
        layer.newGlyph("X")
        self.assertEqual(
            len(font),
            4
        )

    # insert glyphs

    def test_insertGlyph(self):
        font, _ = self.objectGenerator("font")
        glyph, _ = self.objectGenerator("glyph")
        font.insertGlyph(glyph, "inserted1")
        self.assertIn("inserted1", font)
        font["inserted2"] = glyph
        self.assertIn("inserted2", font)
        font.newGlyph("A")
        glyph.unicode = 123
        font["A"] = glyph
        self.assertEqual(font["A"].unicode, 123)

    # ----
    # flatKerning
    # ----

    def test_flatKerning(self):
        font = self.getFont_glyphs()
        # glyph, glyph kerning
        font.kerning["A", "V"] = -100
        font.kerning["V", "A"] = -200
        expected = {("A", "V"): -100, ("V", "A"): -200}
        self.assertEqual(font.getFlatKerning(), expected)
        # add some groups
        font.groups["public.kern1.O"] = ["O", "Ograve"]
        font.groups["public.kern2.O"] = ["O", "Ograve"]
        # group, group kerning
        font.kerning["public.kern1.O", "public.kern2.O"] = -50
        expected = {
            ('O', 'O'): -50,
            ('Ograve', 'O'): -50,
            ('O', 'Ograve'): -50,
            ('Ograve', 'Ograve'): -50,
            ('A', 'V'): -100,
            ('V', 'A'): -200
        }
        self.assertEqual(font.getFlatKerning(), expected)
        # glyph, group exception
        font.kerning["O", "public.kern2.O"] = -30
        expected = {
            ('O', 'O'): -30,
            ('Ograve', 'O'): -50,
            ('O', 'Ograve'): -30,
            ('Ograve', 'Ograve'): -50,
            ('A', 'V'): -100,
            ('V', 'A'): -200
        }
        self.assertEqual(font.getFlatKerning(), expected)
        # glyph, glyph exception
        font.kerning["O", "Ograve"] = -70
        expected = {
            ('O', 'O'): -30,
            ('Ograve', 'O'): -50,
            ('O', 'Ograve'): -70,
            ('Ograve', 'Ograve'): -50,
            ('A', 'V'): -100,
            ('V', 'A'): -200
        }
        self.assertEqual(font.getFlatKerning(), expected)

    # ----
    # Hash
    # ----

    def test_hash_same_object(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(
            hash(font_one),
            hash(font_one)
        )

    def test_hash_different_object(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        self.assertNotEqual(
            hash(font_one),
            hash(font_two)
        )

    def test_hash_same_object_variable_assignment(self):
        font_one = self.getFont_glyphs()
        a = font_one
        self.assertEqual(
            hash(font_one),
            hash(a)
        )

    def test_hash_different_object_variable_assignment(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        a = font_one
        self.assertNotEqual(
            hash(font_two),
            hash(a)
        )

    def test_hash_is_hasbable(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(
            isinstance(font_one, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(
            font_one,
            font_one
        )

    def test_object_not_equal_other(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        self.assertNotEqual(
            font_one,
            font_two
        )

    def test_object_equal_self_variable_assignment(self):
        font_one = self.getFont_glyphs()
        a = font_one
        a.newGlyph("XYZ")
        self.assertEqual(
            font_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        a = font_one
        self.assertNotEqual(
            font_two,
            a
        )

    # ---------
    # Selection
    # ---------

    # Font

    def test_selected_true(self):
        font = self.getFont_glyphs()
        try:
            font.selected = False
        except NotImplementedError:
            return
        font.selected = True
        self.assertEqual(
            font.selected,
            True
        )

    def test_selected_false(self):
        font = self.getFont_glyphs()
        try:
            font.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selected,
            False
        )

    # Layers

    def test_selectedLayer_default(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedLayers,
            ()
        )

    def test_selectedLayer_setSubObject(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        layer1 = font.getLayer("layer A")
        layer2 = font.getLayer("layer B")
        layer1.selected = True
        layer2.selected = True
        self.assertEqual(
            font.selectedLayers,
            (layer1, layer2)
        )

    def test_selectedLayer_setFilledList(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        layer3 = font.getLayer("layer C")
        layer4 = font.getLayer("layer D")
        font.selectedLayers = [layer3, layer4]
        self.assertEqual(
            font.selectedLayers,
            (layer3, layer4)
        )

    def test_selectedLayer_setEmptyList(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        layer1 = font.getLayer("layer A")
        layer1.selected = True
        font.selectedLayers = []
        self.assertEqual(
            font.selectedLayers,
            ()
        )

    # Glyphs

    def test_selectedGlyphs_default(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )

    def test_selectedGlyphs_setSubObject(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(font.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph1, glyph2)
        )

    def test_selectedGlyphs_setFilledList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph3 = font["C"]
        glyph4 = font["D"]
        font.selectedGlyphs = [glyph3, glyph4]
        self.assertEqual(
            tuple(sorted(font.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph3, glyph4)
        )

    def test_selectedGlyphs_setEmptyList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph1.selected = True
        font.selectedGlyphs = []
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )

    # Glyph names

    def test_selectedGlyphNames_default(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedGlyphs,
            ()
        )

    def test_selectedGlyphNames_setSubObject(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(font.selectedGlyphNames)),
            ("A", "B")
        )

    def test_selectedGlyphNames_setFilledList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        font.selectedGlyphNames = ["C", "D"]
        self.assertEqual(
            tuple(sorted(font.selectedGlyphNames)),
            ("C", "D")
        )

    def test_selectedGlyphNames_setEmptyList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph1.selected = True
        font.selectedGlyphNames = []
        self.assertEqual(
            font.selectedGlyphNames,
            ()
        )

    # Guidelines

    def test_selectedGuidelines_default(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            font.selectedGuidelines,
            ()
        )

    def test_selectedGuidelines_setSubObject(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        guideline2 = font.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        guideline2.selected = True
        self.assertEqual(
            font.selectedGuidelines,
            (guideline2,)
        )

    def test_selectedGuidelines_setFilledList(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        guideline2 = font.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        font.selectedGuidelines = [guideline1, guideline2]
        self.assertEqual(
            font.selectedGuidelines,
            (guideline1, guideline2)
        )

    def test_selectedGuidelines_setEmptyList(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        try:
            guideline1.selected = True
        except NotImplementedError:
            return
        font.selectedGuidelines = []
        self.assertEqual(
            font.selectedGuidelines,
            ()
        )

    # save

    def _saveFontPath(self, ext):
        root = tempfile.mkdtemp()
        return os.path.join(root, "test.%s" % ext)

    def _tearDownPath(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    def _save(self, testCallback, **kwargs):
        path = self._saveFontPath(".ufo")
        font = self.getFont_glyphs()
        font.save(path, **kwargs)
        font.close()
        testCallback(path)
        self._tearDownPath(path)

    def test_save(self):
        def testCases(path):
            self.assertTrue(os.path.exists(path) and os.path.isdir(path))
        self._save(testCases)

    def test_save_formatVersion(self):
        from fontTools.ufoLib import UFOReader

        for version in [2, 3]:  # fails on formatVersion 1 (but maybe we should not worry about it...)
            def testCases(path):
                reader = UFOReader(path)
                self.assertEqual(reader.formatVersion, version)
            self._save(testCases, formatVersion=version)

    def test_save_fileStructure(self):
        from fontTools.ufoLib import UFOReader, UFOFileStructure

        for fileStructure in [None, "package", "zip"]:
            def testCases(path):
                reader = UFOReader(path)
                expectedFileStructure = fileStructure
                if fileStructure is None:
                    expectedFileStructure = UFOFileStructure.PACKAGE
                else:
                    expectedFileStructure = UFOFileStructure(fileStructure)
                self.assertEqual(reader.fileStructure, expectedFileStructure)
            self._save(testCases, fileStructure=fileStructure)

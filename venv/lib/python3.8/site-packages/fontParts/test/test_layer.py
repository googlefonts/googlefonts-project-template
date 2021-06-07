import unittest
import collections


class TestLayer(unittest.TestCase):

    # ------
    # Glyphs
    # ------

    def getLayer_glyphs(self):
        layer, _ = self.objectGenerator("layer")
        for name in "ABCD":
            layer.newGlyph(name)
        return layer

    def test_len(self):
        layer = self.getLayer_glyphs()
        self.assertEqual(
            len(layer),
            4
        )

    def _testInsertGlyph(self, setGlyphName=True):
        layer, _ = self.objectGenerator("layer")
        glyph, _ = self.objectGenerator("glyph")
        pen = glyph.getPen()
        pen.moveTo((100, 0))
        pen.lineTo((100, 500))
        pen.lineTo((500, 500))
        pen.closePath()
        glyph.width = 600
        if setGlyphName:
            glyph.name = "test"
        layer["test"] = glyph
        self.assertTrue("test" in layer)
        self.assertEqual(
            layer["test"].bounds,
            glyph.bounds
        )

    def test_set_glyph(self):
        self._testInsertGlyph(setGlyphName=True)

    def test_set_glyph_with_name_None(self):
        self._testInsertGlyph(setGlyphName=False)

    def test_get_glyph_in_font(self):
        layer = self.getLayer_glyphs()
        self.assertEqual(
            layer["A"].name,
            "A"
        )

    def test_get_glyph_not_in_font(self):
        layer = self.getLayer_glyphs()
        with self.assertRaises(KeyError):
            layer["E"]

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        layer_one = self.getLayer_glyphs()
        self.assertEqual(
            hash(layer_one),
            hash(layer_one)
        )

    def test_hash_object_other(self):
        layer_one = self.getLayer_glyphs()
        layer_two = self.getLayer_glyphs()
        self.assertNotEqual(
            hash(layer_one),
            hash(layer_two)
        )

    def test_hash_object_self_variable_assignment(self):
        layer_one = self.getLayer_glyphs()
        a = layer_one
        self.assertEqual(
            hash(layer_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        layer_one = self.getLayer_glyphs()
        layer_two = self.getLayer_glyphs()
        a = layer_one
        self.assertNotEqual(
            hash(layer_two),
            hash(a)
        )

    def test_is_hashable(self):
        layer_one = self.getLayer_glyphs()
        self.assertTrue(
            isinstance(layer_one, collections.Hashable)
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        layer_one = self.getLayer_glyphs()
        self.assertEqual(
            layer_one,
            layer_one
        )

    def test_object_not_equal_other(self):
        layer_one = self.getLayer_glyphs()
        layer_two = self.getLayer_glyphs()
        self.assertNotEqual(
            layer_one,
            layer_two
        )

    def test_object_equal_self_variable_assignment(self):
        layer_one = self.getLayer_glyphs()
        a = layer_one
        self.assertEqual(
            layer_one,
            a
        )

    def test_object_not_equal_self_variable_assignment(self):
        layer_one = self.getLayer_glyphs()
        layer_two = self.getLayer_glyphs()
        a = layer_one
        self.assertNotEqual(
            layer_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        layer.selected = True
        self.assertEqual(
            layer.selected,
            True
        )

    def test_selected_false(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            layer.selected,
            False
        )

    # Glyphs

    def test_selectedGlyphs_default(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )

    def test_selectedGlyphs_setSubObject(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph2 = layer["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph1, glyph2)
        )

    def test_selectedGlyphs_setFilledList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph3 = layer["C"]
        glyph4 = layer["D"]
        layer.selectedGlyphs = [glyph3, glyph4]
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph3, glyph4)
        )

    def test_selectedGlyphs_setEmptyList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph1.selected = True
        layer.selectedGlyphs = []
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )

    # Glyph Names

    def test_selectedGlyphNames_default(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            layer.selectedGlyphs,
            ()
        )

    def test_selectedGlyphNames_setSubObject(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph2 = layer["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphNames)),
            ("A", "B")
        )

    def test_selectedGlyphNames_setFilledList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        layer.selectedGlyphNames = ["C", "D"]
        self.assertEqual(
            tuple(sorted(layer.selectedGlyphNames)),
            ("C", "D")
        )

    def test_selectedGlyphNames_setEmptyList(self):
        layer = self.getLayer_glyphs()
        try:
            layer.selected = False
        except NotImplementedError:
            return
        glyph1 = layer["A"]
        glyph1.selected = True
        layer.selectedGlyphNames = []
        self.assertEqual(
            layer.selectedGlyphNames,
            ()
        )

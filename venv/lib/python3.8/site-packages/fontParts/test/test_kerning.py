import unittest
import collections


class TestKerning(unittest.TestCase):

    def getKerning_generic(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        groups["public.kern1.X"] = ["A", "B", "C"]
        groups["public.kern2.X"] = ["A", "B", "C"]
        kerning = font.kerning
        kerning.update({
            ("public.kern1.X", "public.kern2.X"): 100,
            ("B", "public.kern2.X"): 101,
            ("public.kern1.X", "B"): 102,
            ("A", "A"): 103,
        })
        return kerning

    def getKerning_font2(self):
        font, _ = self.objectGenerator("font")
        groups = font.groups
        groups["public.kern1.X"] = ["A", "B", "C"]
        groups["public.kern2.X"] = ["A", "B", "C"]
        kerning = font.kerning
        kerning.update({
            ("public.kern1.X", "public.kern2.X"): 200,
            ("B", "public.kern2.X"): 201,
            ("public.kern1.X", "B"): 202,
            ("A", "A"): 203,
        })
        return kerning

    # ---
    # len
    # ---

    def test_len_initial(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            len(kerning),
            4
        )

    def test_len_clear(self):
        kerning = self.getKerning_generic()
        kerning.clear()
        self.assertEqual(
            len(kerning),
            0
        )

    # --------
    # contains
    # --------

    def test_contains_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            ('A', 'A') in kerning,
            True
        )

    def test_contains_group_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            ("public.kern1.X", "public.kern2.X") in kerning,
            True
        )

    def test_contains_glyph_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            ("B", "public.kern2.X") in kerning,
            True
        )

    def test_contains_missing_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            ("H", "H") in kerning,
            False
        )

    # ---
    # del
    # ---

    def test_del(self):
        kerning = self.getKerning_generic()
        # Be sure it is here before deleting
        self.assertEqual(
            ('A', 'A') in kerning,
            True
        )
        # Delete
        del kerning[('A', 'A')]
        # Test
        self.assertEqual(
            ('A', 'A') in kerning,
            False
        )

    # ---
    # get
    # ---

    def test_get_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[('A', 'A')],
            103
        )

    def test_get_group_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[("public.kern1.X", "public.kern2.X")],
            100
        )

    def test_get_glyph_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[("B", "public.kern2.X")],
            101
        )

    def test_get_group_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning[("public.kern1.X", "B")],
            102
        )

    def test_get_fallback_default(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning.get(("F", "F")),
            None
        )

    def test_get_fallback_default_user(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning.get(("F", "F"), None),
            None
        )
        self.assertEqual(
            kerning.get(("F", "F"), 0),
            0
        )

    # ---
    # set
    # ---

    def test_set_glyph_glyph(self):
        kerning = self.getKerning_generic()
        kerning[('A', 'A')] = 1
        self.assertEqual(
            kerning[('A', 'A')],
            1
        )

    def test_set_group_group(self):
        kerning = self.getKerning_generic()
        kerning[("public.kern1.X", "public.kern2.X")] = 2
        self.assertEqual(
            kerning[("public.kern1.X", "public.kern2.X")],
            2
        )

    def test_set_glyph_group(self):
        kerning = self.getKerning_generic()
        kerning[("B", "public.kern2.X")] = 3
        self.assertEqual(
            kerning[("B", "public.kern2.X")],
            3
        )

    def test_set_group_glyph(self):
        kerning = self.getKerning_generic()
        kerning[("public.kern1.X", "B")] = 4
        self.assertEqual(
            kerning[("public.kern1.X", "B")],
            4
        )

    # ----
    # Find
    # ----

    def test_find_glyph_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning.find(('A', 'A')),
            103
        )

    def test_find_glyph_glyph_none(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning.find(('D', 'D')),
            None
        )

    def test_find_group_glyph(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning.find(('A', 'B')),
            102
        )

    def test_find_glyph_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning.find(('B', 'B')),
            101
        )

    def test_find_group_group(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            kerning.find(('C', 'C')),
            100
        )

    # ----
    # Hash
    # ----

    def test_hash(self):
        kerning = self.getKerning_generic()
        self.assertEqual(
            isinstance(kerning, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        kerning_one = self.getKerning_generic()
        self.assertEqual(
            kerning_one,
            kerning_one
        )

    def test_object_not_equal_other(self):
        kerning_one = self.getKerning_generic()
        kerning_two = self.getKerning_generic()
        self.assertNotEqual(
            kerning_one,
            kerning_two
        )

    def test_object_equal_self_variable_assignment(self):
        kerning_one = self.getKerning_generic()
        a = kerning_one
        self.assertEqual(
            kerning_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        kerning_one = self.getKerning_generic()
        kerning_two = self.getKerning_generic()
        a = kerning_one
        self.assertNotEqual(
            kerning_two,
            a
        )

    # -------------
    # Interpolation
    # -------------

    def test_interpolation_without_rounding(self):
        interpolated = self.getKerning_generic()
        kerning_min = self.getKerning_generic()
        kerning_max = self.getKerning_font2()
        interpolated.interpolate(0.515, kerning_min, kerning_max, round=False)

        self.assertEqual(
            interpolated[("public.kern1.X", "public.kern2.X")],
            151.5
        )

    def test_interpolation_with_rounding(self):
        interpolated = self.getKerning_generic()
        kerning_min = self.getKerning_generic()
        kerning_max = self.getKerning_font2()
        interpolated.interpolate(0.515, kerning_min, kerning_max, round=True)

        self.assertEqual(
            interpolated[("public.kern1.X", "public.kern2.X")],
            152
        )

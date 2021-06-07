import unittest
import collections


class TestInfo(unittest.TestCase):

    def getInfo_generic(self):
        info, _ = self.objectGenerator("info")
        info.unitsPerEm = 1000
        return info

    # ----------
    # Dimensions
    # ----------

    def test_get_unitsPerEm(self):
        info = self.getInfo_generic()
        self.assertEqual(
            info.unitsPerEm,
            1000
        )

    def test_set_valid_unitsPerEm_int(self):
        info = self.getInfo_generic()
        info.unitsPerEm = 2000
        self.assertEqual(
            info.unitsPerEm,
            2000
        )

    def test_set_valid_unitsPerEm_float(self):
        info = self.getInfo_generic()
        info.unitsPerEm = 2000.1
        self.assertEqual(
            info.unitsPerEm,
            2000.1
        )

    def test_set_invalid_unitsPerEm_negative(self):
        info = self.getInfo_generic()
        with self.assertRaises(ValueError):
            info.unitsPerEm = -1000

    def test_set_invalid_unitsPerEm_string(self):
        info = self.getInfo_generic()
        with self.assertRaises(ValueError):
            info.unitsPerEm = "abc"

    # ----
    # Hash
    # ----

    def test_hash(self):
        info = self.getInfo_generic()
        self.assertEqual(
            isinstance(info, collections.Hashable),
            True
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        info_one = self.getInfo_generic()
        self.assertEqual(
            info_one,
            info_one
        )

    def test_object_not_equal_other(self):
        info_one = self.getInfo_generic()
        info_two = self.getInfo_generic()
        self.assertNotEqual(
            info_one,
            info_two
        )

    def test_object_equal_self_variable_assignment(self):
        info_one = self.getInfo_generic()
        a = info_one
        self.assertEqual(
            info_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        info_one = self.getInfo_generic()
        info_two = self.getInfo_generic()
        a = info_one
        self.assertNotEqual(
            info_two,
            a
        )

    # -----
    # Round
    # -----

    def test_round_unitsPerEm(self):
        info = self.getInfo_generic()
        info.unitsPerEm = 2000.125
        info.round()
        self.assertEqual(
            info.unitsPerEm,
            2000
        )

    # -------------
    # Interpolation
    # -------------

    def test_interpolate_unitsPerEm_without_rounding(self):
        interpolated_font, _ = self.objectGenerator("font")
        font_min, _ = self.objectGenerator("font")
        font_max, _ = self.objectGenerator("font")
        font_min.info.unitsPerEm = 1000
        font_max.info.unitsPerEm = 2000
        interpolated_font.info.interpolate(0.5154, font_min.info, font_max.info, round=False)
        self.assertEqual(
            interpolated_font.info.unitsPerEm,
            1515.4
        )

    def test_interpolate_unitsPerEm_with_rounding(self):
        interpolated_font, _ = self.objectGenerator("font")
        font_min, _ = self.objectGenerator("font")
        font_max, _ = self.objectGenerator("font")
        font_min.info.unitsPerEm = 1000
        font_max.info.unitsPerEm = 2000
        interpolated_font.info.interpolate(0.5154, font_min.info, font_max.info, round=True)
        self.assertEqual(
            interpolated_font.info.unitsPerEm,
            1515
        )

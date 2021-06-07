import unittest
import collections
from fontParts.base import FontPartsError


class TestGuideline(unittest.TestCase):

    def getGuideline_generic(self):
        guideline, _ = self.objectGenerator("guideline")
        guideline.x = 1
        guideline.y = 2
        guideline.angle = 90
        guideline.name = "Test Guideline"
        return guideline

    def getGuideline_fontGuideline(self):
        font, _ = self.objectGenerator("font")
        guideline = font.appendGuideline((1, 2), 90, "Test Guideline Font")
        return guideline

    def getGuideline_glyphGuideline(self):
        font, _ = self.objectGenerator("font")
        layer = font.newLayer("L")
        glyph = layer.newGlyph("X")
        guideline = glyph.appendGuideline((1, 2), 90, "Test Guideline Glyph")
        return guideline

    # ----
    # repr
    # ----

    def test_reprContents(self):
        guideline = self.getGuideline_generic()
        value = guideline._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noGlyph(self):
        guideline, _ = self.objectGenerator("guideline")
        value = guideline._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_Layer(self):
        guideline = self.getGuideline_glyphGuideline()
        value = guideline._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    # --------
    # Attributes
    # --------

    # x

    def test_x_get_generic(self):
        guideline = self.getGuideline_generic()
        self.assertEqual(
            guideline.x,
            1
        )

    def test_x_get_fontGuideline(self):
        guideline = self.getGuideline_fontGuideline()
        self.assertEqual(
            guideline.x,
            1
        )

    def test_x_get_glyphGuideline(self):
        guideline = self.getGuideline_glyphGuideline()
        self.assertEqual(
            guideline.x,
            1
        )

    def test_x_set_valid_zero_generic(self):
        guideline = self.getGuideline_generic()
        guideline.x = 0
        self.assertEqual(
            guideline.x,
            0
        )

    def test_x_set_valid_zero_fontGuideline(self):
        guideline = self.getGuideline_fontGuideline()
        guideline.x = 0
        self.assertEqual(
            guideline.x,
            0
        )

    def test_x_set_valid_zero_glyphGuideline(self):
        guideline = self.getGuideline_glyphGuideline()
        guideline.x = 0
        self.assertEqual(
            guideline.x,
            0
        )

    def test_x_set_valid_positive(self):
        guideline = self.getGuideline_generic()
        guideline.x = 1
        self.assertEqual(
            guideline.x,
            1
        )

    def test_x_set_valid_negative(self):
        guideline = self.getGuideline_generic()
        guideline.x = -1
        self.assertEqual(
            guideline.x,
            -1
        )

    def test_x_set_valid_positive_float(self):
        guideline = self.getGuideline_generic()
        guideline.x = 1.1
        self.assertEqual(
            guideline.x,
            1.1
        )

    def test_x_set_valid_negative_float(self):
        guideline = self.getGuideline_generic()
        guideline.x = -1.1
        self.assertEqual(
            guideline.x,
            -1.1
        )

    def test_x_set_valid_None(self):
        guideline = self.getGuideline_generic()
        guideline.x = None
        self.assertEqual(
            guideline.x,
            0
        )

    def test_x_set_invalid_string(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(TypeError):
            guideline.x = "ABC"

    # y

    def test_y_get_generic(self):
        guideline = self.getGuideline_generic()
        self.assertEqual(
            guideline.y,
            2
        )

    def test_y_get_fontGuideline(self):
        guideline = self.getGuideline_fontGuideline()
        self.assertEqual(
            guideline.y,
            2
        )

    def test_y_get_glyphGuideline(self):
        guideline = self.getGuideline_glyphGuideline()
        self.assertEqual(
            guideline.y,
            2
        )

    def test_y_set_valid_zero_generic(self):
        guideline = self.getGuideline_generic()
        guideline.y = 0
        self.assertEqual(
            guideline.y,
            0
        )

    def test_y_set_valid_zero_fontGuideline(self):
        guideline = self.getGuideline_fontGuideline()
        guideline.y = 0
        self.assertEqual(
            guideline.y,
            0
        )

    def test_y_set_valid_zero_glyphGuideline(self):
        guideline = self.getGuideline_glyphGuideline()
        guideline.y = 0
        self.assertEqual(
            guideline.y,
            0
        )

    def test_y_set_valid_positive(self):
        guideline = self.getGuideline_generic()
        guideline.y = 1
        self.assertEqual(
            guideline.y,
            1
        )

    def test_y_set_valid_negative(self):
        guideline = self.getGuideline_generic()
        guideline.y = -1
        self.assertEqual(
            guideline.y,
            -1
        )

    def test_y_set_valid_positive_float(self):
        guideline = self.getGuideline_generic()
        guideline.y = 1.1
        self.assertEqual(
            guideline.y,
            1.1
        )

    def test_y_set_valid_negative_float(self):
        guideline = self.getGuideline_generic()
        guideline.y = -1.1
        self.assertEqual(
            guideline.y,
            -1.1
        )

    def test_y_set_valid_None(self):
        guideline = self.getGuideline_generic()
        guideline.y = None
        self.assertEqual(
            guideline.y,
            0
        )

    def test_y_set_invalid_string(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(TypeError):
            guideline.y = "ABC"

    # angle

    def test_angle_get_generic(self):
        guideline = self.getGuideline_generic()
        self.assertEqual(
            guideline.angle,
            90
        )

    def test_angle_get_fontGuideline(self):
        guideline = self.getGuideline_fontGuideline()
        self.assertEqual(
            guideline.angle,
            90
        )

    def test_angle_get_glyphGuideline(self):
        guideline = self.getGuideline_glyphGuideline()
        self.assertEqual(
            guideline.angle,
            90
        )

    def test_angle_set_valid_zero_generic(self):
        guideline = self.getGuideline_generic()
        guideline.angle = 0
        self.assertEqual(
            guideline.angle,
            0
        )

    def test_angle_set_valid_zero_fontGuideline(self):
        guideline = self.getGuideline_fontGuideline()
        guideline.angle = 0
        self.assertEqual(
            guideline.angle,
            0
        )

    def test_angle_set_valid_zero_glyphGuideline(self):
        guideline = self.getGuideline_glyphGuideline()
        guideline.angle = 0
        self.assertEqual(
            guideline.angle,
            0
        )

    def test_angle_set_valid_positive(self):
        guideline = self.getGuideline_generic()
        guideline.angle = 10
        self.assertEqual(
            guideline.angle,
            10
        )

    def test_angle_set_valid_negative(self):
        guideline = self.getGuideline_generic()
        guideline.angle = -10
        self.assertEqual(
            guideline.angle,
            350
        )

    def test_angle_set_valid_positive_float(self):
        guideline = self.getGuideline_generic()
        guideline.angle = 10.1
        self.assertEqual(
            guideline.angle,
            10.1
        )

    def test_angle_set_valid_negative_float(self):
        guideline = self.getGuideline_generic()
        guideline.angle = -10.1
        self.assertEqual(
            guideline.angle,
            349.9
        )

    def test_angle_set_valid_positive_edge(self):
        guideline = self.getGuideline_generic()
        guideline.angle = 360
        self.assertEqual(
            guideline.angle,
            360
        )

    def test_angle_set_valid_negative_edge(self):
        guideline = self.getGuideline_generic()
        guideline.angle = -360
        self.assertEqual(
            guideline.angle,
            0
        )

    def test_angle_set_valid_None(self):
        guideline = self.getGuideline_generic()
        guideline.angle = None
        self.assertEqual(
            guideline.angle,
            0
        )

    def test_angle_set_invalid_positive_edge(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(ValueError):
            guideline.angle = 361

    def test_angle_set_invalid_negative_edge(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(ValueError):
            guideline.angle = -361

    def test_angle_set_invalid_string(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(TypeError):
            guideline.angle = "ABC"

    def test_angle_set_valid_none_x0_y0(self):
        guideline = self.getGuideline_generic()
        guideline.x = 0
        guideline.y = 0
        guideline.angle = None
        self.assertEqual(
            guideline.angle,
            0
        )

    def test_angle_set_valid_none_x1_y0(self):
        guideline = self.getGuideline_generic()
        guideline.x = 1
        guideline.y = 0
        guideline.angle = None
        self.assertEqual(
            guideline.angle,
            90
        )

    def test_angle_set_valid_none_x0_y1(self):
        guideline = self.getGuideline_generic()
        guideline.x = 0
        guideline.y = 1
        guideline.angle = None
        self.assertEqual(
            guideline.angle,
            0
        )

    def test_angle_set_valid_none_x1_y1(self):
        guideline = self.getGuideline_generic()
        guideline.x = 1
        guideline.y = 1
        guideline.angle = None
        self.assertEqual(
            guideline.angle,
            0
        )

    # index

    def getGuideline_index(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph.appendGuideline((0, 0), 90, "guideline 0")
        glyph.appendGuideline((0, 0), 90, "guideline 1")
        glyph.appendGuideline((0, 0), 90, "guideline 2")
        return glyph

    def test_get_index_noParent(self):
        guideline, _ = self.objectGenerator("guideline")
        self.assertIsNone(guideline.index)

    def test_get_index(self):
        glyph = self.getGuideline_index()
        for i, guideline in enumerate(glyph.guidelines):
            self.assertEqual(guideline.index, i)

    def test_set_index_noParent(self):
        guideline, _ = self.objectGenerator("guideline")
        with self.assertRaises(FontPartsError):
            guideline.index = 1

    def test_set_index_positive(self):
        glyph = self.getGuideline_index()
        guideline = glyph.guidelines[0]
        with self.assertRaises(FontPartsError):
            guideline.index = 2

    def test_set_index_negative(self):
        glyph = self.getGuideline_index()
        guideline = glyph.guidelines[1]
        with self.assertRaises(FontPartsError):
            guideline.index = -1

    # name

    def test_name_get_none(self):
        guideline, _ = self.objectGenerator("guideline")
        self.assertIsNone(guideline.name)

    def test_name_set_valid(self):
        guideline = self.getGuideline_generic()
        guideline.name = u"foo"
        self.assertEqual(guideline.name, u"foo")

    def test_name_set_none(self):
        guideline = self.getGuideline_generic()
        guideline.name = None
        self.assertIsNone(guideline.name)

    def test_name_set_invalid(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(TypeError):
            guideline.name = 123

    # color

    def test_color_get_none(self):
        guideline = self.getGuideline_generic()
        self.assertIsNone(guideline.color)

    def test_color_set_valid_max(self):
        guideline = self.getGuideline_generic()
        guideline.color = (1, 1, 1, 1)
        self.assertEqual(guideline.color, (1, 1, 1, 1))

    def test_color_set_valid_min(self):
        guideline = self.getGuideline_generic()
        guideline.color = (0, 0, 0, 0)
        self.assertEqual(guideline.color, (0, 0, 0, 0))

    def test_color_set_valid_decimal(self):
        guideline = self.getGuideline_generic()
        guideline.color = (0.1, 0.2, 0.3, 0.4)
        self.assertEqual(guideline.color, (0.1, 0.2, 0.3, 0.4))

    def test_color_set_none(self):
        guideline = self.getGuideline_generic()
        guideline.color = None
        self.assertIsNone(guideline.color)

    def test_color_set_invalid_over_max(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(ValueError):
            guideline.color = (1.1, 0.2, 0.3, 0.4)

    def test_color_set_invalid_uner_min(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(ValueError):
            guideline.color = (-0.1, 0.2, 0.3, 0.4)

    def test_color_set_invalid_too_few(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(ValueError):
            guideline.color = (0.1, 0.2, 0.3)

    def test_color_set_invalid_string(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(TypeError):
            guideline.color = "0.1,0.2,0.3,0.4"

    def test_color_set_invalid_int(self):
        guideline = self.getGuideline_generic()
        with self.assertRaises(TypeError):
            guideline.color = 123

    # identifier

    def test_identifier_get_none(self):
        guideline = self.getGuideline_generic()
        self.assertIsNone(guideline.identifier)

    def test_identifier_generated_type(self):
        guideline = self.getGuideline_generic()
        guideline.getIdentifier()
        self.assertIsInstance(guideline.identifier, str)

    def test_identifier_consistency(self):
        guideline = self.getGuideline_generic()
        guideline.getIdentifier()
        # get: twice to test consistency
        self.assertEqual(guideline.identifier, guideline.identifier)

    def test_identifier_cannot_set(self):
        # identifier is a read-only property
        guideline = self.getGuideline_generic()
        with self.assertRaises(FontPartsError):
            guideline.identifier = "ABC"

    def test_identifier_force_set(self):
        identifier = "ABC"
        guideline = self.getGuideline_generic()
        guideline._setIdentifier(identifier)
        self.assertEqual(guideline.identifier, identifier)

    # -------
    # Methods
    # -------

    def getGuideline_copy(self):
        guideline = self.getGuideline_generic()
        guideline.name = "foo"
        guideline.color = (0.1, 0.2, 0.3, 0.4)
        return guideline

    # copy

    def test_copy_seperate_objects(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        self.assertIsNot(guideline, copied)

    def test_copy_same_name(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        self.assertEqual(guideline.name, copied.name)

    def test_copy_same_color(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        self.assertEqual(guideline.color, copied.color)

    def test_copy_same_identifier(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        self.assertEqual(guideline.identifier, copied.identifier)

    def test_copy_generated_identifier_different(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        guideline.getIdentifier()
        copied.getIdentifier()
        self.assertNotEqual(guideline.identifier, copied.identifier)

    def test_copy_same_x(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        self.assertEqual(guideline.x, copied.x)

    def test_copy_same_y(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        self.assertEqual(guideline.y, copied.y)

    def test_copy_same_angle(self):
        guideline = self.getGuideline_copy()
        copied = guideline.copy()
        self.assertEqual(guideline.angle, copied.angle)

    # transform

    def getGuideline_transform(self):
        guideline = self.getGuideline_generic()
        guideline.angle = 45.0
        return guideline

    def test_transformBy_valid_no_origin(self):
        guideline = self.getGuideline_transform()
        guideline.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(guideline.x, -1)
        self.assertEqual(guideline.y, 8)
        self.assertAlmostEqual(guideline.angle, 56.310, places=3)

    def test_transformBy_valid_origin(self):
        guideline = self.getGuideline_transform()
        guideline.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(guideline.x, 1)
        self.assertEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 45.000, places=3)

    def test_transformBy_invalid_one_string_value(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.transformBy((1, 0, 0, 1, 0, "0"))

    def test_transformBy_invalid_all_string_values(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.transformBy("1, 0, 0, 1, 0, 0")

    def test_transformBy_invalid_int_value(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.transformBy(123)

    # moveBy

    def test_moveBy_valid(self):
        guideline = self.getGuideline_transform()
        guideline.moveBy((-1, 2))
        self.assertEqual(guideline.x, 0)
        self.assertEqual(guideline.y, 4)
        self.assertAlmostEqual(guideline.angle, 45.000, places=3)

    def test_moveBy_invalid_one_string_value(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.moveBy((-1, "2"))

    def test_moveBy_invalid_all_strings_value(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.moveBy("-1, 2")

    def test_moveBy_invalid_int_value(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.moveBy(1)

    # scaleBy

    def test_scaleBy_valid_one_value_no_origin(self):
        guideline = self.getGuideline_transform()
        guideline.scaleBy((-2))
        self.assertEqual(guideline.x, -2)
        self.assertEqual(guideline.y, -4)
        self.assertAlmostEqual(guideline.angle, 225.000, places=3)

    def test_scaleBy_valid_two_values_no_origin(self):
        guideline = self.getGuideline_transform()
        guideline.scaleBy((-2, 3))
        self.assertEqual(guideline.x, -2)
        self.assertEqual(guideline.y, 6)
        self.assertAlmostEqual(guideline.angle, 123.690, places=3)

    def test_scaleBy_valid_two_values_origin(self):
        guideline = self.getGuideline_transform()
        guideline.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(guideline.x, 1)
        self.assertEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 123.690, places=3)

    def test_scaleBy_invalid_one_string_value(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.scaleBy((-1, "2"))

    def test_scaleBy_invalid_two_string_values(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.scaleBy("-1, 2")

    def test_scaleBy_invalid_tuple_too_many_values(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(ValueError):
            guideline.scaleBy((-1, 2, -3))

    # rotateBy

    def test_rotateBy_valid_no_origin(self):
        guideline = self.getGuideline_transform()
        guideline.rotateBy(45)
        self.assertAlmostEqual(guideline.x, -0.707, places=3)
        self.assertAlmostEqual(guideline.y, 2.121, places=3)
        self.assertAlmostEqual(guideline.angle, 0.000, places=3)

    def test_rotateBy_valid_origin(self):
        guideline = self.getGuideline_transform()
        guideline.rotateBy(45, origin=(1, 2))
        self.assertAlmostEqual(guideline.x, 1)
        self.assertAlmostEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 0.000, places=3)

    def test_rotateBy_invalid_string_value(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(TypeError):
            guideline.rotateBy("45")

    def test_rotateBy_invalid_too_large_value_positive(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(ValueError):
            guideline.rotateBy(361)

    def test_rotateBy_invalid_too_large_value_negative(self):
        guideline = self.getGuideline_transform()
        with self.assertRaises(ValueError):
            guideline.rotateBy(-361)

    # skewBy

    def test_skewBy_valid_no_origin_one_value(self):
        guideline = self.getGuideline_transform()
        guideline.skewBy(100)
        self.assertAlmostEqual(guideline.x, -10.343, places=3)
        self.assertEqual(guideline.y, 2.0)
        self.assertAlmostEqual(guideline.angle, 8.525, places=3)

    def test_skewBy_valid_no_origin_two_values(self):
        guideline = self.getGuideline_transform()
        guideline.skewBy((100, 200))
        self.assertAlmostEqual(guideline.x, -10.343, places=3)
        self.assertAlmostEqual(guideline.y, 2.364, places=3)
        self.assertAlmostEqual(guideline.angle, 5.446, places=3)

    def test_skewBy_valid_origin_one_value(self):
        guideline = self.getGuideline_transform()
        guideline.skewBy(100, origin=(1, 2))
        self.assertEqual(guideline.x, 1)
        self.assertEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 8.525, places=3)

    def test_skewBy_valid_origin_two_values(self):
        guideline = self.getGuideline_transform()
        guideline.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(guideline.x, 1)
        self.assertEqual(guideline.y, 2)
        self.assertAlmostEqual(guideline.angle, 5.446, places=3)

    # -------------
    # Normalization
    # -------------

    # round

    def getGuideline_round(self):
        guideline = self.getGuideline_generic()
        guideline.x = 1.1
        guideline.y = 2.5
        guideline.angle = 45.5
        return guideline

    def test_round_close_to(self):
        guideline = self.getGuideline_round()
        guideline.round()
        self.assertEqual(guideline.x, 1)

    def test_round_at_half(self):
        guideline = self.getGuideline_round()
        guideline.round()
        self.assertEqual(guideline.y, 3)

    def test_round_angle(self):
        guideline = self.getGuideline_round()
        guideline.round()
        self.assertEqual(guideline.angle, 45.5)

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        guideline_one = self.getGuideline_generic()
        self.assertEqual(
            hash(guideline_one),
            hash(guideline_one)
        )

    def test_hash_object_other(self):
        guideline_one = self.getGuideline_generic()
        guideline_two = self.getGuideline_generic()
        self.assertNotEqual(
            hash(guideline_one),
            hash(guideline_two)
        )

    def test_hash_object_self_variable_assignment(self):
        guideline_one = self.getGuideline_generic()
        a = guideline_one
        self.assertEqual(
            hash(guideline_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        guideline_one = self.getGuideline_generic()
        guideline_two = self.getGuideline_generic()
        a = guideline_one
        self.assertNotEqual(
            hash(guideline_two),
            hash(a)
        )

    def test_is_hashable(self):
        guideline_one = self.getGuideline_generic()
        self.assertTrue(
            isinstance(guideline_one, collections.Hashable)
        )

    # -------
    # Parents
    # -------

    def test_get_parent_font(self):
        font, _ = self.objectGenerator("font")
        layer = font.newLayer("L")
        glyph = layer.newGlyph("X")
        guideline = glyph.appendGuideline((0, 0), 90, "Test Guideline")
        self.assertIsNotNone(guideline.font)
        self.assertEqual(
            guideline.font,
            font
        )

    def test_get_parent_noFont(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        guideline = glyph.appendGuideline((0, 0), 90, "Test Guideline")
        self.assertIsNone(guideline.font)

    def test_get_parent_layer(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        guideline = glyph.appendGuideline((0, 0), 90, "Test Guideline")
        self.assertIsNotNone(guideline.layer)
        self.assertEqual(
            guideline.layer,
            layer
        )

    def test_get_parent_noLayer(self):
        glyph, _ = self.objectGenerator("glyph")
        guideline = glyph.appendGuideline((0, 0), 90, "Test Guideline")
        self.assertIsNone(guideline.font)
        self.assertIsNone(guideline.layer)

    def test_get_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        guideline = glyph.appendGuideline((0, 0), 90, "Test Guideline")
        self.assertIsNotNone(guideline.glyph)
        self.assertEqual(
            guideline.glyph,
            glyph
        )

    def test_get_parent_noGlyph(self):
        guideline, _ = self.objectGenerator("guideline")
        self.assertIsNone(guideline.font)
        self.assertIsNone(guideline.layer)
        self.assertIsNone(guideline.glyph)

    def test_set_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        guideline = self.getGuideline_generic()
        guideline.glyph = glyph
        self.assertIsNotNone(guideline.glyph)
        self.assertEqual(
            guideline.glyph,
            glyph
        )

    def test_set_parent_glyph_none(self):
        guideline, _ = self.objectGenerator("guideline")
        guideline.glyph = None
        self.assertIsNone(guideline.glyph)

    def test_set_parent_font_none(self):
        guideline, _ = self.objectGenerator("guideline")
        guideline.font = None
        self.assertIsNone(guideline.glyph)

    def test_set_parent_glyph_exists(self):
        glyph, _ = self.objectGenerator("glyph")
        otherGlyph, _ = self.objectGenerator("glyph")
        guideline = glyph.appendGuideline((0, 0), 90, "Test Guideline")
        with self.assertRaises(AssertionError):
            guideline.glyph = otherGlyph

    def test_set_parent_glyph_font_exists(self):
        guideline = self.getGuideline_fontGuideline()
        glyph, _ = self.objectGenerator("glyph")
        with self.assertRaises(AssertionError):
            guideline.glyph = glyph

    def test_set_parent_font_font_exists(self):
        guideline = self.getGuideline_fontGuideline()
        font, _ = self.objectGenerator("font")
        with self.assertRaises(AssertionError):
            guideline.font = font

    def test_set_parent_font_glyph_exists(self):
        guideline = self.getGuideline_glyphGuideline()
        font, _ = self.objectGenerator("font")
        with self.assertRaises(AssertionError):
            guideline.font = font

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        guideline_one = self.getGuideline_generic()
        self.assertEqual(
            guideline_one,
            guideline_one
        )

    def test_object_not_equal_other(self):
        guideline_one = self.getGuideline_generic()
        guideline_two = self.getGuideline_generic()
        self.assertNotEqual(
            guideline_one,
            guideline_two
        )

    def test_object_equal_self_variable_assignment(self):
        guideline_one = self.getGuideline_generic()
        a = guideline_one
        a.x = 200
        self.assertEqual(
            guideline_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        guideline_one = self.getGuideline_generic()
        guideline_two = self.getGuideline_generic()
        a = guideline_one
        self.assertNotEqual(
            guideline_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        guideline = self.getGuideline_generic()
        try:
            guideline.selected = False
        except NotImplementedError:
            return
        guideline.selected = True
        self.assertEqual(
            guideline.selected,
            True
        )

    def test_not_selected_false(self):
        guideline = self.getGuideline_generic()
        try:
            guideline.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            guideline.selected,
            False
        )

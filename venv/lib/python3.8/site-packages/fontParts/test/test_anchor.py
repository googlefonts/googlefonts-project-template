import unittest
import collections
from fontParts.base import FontPartsError


class TestAnchor(unittest.TestCase):

    def getAnchor_generic(self):
        anchor, _ = self.objectGenerator("anchor")
        anchor.name = "Anchor Attribute Test"
        anchor.x = 1
        anchor.y = 2
        anchor.color = None
        return anchor

    # ----
    # repr
    # ----

    def test_reprContents(self):
        anchor = self.getAnchor_generic()
        value = anchor._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noGlyph(self):
        anchor, _ = self.objectGenerator("anchor")
        value = anchor._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_color(self):
        anchor = self.getAnchor_generic()
        anchor.color = (1, 0, 1, 1)
        value = anchor._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noGlyph_color(self):
        anchor, _ = self.objectGenerator("anchor")
        anchor.color = (1, 0, 1, 1)
        value = anchor._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    # ----------
    # Attributes
    # ----------

    # Name

    def test_get(self):
        anchor = self.getAnchor_generic()
        self.assertEqual(anchor.name, "Anchor Attribute Test")

    def test_set_valid(self):
        anchor = self.getAnchor_generic()
        anchor.name = u"foo"
        self.assertEqual(anchor.name, u"foo")

    def test_set_none(self):
        anchor = self.getAnchor_generic()
        anchor.name = None
        self.assertIsNone(anchor.name)

    def test_set_invalid(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.name = 123

    # Color

    def test_color_get_none(self):
        anchor = self.getAnchor_generic()
        self.assertIsNone(anchor.color)

    def test_color_set_valid_max(self):
        anchor = self.getAnchor_generic()
        anchor.color = (1, 1, 1, 1)
        self.assertEqual(anchor.color, (1, 1, 1, 1))

    def test_color_set_valid_min(self):
        anchor = self.getAnchor_generic()
        anchor.color = (0, 0, 0, 0)
        self.assertEqual(anchor.color, (0, 0, 0, 0))

    def test_color_set_valid_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.color = (0.1, 0.2, 0.3, 0.4)
        self.assertEqual(anchor.color, (0.1, 0.2, 0.3, 0.4))

    def test_color_set_none(self):
        anchor = self.getAnchor_generic()
        anchor.color = None
        self.assertIsNone(anchor.color)

    def test_color_set_invalid_over_max(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(ValueError):
            anchor.color = (1.1, 0.2, 0.3, 0.4)

    def test_color_set_invalid_uner_min(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(ValueError):
            anchor.color = (-0.1, 0.2, 0.3, 0.4)

    def test_color_set_invalid_too_few(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(ValueError):
            anchor.color = (0.1, 0.2, 0.3)

    def test_color_set_invalid_string(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.color = "0.1,0.2,0.3,0.4"

    def test_color_set_invalid_int(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.color = 123

    # Identifier

    def test_identifier_get_none(self):
        anchor = self.getAnchor_generic()
        self.assertIsNone(anchor.identifier)

    def test_identifier_generated_type(self):
        anchor = self.getAnchor_generic()
        anchor.getIdentifier()
        self.assertIsInstance(anchor.identifier, str)

    def test_identifier_consistency(self):
        anchor = self.getAnchor_generic()
        anchor.getIdentifier()
        # get: twice to test consistency
        self.assertEqual(anchor.identifier, anchor.identifier)

    def test_identifier_cannot_set(self):
        # identifier is a read-only property
        anchor = self.getAnchor_generic()
        with self.assertRaises(FontPartsError):
            anchor.identifier = "ABC"

    def test_identifier_force_set(self):
        identifier = "ABC"
        anchor = self.getAnchor_generic()
        anchor._setIdentifier(identifier)
        self.assertEqual(anchor.identifier, identifier)

    # Index

    def getAnchor_index(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph.appendAnchor("anchor 0", (0, 0))
        glyph.appendAnchor("anchor 1", (0, 0))
        glyph.appendAnchor("anchor 2", (0, 0))
        return glyph

    def test_get_index_noParent(self):
        anchor, _ = self.objectGenerator("anchor")
        self.assertIsNone(anchor.index)

    def test_get_index(self):
        glyph = self.getAnchor_index()
        for i, anchor in enumerate(glyph.anchors):
            self.assertEqual(anchor.index, i)

    def test_set_index_noParent(self):
        anchor, _ = self.objectGenerator("anchor")
        with self.assertRaises(FontPartsError):
            anchor.index = 1

    def test_set_index_positive(self):
        glyph = self.getAnchor_index()
        anchor = glyph.anchors[0]
        with self.assertRaises(FontPartsError):
            anchor.index = 2

    def test_set_index_negative(self):
        glyph = self.getAnchor_index()
        anchor = glyph.anchors[1]
        with self.assertRaises(FontPartsError):
            anchor.index = -1

    # x

    def test_x_get(self):
        anchor = self.getAnchor_generic()
        self.assertEqual(anchor.x, 1)

    def test_x_set_valid_positive(self):
        anchor = self.getAnchor_generic()
        anchor.x = 100
        self.assertEqual(anchor.x, 100)

    def test_x_set_valid_negative(self):
        anchor = self.getAnchor_generic()
        anchor.x = -100
        self.assertEqual(anchor.x, -100)

    def test_x_set_valid_zero(self):
        anchor = self.getAnchor_generic()
        anchor.x = 0
        self.assertEqual(anchor.x, 0)

    def test_x_set_valid_positive_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.x = 1.1
        self.assertEqual(anchor.x, 1.1)

    def test_x_set_valid_negative_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.x = -1.1
        self.assertEqual(anchor.x, -1.1)

    def test_x_set_invalid_none(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.x = None

    def test_x_set_valid_string(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.x = "ABC"

    # y

    def test_y_get(self):
        anchor = self.getAnchor_generic()
        self.assertEqual(anchor.y, 2)

    def test_y_set_valid_positive(self):
        anchor = self.getAnchor_generic()
        anchor.y = 100
        self.assertEqual(anchor.y, 100)

    def test_y_set_valid_negative(self):
        anchor = self.getAnchor_generic()
        anchor.y = -100
        self.assertEqual(anchor.y, -100)

    def test_y_set_valid_zero(self):
        anchor = self.getAnchor_generic()
        anchor.y = 0
        self.assertEqual(anchor.y, 0)

    def test_y_set_valid_positive_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.y = 1.1
        self.assertEqual(anchor.y, 1.1)

    def test_y_set_valid_negative_decimal(self):
        anchor = self.getAnchor_generic()
        anchor.y = -1.1
        self.assertEqual(anchor.y, -1.1)

    def test_y_set_invalid_none(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.y = None

    def test_y_set_valid_string(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.y = "ABC"

    # -------
    # Methods
    # -------

    def getAnchor_copy(self):
        anchor = self.getAnchor_generic()
        anchor.color = (0.1, 0.2, 0.3, 0.4)
        return anchor

    # copy

    def test_copy_seperate_objects(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertIsNot(anchor, copied)

    def test_copy_same_name(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.name, copied.name)

    def test_copy_same_color(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.color, copied.color)

    def test_copy_same_identifier(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.identifier, copied.identifier)

    def test_copy_generated_identifier_different(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        anchor.getIdentifier()
        copied.getIdentifier()
        self.assertNotEqual(anchor.identifier, copied.identifier)

    def test_copy_same_x(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.x, copied.x)

    def test_copy_same_y(self):
        anchor = self.getAnchor_copy()
        copied = anchor.copy()
        self.assertEqual(anchor.y, copied.y)

    # transform

    def test_transformBy_valid_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(anchor.x, -1)
        self.assertEqual(anchor.y, 8)

    def test_transformBy_valid_origin(self):
        anchor = self.getAnchor_generic()
        anchor.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)

    def test_transformBy_invalid_one_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.transformBy((1, 0, 0, 1, 0, "0"))

    def test_transformBy_invalid_all_string_values(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.transformBy("1, 0, 0, 1, 0, 0")

    def test_transformBy_invalid_int_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.transformBy(123)

    # moveBy

    def test_moveBy_valid(self):
        anchor = self.getAnchor_generic()
        anchor.moveBy((-1, 2))
        self.assertEqual(anchor.x, 0)
        self.assertEqual(anchor.y, 4)

    def test_moveBy_invalid_one_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.moveBy((-1, "2"))

    def test_moveBy_invalid_all_strings_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.moveBy("-1, 2")

    def test_moveBy_invalid_int_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.moveBy(1)

    # scaleBy

    def test_scaleBy_valid_one_value_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.scaleBy((-2))
        self.assertEqual(anchor.x, -2)
        self.assertEqual(anchor.y, -4)

    def test_scaleBy_valid_two_values_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.scaleBy((-2, 3))
        self.assertEqual(anchor.x, -2)
        self.assertEqual(anchor.y, 6)

    def test_scaleBy_valid_two_values_origin(self):
        anchor = self.getAnchor_generic()
        anchor.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)

    def test_scaleBy_invalid_one_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.scaleBy((-1, "2"))

    def test_scaleBy_invalid_two_string_values(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.scaleBy("-1, 2")

    def test_scaleBy_invalid_tuple_too_many_values(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(ValueError):
            anchor.scaleBy((-1, 2, -3))

    # rotateBy

    def test_rotateBy_valid_no_origin(self):
        anchor = self.getAnchor_generic()
        anchor.rotateBy(45)
        self.assertAlmostEqual(anchor.x, -0.707, places=3)
        self.assertAlmostEqual(anchor.y, 2.121, places=3)

    def test_rotateBy_valid_origin(self):
        anchor = self.getAnchor_generic()
        anchor.rotateBy(45, origin=(1, 2))
        self.assertAlmostEqual(anchor.x, 1)
        self.assertAlmostEqual(anchor.y, 2)

    def test_rotateBy_invalid_string_value(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(TypeError):
            anchor.rotateBy("45")

    def test_rotateBy_invalid_too_large_value_positive(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(ValueError):
            anchor.rotateBy(361)

    def test_rotateBy_invalid_too_large_value_negative(self):
        anchor = self.getAnchor_generic()
        with self.assertRaises(ValueError):
            anchor.rotateBy(-361)

    # skewBy

    def test_skewBy_valid_no_origin_one_value(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy(100)
        self.assertAlmostEqual(anchor.x, -10.343, places=3)
        self.assertEqual(anchor.y, 2.0)

    def test_skewBy_valid_no_origin_two_values(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy((100, 200))
        self.assertAlmostEqual(anchor.x, -10.343, places=3)
        self.assertAlmostEqual(anchor.y, 2.364, places=3)

    def test_skewBy_valid_origin_one_value(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy(100, origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)

    def test_skewBy_valid_origin_two_values(self):
        anchor = self.getAnchor_generic()
        anchor.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(anchor.x, 1)
        self.assertEqual(anchor.y, 2)

    # round

    def getAnchor_round(self):
        anchor = self.getAnchor_generic()
        anchor.x = 1.1
        anchor.y = 2.5
        return anchor

    def test_round_close_to(self):
        anchor = self.getAnchor_round()
        anchor.round()
        self.assertEqual(anchor.x, 1)

    def test_round_at_half(self):
        anchor = self.getAnchor_round()
        anchor.round()
        self.assertEqual(anchor.y, 3)

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        anchor_one = self.getAnchor_generic()
        self.assertEqual(
            hash(anchor_one),
            hash(anchor_one)
        )

    def test_hash_object_other(self):
        anchor_one = self.getAnchor_generic()
        anchor_two = self.getAnchor_generic()
        self.assertNotEqual(
            hash(anchor_one),
            hash(anchor_two)
        )

    def test_hash_object_self_variable_assignment(self):
        anchor_one = self.getAnchor_generic()
        a = anchor_one
        self.assertEqual(
            hash(anchor_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        anchor_one = self.getAnchor_generic()
        anchor_two = self.getAnchor_generic()
        a = anchor_one
        self.assertNotEqual(
            hash(anchor_two),
            hash(a)
        )

    def test_is_hashable(self):
        anchor_one = self.getAnchor_generic()
        self.assertTrue(
            isinstance(anchor_one, collections.Hashable)
        )

    # -------
    # Parents
    # -------

    def test_get_parent_font(self):
        font, _ = self.objectGenerator("font")
        layer = font.newLayer("L")
        glyph = layer.newGlyph("X")
        anchor = glyph.appendAnchor("anchor 0", (0, 0))
        self.assertIsNotNone(anchor.font)
        self.assertEqual(
            anchor.font,
            font
        )

    def test_get_parent_noFont(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        anchor = glyph.appendAnchor("anchor 0", (0, 0))
        self.assertIsNone(anchor.font)

    def test_get_parent_layer(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        anchor = glyph.appendAnchor("anchor 0", (0, 0))
        self.assertIsNotNone(anchor.layer)
        self.assertEqual(
            anchor.layer,
            layer
        )

    def test_get_parent_noLayer(self):
        glyph, _ = self.objectGenerator("glyph")
        anchor = glyph.appendAnchor("anchor 0", (0, 0))
        self.assertIsNone(anchor.font)
        self.assertIsNone(anchor.layer)

    def test_get_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        anchor = glyph.appendAnchor("anchor 0", (0, 0))
        self.assertIsNotNone(anchor.glyph)
        self.assertEqual(
            anchor.glyph,
            glyph
        )

    def test_get_parent_noGlyph(self):
        anchor, _ = self.objectGenerator("anchor")
        self.assertIsNone(anchor.font)
        self.assertIsNone(anchor.layer)
        self.assertIsNone(anchor.glyph)

    def test_set_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        anchor = self.getAnchor_generic()
        anchor.glyph = glyph
        self.assertIsNotNone(anchor.glyph)
        self.assertEqual(
            anchor.glyph,
            glyph
        )

    def test_set_parent_glyph_none(self):
        anchor, _ = self.objectGenerator("anchor")
        anchor.glyph = None
        self.assertIsNone(anchor.glyph)

    def test_set_parent_glyph_exists(self):
        glyph, _ = self.objectGenerator("glyph")
        otherGlyph, _ = self.objectGenerator("glyph")
        anchor = glyph.appendAnchor("anchor 0", (0, 0))
        with self.assertRaises(AssertionError):
            anchor.glyph = otherGlyph

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        anchor_one = self.getAnchor_generic()
        self.assertEqual(
            anchor_one,
            anchor_one
        )

    def test_object_not_equal_other(self):
        anchor_one = self.getAnchor_generic()
        anchor_two = self.getAnchor_generic()
        self.assertNotEqual(
            anchor_one,
            anchor_two
        )

    def test_object_equal_variable_assignment_self(self):
        anchor_one = self.getAnchor_generic()
        a = anchor_one
        a.moveBy((-1, 2))
        self.assertEqual(
            anchor_one,
            a
        )

    def test_object_not_equal_variable_assignment_other(self):
        anchor_one = self.getAnchor_generic()
        anchor_two = self.getAnchor_generic()
        a = anchor_one
        self.assertNotEqual(
            anchor_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        anchor = self.getAnchor_generic()
        try:
            anchor.selected = False
        except NotImplementedError:
            return
        anchor.selected = True
        self.assertEqual(
            anchor.selected,
            True
        )

    def test_selected_false(self):
        anchor = self.getAnchor_generic()
        try:
            anchor.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            anchor.selected,
            False
        )

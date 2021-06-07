import unittest
import collections
from fontParts.base import FontPartsError


class TestComponent(unittest.TestCase):

    def getComponent_generic(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("A")
        pen = glyph.getPen()
        pen.moveTo((0, 0))
        pen.lineTo((0, 100))
        pen.lineTo((100, 100))
        pen.lineTo((100, 0))
        pen.closePath()
        for i, point in enumerate(glyph[0].points):
            point.name = "point %d" % i
        glyph = layer.newGlyph("B")
        component = glyph.appendComponent("A")
        component.transformation = (1, 0, 0, 1, 0, 0)
        return component

    # ----
    # repr
    # ----

    def test_reprContents(self):
        component = self.getComponent_generic()
        value = component._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noGlyph(self):
        component, _ = self.objectGenerator("component")
        value = component._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    # -------
    # Parents
    # -------

    def test_get_parent_font(self):
        font, _ = self.objectGenerator("font")
        layer = font.newLayer("L")
        glyph = layer.newGlyph("X")
        component = glyph.appendComponent("A")
        self.assertIsNotNone(component.font)
        self.assertEqual(
            component.font,
            font
        )

    def test_get_parent_noFont(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        component = glyph.appendComponent("A")
        self.assertIsNone(component.font)

    def test_get_parent_layer(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        component = glyph.appendComponent("A")
        self.assertIsNotNone(component.layer)
        self.assertEqual(
            component.layer,
            layer
        )

    def test_get_parent_noLayer(self):
        glyph, _ = self.objectGenerator("glyph")
        component = glyph.appendComponent("A")
        self.assertIsNone(component.font)
        self.assertIsNone(component.layer)

    def test_get_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        component = glyph.appendComponent("A")
        self.assertIsNotNone(component.glyph)
        self.assertEqual(
            component.glyph,
            glyph
        )

    def test_get_parent_noGlyph(self):
        component, _ = self.objectGenerator("component")
        self.assertIsNone(component.font)
        self.assertIsNone(component.layer)
        self.assertIsNone(component.glyph)

    def test_set_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        component, _ = self.objectGenerator("component")
        component.glyph = glyph
        self.assertIsNotNone(component.glyph)
        self.assertEqual(
            component.glyph,
            glyph
        )

    def test_set_parent_glyph_none(self):
        component, _ = self.objectGenerator("component")
        component.glyph = None
        self.assertIsNone(component.glyph)

    def test_set_parent_glyph_exists(self):
        glyph, _ = self.objectGenerator("glyph")
        otherGlyph, _ = self.objectGenerator("glyph")
        component = glyph.appendComponent("A")
        with self.assertRaises(AssertionError):
            component.glyph = otherGlyph

    # ----------
    # Attributes
    # ----------

    # baseGlyph

    def test_baseGlyph_generic(self):
        component = self.getComponent_generic()
        self.assertEqual(
            component.baseGlyph,
            "A"
        )

    def test_baseGlyph_valid_set(self):
        component = self.getComponent_generic()
        component.baseGlyph = "B"
        self.assertEqual(
            component.baseGlyph,
            "B"
        )

    def test_baseGlyph_invalid_set_none(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.baseGlyph = None

    def test_baseGlyph_invalid_set_empty_string(self):
        component = self.getComponent_generic()
        with self.assertRaises(ValueError):
            component.baseGlyph = ""

    def test_baseGlyph_invalid_set_int(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.baseGlyph = 123

    # transformation

    def test_transformation_generic(self):
        component = self.getComponent_generic()
        self.assertEqual(
            component.transformation,
            (1, 0, 0, 1, 0, 0)
        )

    def test_transformation_valid_set_positive(self):
        component = self.getComponent_generic()
        component.transformation = (1, 2, 3, 4, 5, 6)
        self.assertEqual(
            component.transformation,
            (1, 2, 3, 4, 5, 6)
        )

    def test_transformation_valid_set_negative(self):
        component = self.getComponent_generic()
        component.transformation = (-1, -2, -3, -4, -5, -6)
        self.assertEqual(
            component.transformation,
            (-1, -2, -3, -4, -5, -6)
        )

    def test_transformation_invalid_set_member(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.transformation = (1, 0, 0, 1, 0, "0")

    def test_transformation_invalid_set_none(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.transformation = None

    # offset

    def test_offset_generic(self):
        component = self.getComponent_generic()
        self.assertEqual(
            component.offset,
            (0, 0)
        )

    def test_offset_valid_set_zero(self):
        component = self.getComponent_generic()
        component.offset = (0, 0)
        self.assertEqual(
            component.offset,
            (0, 0)
        )

    def test_offset_valid_set_positive_positive(self):
        component = self.getComponent_generic()
        component.offset = (1, 2)
        self.assertEqual(
            component.offset,
            (1, 2)
        )

    def test_offset_valid_set_negative_positive(self):
        component = self.getComponent_generic()
        component.offset = (-1, 2)
        self.assertEqual(
            component.offset,
            (-1, 2)
        )

    def test_offset_valid_set_positive_negative(self):
        component = self.getComponent_generic()
        component.offset = (1, -2)
        self.assertEqual(
            component.offset,
            (1, -2)
        )

    def test_offset_valid_set_negative_negative(self):
        component = self.getComponent_generic()
        component.offset = (-1, -2)
        self.assertEqual(
            component.offset,
            (-1, -2)
        )

    def test_offset_invalid_set_real_bogus(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.offset = (1, "2")

    def test_offset_invalid_set_bogus_real(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.offset = ("1", 2)

    def test_offset_invalid_set_int(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.offset = 1

    def test_offset_invalid_set_none(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.offset = None

    # scale

    def test_scale_generic(self):
        component = self.getComponent_generic()
        self.assertEqual(
            component.scale,
            (1, 1)
        )

    def test_scale_valid_set_zero(self):
        component = self.getComponent_generic()
        component.scale = (0, 0)
        self.assertEqual(
            component.scale,
            (0, 0)
        )

    def test_scale_valid_set_positive_positive(self):
        component = self.getComponent_generic()
        component.scale = (1, 2)
        self.assertEqual(
            component.scale,
            (1, 2)
        )

    def test_scale_valid_set_negative_positive(self):
        component = self.getComponent_generic()
        component.scale = (-1, 2)
        self.assertEqual(
            component.scale,
            (-1, 2)
        )

    def test_scale_valid_set_positive_negative(self):
        component = self.getComponent_generic()
        component.scale = (1, -2)
        self.assertEqual(
            component.scale,
            (1, -2)
        )

    def test_scale_valid_set_negative_negative(self):
        component = self.getComponent_generic()
        component.scale = (-1, -2)
        self.assertEqual(
            component.scale,
            (-1, -2)
        )

    def test_scale_invalid_set_real_bogus(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.scale = (1, "2")

    def test_scale_invalid_set_bogus_real(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.scale = ("1", 2)

    def test_scale_invalid_set_int(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.scale = 1

    def test_scale_invalid_set_none(self):
        component = self.getComponent_generic()
        with self.assertRaises(TypeError):
            component.scale = None

    # --------------
    # Identification
    # --------------

    # index

    def getComponent_index(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph.appendComponent("A")
        glyph.appendComponent("B")
        glyph.appendComponent("C")
        return glyph

    def test_get_index_noParent(self):
        component, _ = self.objectGenerator("component")
        self.assertIsNone(component.index)

    def test_get_index(self):
        glyph = self.getComponent_index()
        for i, component in enumerate(glyph.components):
            self.assertEqual(component.index, i)

    def test_set_index_noParent(self):
        component, _ = self.objectGenerator("component")
        with self.assertRaises(FontPartsError):
            component.index = 1

    def test_set_index_positive(self):
        glyph = self.getComponent_index()
        component = glyph.components[0]
        component.index = 2
        self.assertEqual(
            [c.baseGlyph for c in glyph.components],
            ["B", "A", "C"]
        )

    def test_set_index_pastLength(self):
        glyph = self.getComponent_index()
        component = glyph.components[0]
        component.index = 20
        self.assertEqual(
            [c.baseGlyph for c in glyph.components],
            ["B", "C", "A"]
        )

    def test_set_index_negative(self):
        glyph = self.getComponent_index()
        component = glyph.components[1]
        component.index = -1
        self.assertEqual(
            [c.baseGlyph for c in glyph.components],
            ["B", "A", "C"]
        )

    # identifier

    def test_identifier_get_none(self):
        component = self.getComponent_generic()
        self.assertIsNone(component.identifier)

    def test_identifier_generated_type(self):
        component = self.getComponent_generic()
        component.getIdentifier()
        self.assertIsInstance(component.identifier, str)

    def test_identifier_consistency(self):
        component = self.getComponent_generic()
        component.getIdentifier()
        # get: twice to test consistency
        self.assertEqual(component.identifier, component.identifier)

    def test_identifier_cannot_set(self):
        # identifier is a read-only property
        component = self.getComponent_generic()
        with self.assertRaises(FontPartsError):
            component.identifier = "ABC"

    # ----
    # Copy
    # ----

    def getComponent_copy(self):
        component = self.getComponent_generic()
        component.transformation = (1, 2, 3, 4, 5, 6)
        return component

    def test_copy_seperate_objects(self):
        component = self.getComponent_copy()
        copied = component.copy()
        self.assertIsNot(component, copied)

    def test_copy_same_baseGlyph(self):
        component = self.getComponent_copy()
        copied = component.copy()
        self.assertEqual(component.baseGlyph, copied.baseGlyph)

    def test_copy_same_transformation(self):
        component = self.getComponent_copy()
        copied = component.copy()
        self.assertEqual(component.transformation, copied.transformation)

    def test_copy_same_offset(self):
        component = self.getComponent_copy()
        copied = component.copy()
        self.assertEqual(component.offset, copied.offset)

    def test_copy_same_scale(self):
        component = self.getComponent_copy()
        copied = component.copy()
        self.assertEqual(component.scale, copied.scale)

    def test_copy_not_identifier(self):
        component = self.getComponent_copy()
        component.getIdentifier()
        copied = component.copy()
        self.assertNotEqual(component.identifier, copied.identifier)

    def test_copy_generated_identifier_different(self):
        component = self.getComponent_copy()
        copied = component.copy()
        component.getIdentifier()
        copied.getIdentifier()
        self.assertNotEqual(component.identifier, copied.identifier)

    # ----
    # Pens
    # ----

    # draw

    def test_draw(self):
        from fontTools.pens.recordingPen import RecordingPen
        component = self.getComponent_generic()
        component.transformation = (1, 2, 3, 4, 5, 6)
        pen = RecordingPen()
        component.draw(pen)
        expected = [('addComponent', ('A', (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)))]
        self.assertEqual(
            pen.value,
            expected
        )

    # drawPoints

    def test_drawPoints(self):
        from fontPens.recordingPointPen import RecordingPointPen
        component = self.getComponent_generic()
        component.transformation = (1, 2, 3, 4, 5, 6)
        identifier = component.getIdentifier()
        pointPen = RecordingPointPen()
        component.drawPoints(pointPen)
        expected = [('addComponent',
                    (u'A', (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)),
                    {'identifier': identifier})]
        self.assertEqual(
            pointPen.value,
            expected
        )

    def test_drawPoints_legacy(self):
        from .legacyPointPen import LegacyPointPen
        component = self.getComponent_generic()
        component.transformation = (1, 2, 3, 4, 5, 6)
        component.getIdentifier()
        pointPen = LegacyPointPen()
        component.drawPoints(pointPen)
        expected = [('addComponent', (u'A', (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)), {})]
        self.assertEqual(
            pointPen.value,
            expected
        )

    # --------------
    # Transformation
    # --------------

    def getComponent_transform(self):
        component = self.getComponent_generic()
        component.transformation = (1, 2, 3, 4, 5, 6)
        return component

    # transformBy

    def test_transformBy_valid_no_origin(self):
        component = self.getComponent_transform()
        component.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(
            component.transformation,
            (2.0, 6.0, 6.0, 12.0, 7.0, 20.0)
        )

    def test_transformBy_valid_origin(self):
        component = self.getComponent_transform()
        component.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(
            component.transformation,
            (2.0, 4.0, 6.0, 8.0, 9.0, 10.0)
        )

    def test_transformBy_invalid_one_string_value(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.transformBy((1, 0, 0, 1, 0, "0"))

    def test_transformBy_invalid_all_string_values(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.transformBy("1, 0, 0, 1, 0, 0")

    def test_transformBy_invalid_int_value(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.transformBy(123)

    # moveBy

    def test_moveBy_valid(self):
        component = self.getComponent_transform()
        component.moveBy((-1, 2))
        self.assertEqual(
            component.transformation,
            (1.0, 2.0, 3.0, 4.0, 4.0, 8.0)
        )

    def test_moveBy_invalid_one_string_value(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.moveBy((-1, "2"))

    def test_moveBy_invalid_all_strings_value(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.moveBy("-1, 2")

    def test_moveBy_invalid_int_value(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.moveBy(1)

    # scaleBy

    def test_scaleBy_valid_one_value_no_origin(self):
        component = self.getComponent_transform()
        component.scaleBy((-2))
        self.assertEqual(
            component.transformation,
            (-2.0, -4.0, -6.0, -8.0, -10.0, -12.0)
        )

    def test_scaleBy_valid_two_values_no_origin(self):
        component = self.getComponent_transform()
        component.scaleBy((-2, 3))
        self.assertEqual(
            component.transformation,
            (-2.0, 6.0, -6.0, 12.0, -10.0, 18.0)
        )

    def test_scaleBy_valid_two_values_origin(self):
        component = self.getComponent_transform()
        component.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(
            component.transformation,
            (-2.0, 6.0, -6.0, 12.0, -7.0, 14.0)
        )

    def test_scaleBy_invalid_one_string_value(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.scaleBy((-1, "2"))

    def test_scaleBy_invalid_two_string_values(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.scaleBy("-1, 2")

    def test_scaleBy_invalid_tuple_too_many_values(self):
        component = self.getComponent_transform()
        with self.assertRaises(ValueError):
            component.scaleBy((-1, 2, -3))

    # # rotateBy

    def test_rotateBy_valid_no_origin(self):
        component = self.getComponent_transform()
        component.rotateBy(45)
        self.assertEqual(
            [round(i, 3) for i in component.transformation],
            [-0.707, 2.121, -0.707, 4.95, -0.707, 7.778]
        )

    def test_rotateBy_valid_origin(self):
        component = self.getComponent_transform()
        component.rotateBy(45, origin=(1, 2))
        self.assertEqual(
            [round(i, 3) for i in component.transformation],
            [-0.707, 2.121, -0.707, 4.95, 1.0, 7.657]
        )

    def test_rotateBy_invalid_string_value(self):
        component = self.getComponent_transform()
        with self.assertRaises(TypeError):
            component.rotateBy("45")

    def test_rotateBy_invalid_too_large_value_positive(self):
        component = self.getComponent_transform()
        with self.assertRaises(ValueError):
            component.rotateBy(361)

    def test_rotateBy_invalid_too_large_value_negative(self):
        component = self.getComponent_transform()
        with self.assertRaises(ValueError):
            component.rotateBy(-361)

    # skewBy

    def test_skewBy_valid_no_origin_one_value(self):
        component = self.getComponent_transform()
        component.skewBy(100)
        self.assertEqual(
            [round(i, 3) for i in component.transformation],
            [-10.343, 2.0, -19.685, 4.0, -29.028, 6.0]
        )

    def test_skewBy_valid_no_origin_two_values(self):
        component = self.getComponent_transform()
        component.skewBy((100, 200))
        self.assertEqual(
            [round(i, 3) for i in component.transformation],
            [-10.343, 2.364, -19.685, 5.092, -29.028, 7.82]
        )

    def test_skewBy_valid_origin_one_value(self):
        component = self.getComponent_transform()
        component.skewBy(100, origin=(1, 2))
        self.assertEqual(
            [round(i, 3) for i in component.transformation],
            [-10.343, 2.0, -19.685, 4.0, -17.685, 6.0]
        )

    def test_skewBy_valid_origin_two_values(self):
        component = self.getComponent_transform()
        component.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(
            [round(i, 3) for i in component.transformation],
            [-10.343, 2.364, -19.685, 5.092, -17.685, 7.456]
        )

    # -------------
    # Normalization
    # -------------

    # round

    def test_round(self):
        component = self.getComponent_generic()
        component.transformation = (1.2, 2.2, 3.3, 4.4, 5.1, 6.6)
        component.round()
        self.assertEqual(
            component.transformation,
            (1.2, 2.2, 3.3, 4.4, 5, 7)
        )

    # decompose

    def test_decompose_noParent(self):
        component, _ = self.objectGenerator("component")
        with self.assertRaises(FontPartsError):
            component.decompose()

    def test_decompose_digest(self):
        from fontPens.digestPointPen import DigestPointPen
        component = self.getComponent_generic()
        glyph = component.glyph
        glyph.layer[component.baseGlyph]
        component.decompose()
        pointPen = DigestPointPen()
        glyph.drawPoints(pointPen)
        expected = (
            ('beginPath', None),
            ((0, 0), u'line', False, 'point 0'),
            ((0, 100), u'line', False, 'point 1'),
            ((100, 100), u'line', False, 'point 2'),
            ((100, 0), u'line', False, 'point 3'),
            'endPath'
        )
        self.assertEqual(
            pointPen.getDigest(),
            expected
        )

    def test_decompose_identifiers(self):
        component = self.getComponent_generic()
        glyph = component.glyph
        baseGlyph = glyph.layer[component.baseGlyph]
        baseGlyph[0].getIdentifier()
        for point in baseGlyph[0].points:
            point.getIdentifier()
        component.decompose()
        self.assertEqual(
            [point.identifier for point in glyph[0].points],
            [point.identifier for point in baseGlyph[0].points]
        )
        self.assertEqual(
            glyph[0].identifier,
            baseGlyph[0].identifier
        )

    def test_decompose_transformation(self):
        from fontPens.digestPointPen import DigestPointPen
        component = self.getComponent_generic()
        component.scale = (2, 2)
        glyph = component.glyph
        glyph.layer[component.baseGlyph]
        component.decompose()
        pointPen = DigestPointPen()
        glyph.drawPoints(pointPen)
        expected = (
            ('beginPath', None),
            ((0, 0), u'line', False, 'point 0'),
            ((0, 200), u'line', False, 'point 1'),
            ((200, 200), u'line', False, 'point 2'),
            ((200, 0), u'line', False, 'point 3'),
            'endPath'
        )
        self.assertEqual(
            pointPen.getDigest(),
            expected
        )

    # ------------
    # Data Queries
    # ------------

    # bounds

    def test_bounds_get(self):
        component = self.getComponent_generic()
        self.assertEqual(
            component.bounds,
            (0, 0, 100, 100)
        )

    def test_bounds_none(self):
        component = self.getComponent_generic()
        layer = component.layer
        baseGlyph = layer[component.baseGlyph]
        baseGlyph.clear()
        self.assertIsNone(component.bounds)

    def test_bounds_on_move(self):
        component = self.getComponent_generic()
        component.moveBy((0.1, -0.1))
        self.assertEqual(
            component.bounds,
            (0.1, -0.1, 100.1, 99.9)
        )

    def test_bounds_on_scale(self):
        component = self.getComponent_generic()
        component.scaleBy((2, 0.5))
        self.assertEqual(
            component.bounds,
            (0, 0, 200, 50)
        )

    def test_bounds_invalid_set(self):
        component = self.getComponent_generic()
        with self.assertRaises(FontPartsError):
            component.bounds = (0, 0, 100, 100)

    # pointInside

    def test_pointInside_true(self):
        component = self.getComponent_generic()
        self.assertEqual(
            component.pointInside((1, 1)),
            True
        )

    def test_pointInside_false(self):
        component = self.getComponent_generic()
        self.assertEqual(
            component.pointInside((-1, -1)),
            False
        )

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        component_one = self.getComponent_generic()
        self.assertEqual(
            hash(component_one),
            hash(component_one)
        )

    def test_hash_object_other(self):
        component_one = self.getComponent_generic()
        component_two = self.getComponent_generic()
        self.assertNotEqual(
            hash(component_one),
            hash(component_two)
        )

    def test_hash_object_self_variable_assignment(self):
        component_one = self.getComponent_generic()
        a = component_one
        self.assertEqual(
            hash(component_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        component_one = self.getComponent_generic()
        component_two = self.getComponent_generic()
        a = component_one
        self.assertNotEqual(
            hash(component_two),
            hash(a)
        )

    def test_is_hashable(self):
        component_one = self.getComponent_generic()
        self.assertTrue(
            isinstance(component_one, collections.Hashable)
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        component_one = self.getComponent_generic()
        self.assertEqual(
            component_one,
            component_one
        )

    def test_object_not_equal_other(self):
        component_one = self.getComponent_generic()
        component_two = self.getComponent_generic()
        self.assertNotEqual(
            component_one,
            component_two
        )

    def test_object_equal_assigned_variable(self):
        component_one = self.getComponent_generic()
        a = component_one
        a.baseGlyph = "C"
        self.assertEqual(
            component_one,
            a
        )

    def test_object_not_equal_assigned_variable_other(self):
        component_one = self.getComponent_generic()
        component_two = self.getComponent_generic()
        a = component_one
        self.assertNotEqual(
            component_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        component = self.getComponent_generic()
        try:
            component.selected = False
        except NotImplementedError:
            return
        component.selected = True
        self.assertEqual(
            component.selected,
            True
        )

    def test_selected_false(self):
        component = self.getComponent_generic()
        try:
            component.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            component.selected,
            False
        )

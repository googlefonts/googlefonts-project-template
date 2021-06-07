import unittest
import collections
from fontParts.base import FontPartsError


class TestPoint(unittest.TestCase):

    def getPoint_generic(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        point = contour.points[1]
        point.smooth = True
        return point

    # ----
    # repr
    # ----

    def test_reprContents(self):
        point = self.getPoint_generic()
        value = point._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_withName(self):
        point = self.getPoint_withName()
        value = point._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_isSmooth(self):
        point = self.getPoint_generic()
        point.smooth = True
        value = point._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noContour(self):
        point, _ = self.objectGenerator("point")
        value = point._reprContents()
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
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        point = contour.points[0]
        self.assertIsNotNone(point.font)
        self.assertEqual(
            point.font,
            font
        )

    def test_get_parent_noFont(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        point = contour.points[0]
        self.assertIsNone(point.font)

    def test_get_parent_layer(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        point = contour.points[0]
        self.assertIsNotNone(point.layer)
        self.assertEqual(
            point.layer,
            layer
        )

    def test_get_parent_noLayer(self):
        glyph, _ = self.objectGenerator("glyph")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        point = contour.points[0]
        self.assertIsNone(point.font)
        self.assertIsNone(point.layer)

    def test_get_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        point = contour.points[0]
        self.assertIsNotNone(point.glyph)
        self.assertEqual(
            point.glyph,
            glyph
        )

    def test_get_parent_noGlyph(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        point = contour.points[0]
        self.assertIsNone(point.glyph)

    def test_get_parent_contour(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        point = contour.points[0]
        self.assertIsNotNone(point.contour)
        self.assertEqual(
            point.contour,
            contour
        )

    def test_get_parent_noContour(self):
        point, _ = self.objectGenerator("point")
        self.assertIsNone(point.contour)

    def test_get_parent_segment(self):
        point, _ = self.objectGenerator("point")
        with self.assertRaises(AttributeError):
            point.segment

    def test_set_parent_contour(self):
        contour, _ = self.objectGenerator("contour")
        point, _ = self.objectGenerator("point")
        point.contour = contour
        self.assertIsNotNone(point.contour)
        self.assertEqual(
            point.contour,
            contour
        )

    def test_set_already_set_parent_contour(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((10, 20))
        point = contour.points[0]
        contourOther, _ = self.objectGenerator("contour")
        with self.assertRaises(AssertionError):
            point.contour = contourOther

    def test_set_parent_contour_none(self):
        point, _ = self.objectGenerator("point")
        point.contour = None
        self.assertIsNone(point.contour)

    def test_get_parent_glyph_noContour(self):
        point, _ = self.objectGenerator("point")
        self.assertIsNone(point.glyph)

    def test_get_parent_layer_noContour(self):
        point, _ = self.objectGenerator("point")
        self.assertIsNone(point.layer)

    def test_get_parent_font_noContour(self):
        point, _ = self.objectGenerator("point")
        self.assertIsNone(point.font)

    # ----------
    # Attributes
    # ----------

    # type

    def test_get_type(self):
        point = self.getPoint_generic()
        self.assertEqual(
            point.type,
            "line"
        )

    def test_set_move(self):
        point = self.getPoint_generic()
        point.type = "move"
        self.assertEqual(
            point.type,
            "move"
        )

    def test_set_curve(self):
        point = self.getPoint_generic()
        point.type = "curve"
        self.assertEqual(
            point.type,
            "curve"
        )

    def test_set_wcurve(self):
        point = self.getPoint_generic()
        point.type = "qcurve"
        self.assertEqual(
            point.type,
            "qcurve"
        )

    def test_set_offcurve(self):
        point = self.getPoint_generic()
        point.type = "offcurve"
        self.assertEqual(
            point.type,
            "offcurve"
        )

    def test_set_invalid_point_type_string(self):
        point = self.getPoint_generic()
        with self.assertRaises(ValueError):
            point.type = "xxx"

    def test_set_invalid_point_type_int(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.type = 123

    # smooth

    def test_get_smooth(self):
        point = self.getPoint_generic()
        self.assertEqual(
            point.smooth,
            True
        )

    def test_set_smooth_valid(self):
        point = self.getPoint_generic()
        point.smooth = True
        self.assertEqual(
            point.smooth,
            True
        )

    def test_set_smooth_invalid(self):
        point = self.getPoint_generic()
        with self.assertRaises(ValueError):
            point.smooth = "smooth"

    # x

    def test_get_x(self):
        point = self.getPoint_generic()
        self.assertEqual(
            point.x,
            101
        )

    def test_set_x_valid_int(self):
        point = self.getPoint_generic()
        point.x = 100
        self.assertEqual(
            point.x,
            100
        )

    def test_set_x_valid_float(self):
        point = self.getPoint_generic()
        point.x = 100.5
        self.assertEqual(
            point.x,
            100.5
        )

    def test_set_x_invalidType(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.x = "100"

    # y

    def test_get_y(self):
        point = self.getPoint_generic()
        self.assertEqual(
            point.y,
            202
        )

    def test_set_y_valid_int(self):
        point = self.getPoint_generic()
        point.y = 200
        self.assertEqual(
            point.y,
            200
        )

    def test_set_y_valid_float(self):
        point = self.getPoint_generic()
        point.y = 200.5
        self.assertEqual(
            point.y,
            200.5
        )

    def test_set_y_invalidType(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.y = "200"

    # --------------
    # Identification
    # --------------

    # index

    def getPoint_noParentContour(self):
        point, _ = self.objectGenerator("point")
        point.x = 101
        point.y = 202
        return point

    def test_get_index(self):
        point = self.getPoint_generic()
        self.assertEqual(
            point.index,
            1
        )

    def test_get_index_noParentContour(self):
        point = self.getPoint_noParentContour()
        self.assertEqual(
            point.index,
            None
        )

    def test_set_index(self):
        point = self.getPoint_generic()
        with self.assertRaises(FontPartsError):
            point.index = 0

    # name

    def getPoint_withName(self):
        point = self.getPoint_generic()
        point.name = "P"
        return point

    def test_get_name_noName(self):
        point = self.getPoint_generic()
        self.assertEqual(
            point.name,
            None
        )

    def test_get_name_hasName(self):
        point = self.getPoint_withName()
        self.assertEqual(
            point.name,
            "P"
        )

    def test_set_name_valid_str(self):
        point = self.getPoint_generic()
        point.name = "P"
        self.assertEqual(
            point.name,
            "P"
        )

    def test_set_name_valid_none(self):
        point = self.getPoint_generic()
        point.name = None
        self.assertEqual(
            point.name,
            None
        )

    def test_set_name_invalidType(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.name = 1

    # identifier

    def test_identifier_get_none(self):
        point = self.getPoint_generic()
        self.assertIsNone(point.identifier)

    def test_identifier_generated_type(self):
        point = self.getPoint_generic()
        point.getIdentifier()
        self.assertIsInstance(point.identifier, str)

    def test_identifier_consistency(self):
        point = self.getPoint_generic()
        point.getIdentifier()
        # get: twice to test consistency
        self.assertEqual(point.identifier, point.identifier)

    def test_identifier_cannot_set(self):
        # identifier is a read-only property
        point = self.getPoint_generic()
        with self.assertRaises(FontPartsError):
            point.identifier = "ABC"

    def test_getIdentifer_no_contour(self):
        point, _ = self.objectGenerator("point")
        with self.assertRaises(FontPartsError):
            point.getIdentifier()

    def test_getIdentifer_consistency(self):
        point = self.getPoint_generic()
        point.getIdentifier()
        self.assertEqual(point.identifier, point.getIdentifier())

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        point_one = self.getPoint_generic()
        self.assertEqual(
            hash(point_one),
            hash(point_one)
        )

    def test_hash_object_other(self):
        point_one = self.getPoint_generic()
        point_two = self.getPoint_generic()
        self.assertNotEqual(
            hash(point_one),
            hash(point_two)
        )

    def test_hash_object_self_variable_assignment(self):
        point_one = self.getPoint_generic()
        a = point_one
        self.assertEqual(
            hash(point_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        point_one = self.getPoint_generic()
        point_two = self.getPoint_generic()
        a = point_one
        self.assertNotEqual(
            hash(point_two),
            hash(a)
        )

    def test_is_hashable(self):
        point_one = self.getPoint_generic()
        self.assertTrue(
            isinstance(point_one, collections.Hashable)
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        point_one = self.getPoint_generic()
        self.assertEqual(
            point_one,
            point_one
        )

    def test_object_not_equal_other(self):
        point_one = self.getPoint_generic()
        point_two = self.getPoint_generic()
        self.assertNotEqual(
            point_one,
            point_two
        )

    def test_object_equal_self_variable_assignment(self):
        point_one = self.getPoint_generic()
        a = point_one
        self.assertEqual(
            point_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        point_one = self.getPoint_generic()
        point_two = self.getPoint_generic()
        a = point_one
        self.assertNotEqual(
            point_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        point = self.getPoint_generic()
        try:
            point.selected = False
        except NotImplementedError:
            return
        point.selected = True
        self.assertEqual(
            point.selected,
            True
        )

    def test_selected_false(self):
        point = self.getPoint_generic()
        try:
            point.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            point.selected,
            False
        )

    # ----
    # Copy
    # ----

    def test_copy_seperate_objects(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertIsNot(
            point,
            copied
        )

    def test_copy_different_contour(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertIsNot(
            point.contour,
            copied.contour
        )

    def test_copy_none_contour(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertEqual(
            copied.contour,
            None
        )

    def test_copy_same_type(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertEqual(
            point.type,
            copied.type
        )

    def test_copy_same_smooth(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertEqual(
            point.smooth,
            copied.smooth
        )

    def test_copy_same_x(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertEqual(
            point.x,
            copied.x
        )

    def test_copy_same_y(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertEqual(
            point.y,
            copied.y
        )

    def test_copy_same_name(self):
        point = self.getPoint_generic()
        copied = point.copy()
        self.assertEqual(
            point.name,
            copied.name
        )

    def test_copy_same_identifier_None(self):
        point = self.getPoint_generic()
        point._setIdentifier(None)
        copied = point.copy()
        self.assertEqual(
            point.identifier,
            copied.identifier,
        )

    def test_copy_different_identifier(self):
        point = self.getPoint_generic()
        point.getIdentifier()
        copied = point.copy()
        self.assertNotEqual(
            point.identifier,
            copied.identifier,
        )

    def test_copy_generated_identifier_different(self):
        otherContour, _ = self.objectGenerator("contour")
        point = self.getPoint_generic()
        copied = point.copy()
        copied.contour = otherContour
        point.getIdentifier()
        copied.getIdentifier()
        self.assertNotEqual(
            point.identifier,
            copied.identifier
        )

    def test_copyData_type(self):
        point = self.getPoint_generic()
        pointOther, _ = self.objectGenerator("point")
        pointOther.copyData(point)
        self.assertEqual(
            point.type,
            pointOther.type,
        )

    def test_copyData_smooth(self):
        point = self.getPoint_generic()
        pointOther, _ = self.objectGenerator("point")
        pointOther.copyData(point)
        self.assertEqual(
            point.smooth,
            pointOther.smooth,
        )

    def test_copyData_x(self):
        point = self.getPoint_generic()
        pointOther, _ = self.objectGenerator("point")
        pointOther.copyData(point)
        self.assertEqual(
            point.x,
            pointOther.x,
        )

    def test_copyData_y(self):
        point = self.getPoint_generic()
        pointOther, _ = self.objectGenerator("point")
        pointOther.copyData(point)
        self.assertEqual(
            point.y,
            pointOther.y,
        )

    def test_copyData_name(self):
        point = self.getPoint_generic()
        point.name = "P"
        pointOther, _ = self.objectGenerator("point")
        pointOther.copyData(point)
        self.assertEqual(
            point.name,
            pointOther.name,
        )

    def test_copyData_different_identifier(self):
        point = self.getPoint_generic()
        point.getIdentifier()
        pointOther, _ = self.objectGenerator("point")
        pointOther.copyData(point)
        self.assertNotEqual(
            point.identifier,
            pointOther.identifier,
        )

    # --------------
    # Transformation
    # --------------

    def test_transformBy_valid_no_origin(self):
        point = self.getPoint_generic()
        point.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(
            (point.x, point.y),
            (199.0, 608.0)
        )

    def test_transformBy_valid_origin(self):
        point = self.getPoint_generic()
        point.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(
            (point.x, point.y),
            (201.0, 402.0)
        )

    def test_transformBy_invalid_one_string_value(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.transformBy((1, 0, 0, 1, 0, "0"))

    def test_transformBy_invalid_all_string_values(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.transformBy("1, 0, 0, 1, 0, 0")

    def test_transformBy_invalid_int_value(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.transformBy(123)

    # moveBy

    def test_moveBy_valid(self):
        point = self.getPoint_generic()
        point.moveBy((-1, 2))
        self.assertEqual(
            (point.x, point.y),
            (100.0, 204.0)
        )

    def test_moveBy_invalid_one_string_value(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.moveBy((-1, "2"))

    def test_moveBy_invalid_all_strings_value(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.moveBy("-1, 2")

    def test_moveBy_invalid_int_value(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.moveBy(1)

    # scaleBy

    def test_scaleBy_valid_one_value_no_origin(self):
        point = self.getPoint_generic()
        point.scaleBy((-2))
        self.assertEqual(
            (point.x, point.y),
            (-202.0, -404.0)
        )

    def test_scaleBy_valid_two_values_no_origin(self):
        point = self.getPoint_generic()
        point.scaleBy((-2, 3))
        self.assertEqual(
            (point.x, point.y),
            (-202.0, 606.0)
        )

    def test_scaleBy_valid_two_values_origin(self):
        point = self.getPoint_generic()
        point.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(
            (point.x, point.y),
            (-199.0, 602.0)
        )

    def test_scaleBy_invalid_one_string_value(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.scaleBy((-1, "2"))

    def test_scaleBy_invalid_two_string_values(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.scaleBy("-1, 2")

    def test_scaleBy_invalid_tuple_too_many_values(self):
        point = self.getPoint_generic()
        with self.assertRaises(ValueError):
            point.scaleBy((-1, 2, -3))

    # rotateBy

    def test_rotateBy_valid_no_origin(self):
        point = self.getPoint_generic()
        point.rotateBy(45)
        self.assertEqual(
            [(round(point.x, 3)), (round(point.y, 3))],
            [-71.418, 214.253]
        )

    def test_rotateBy_valid_origin(self):
        point = self.getPoint_generic()
        point.rotateBy(45, origin=(1, 2))
        self.assertEqual(
            [(round(point.x, 3)), (round(point.y, 3))],
            [-69.711, 214.132]
        )

    def test_rotateBy_invalid_string_value(self):
        point = self.getPoint_generic()
        with self.assertRaises(TypeError):
            point.rotateBy("45")

    def test_rotateBy_invalid_too_large_value_positive(self):
        point = self.getPoint_generic()
        with self.assertRaises(ValueError):
            point.rotateBy(361)

    def test_rotateBy_invalid_too_large_value_negative(self):
        point = self.getPoint_generic()
        with self.assertRaises(ValueError):
            point.rotateBy(-361)

    # skewBy

    def test_skewBy_valid_no_origin_one_value(self):
        point = self.getPoint_generic()
        point.skewBy(100)
        self.assertEqual(
            [(round(point.x, 3)), (round(point.y, 3))],
            [-1044.599, 202.0]
        )

    def test_skewBy_valid_no_origin_two_values(self):
        point = self.getPoint_generic()
        point.skewBy((100, 200))
        self.assertEqual(
            [(round(point.x, 3)), (round(point.y, 3))],
            [-1044.599, 238.761]
        )

    def test_skewBy_valid_origin_one_value(self):
        point = self.getPoint_generic()
        point.skewBy(100, origin=(1, 2))
        self.assertEqual(
            [(round(point.x, 3)), (round(point.y, 3))],
            [-1033.256, 202.0]
        )

    def test_skewBy_valid_origin_two_values(self):
        point = self.getPoint_generic()
        point.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(
            [(round(point.x, 3)), (round(point.y, 3))],
            [-1033.256, 238.397]
        )

    # -------------
    # Normalization
    # -------------

    # round

    def getPoint_floatXY(self):
        point, _ = self.objectGenerator("point")
        point.x = 101.3
        point.y = 202.6
        return point

    def test_roundX(self):
        point = self.getPoint_floatXY()
        point.round()
        self.assertEqual(
            point.x,
            101
        )

    def test_roundY(self):
        point = self.getPoint_floatXY()
        point.round()
        self.assertEqual(
            point.y,
            203
        )

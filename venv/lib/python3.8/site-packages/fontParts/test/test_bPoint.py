import unittest
import collections
from fontParts.base import FontPartsError


class TestBPoint(unittest.TestCase):

    def getBPoint_corner(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        return bPoint

    def getBPoint_corner_with_bcpOut(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((133, 212), "offcurve")
        contour.appendPoint((0, 0), "offcurve")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        return bPoint

    def getBPoint_corner_with_bcpIn(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((0, 0), "offcurve")
        contour.appendPoint((61, 190), "offcurve")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        return bPoint

    def getContour(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((19, 121), "offcurve")
        contour.appendPoint((61, 190), "offcurve")
        contour.appendPoint((101, 202), "curve", smooth=True)
        contour.appendPoint((133, 212), "offcurve")
        contour.appendPoint((155, 147), "offcurve")
        contour.appendPoint((255, 147), "curve")
        return contour

    def getBPoint_curve(self):
        contour = self.getContour()
        bPoint = contour.bPoints[1]
        return bPoint

    def getBPoint_curve_firstPointOpenContour(self):
        contour = self.getContour()
        bPoint = contour.bPoints[0]
        return bPoint

    def getBPoint_curve_lastPointOpenContour(self):
        contour = self.getContour()
        bPoint = contour.bPoints[-1]
        return bPoint

    def getBPoint_withName(self):
        bPoint = self.getBPoint_corner()
        bPoint.name = "BP"
        return bPoint

    # ----
    # repr
    # ----

    def test_reprContents(self):
        bPoint = self.getBPoint_corner()
        value = bPoint._reprContents()
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
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        bPoint = contour.bPoints[1]
        self.assertIsNotNone(bPoint.font)
        self.assertEqual(
            bPoint.font,
            font
        )

    def test_get_parent_noFont(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        bPoint = contour.bPoints[1]
        self.assertIsNone(bPoint.font)

    def test_get_parent_layer(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        bPoint = contour.bPoints[1]
        self.assertIsNotNone(bPoint.layer)
        self.assertEqual(
            bPoint.layer,
            layer
        )

    def test_get_parent_noLayer(self):
        glyph, _ = self.objectGenerator("glyph")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        bPoint = contour.bPoints[1]
        self.assertIsNone(bPoint.font)
        self.assertIsNone(bPoint.layer)

    def test_get_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        glyph.appendContour(contour)
        contour = glyph.contours[0]
        bPoint = contour.bPoints[1]
        self.assertIsNotNone(bPoint.glyph)
        self.assertEqual(
            bPoint.glyph,
            glyph
        )

    def test_get_parent_noGlyph(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        self.assertIsNone(bPoint.glyph)

    def test_get_parent_contour(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        self.assertIsNotNone(bPoint.contour)
        self.assertEqual(
            bPoint.contour,
            contour
        )

    def test_get_parent_noContour(self):
        bPoint, _ = self.objectGenerator("bPoint")
        self.assertIsNone(bPoint.contour)

    def test_get_parent_segment(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        self.assertIsNotNone(bPoint._segment)

    # def test_get_parent_noSegment(self):
    #     bPoint, _ = self.objectGenerator("bPoint")
    #     self.assertIsNone(bPoint._segment)

    def test_get_parent_nextSegment(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[2]
        self.assertIsNotNone(bPoint._nextSegment)

    def test_get_parent_noNextSegment(self):
        bPoint, _ = self.objectGenerator("bPoint")
        self.assertIsNone(bPoint._nextSegment)

    # get segment/nosegment

    def test_set_parent_contour(self):
        contour, _ = self.objectGenerator("contour")
        bPoint, _ = self.objectGenerator("bPoint")
        bPoint.contour = contour
        self.assertIsNotNone(bPoint.contour)
        self.assertEqual(
            bPoint.contour,
            contour
        )

    def test_set_already_set_parent_contour(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        contour.appendPoint((303, 0), "line")
        bPoint = contour.bPoints[1]
        contourOther, _ = self.objectGenerator("contour")
        with self.assertRaises(AssertionError):
            bPoint.contour = contourOther

    def test_set_parent_contour_none(self):
        bPoint, _ = self.objectGenerator("bPoint")
        bPoint.contour = None
        self.assertIsNone(bPoint.contour)

    def test_get_parent_glyph_noContour(self):
        bPoint, _ = self.objectGenerator("bPoint")
        self.assertIsNone(bPoint.glyph)

    def test_get_parent_layer_noContour(self):
        bPoint, _ = self.objectGenerator("bPoint")
        self.assertIsNone(bPoint.layer)

    def test_get_parent_font_noContour(self):
        bPoint, _ = self.objectGenerator("bPoint")
        self.assertIsNone(bPoint.font)

    # ----
    # Attributes
    # ----

    # type

    def test_get_type_corner(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.type,
            "corner"
        )

    def test_get_type_curve(self):
        bPoint = self.getBPoint_curve()
        self.assertEqual(
            bPoint.type,
            "curve"
        )

    def test_set_type_corner(self):
        bPoint = self.getBPoint_curve()
        bPoint.type = "corner"
        self.assertEqual(
            bPoint.type,
            "corner"
        )

    def test_set_type_curve(self):
        bPoint = self.getBPoint_corner()
        bPoint.type = "curve"
        self.assertEqual(
            bPoint.type,
            "curve"
        )

    def test_type_not_equal(self):
        bPoint = self.getBPoint_corner()
        self.assertNotEqual(
            bPoint.type,
            "curve"
        )

    def test_set_bcpOutIn_type_change(self):
        bPoint = self.getBPoint_curve()
        bPoint.bcpOut = (0, 0)
        bPoint.bcpIn = (0, 0)
        self.assertEqual(
            bPoint.type,
            "corner"
        )

    def test_set_bcpInOut_type_change(self):
        bPoint = self.getBPoint_curve()
        bPoint.bcpIn = (0, 0)
        bPoint.bcpOut = (0, 0)
        self.assertEqual(
            bPoint.type,
            "corner"
        )

    # https://github.com/robotools/fontParts/issues/435
    def test_smooth_move_type_issue435(self):
        contour = self.getContour()
        contour.points[0].smooth = True
        bPoint = contour.bPoints[0]
        self.assertEqual(
            bPoint.type,
            "curve"
        )

    # anchor

    def test_get_anchor(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.anchor,
            (101, 202)
        )

    def test_set_anchor_valid_tuple(self):
        bPoint = self.getBPoint_corner()
        bPoint.anchor = (51, 45)
        self.assertEqual(
            bPoint.anchor,
            (51, 45)
        )

    def test_set_anchor_valid_list(self):
        bPoint = self.getBPoint_corner()
        bPoint.anchor = [51, 45]
        self.assertEqual(
            bPoint.anchor,
            (51, 45)
        )

    def test_set_anchor_invalid_too_many_items(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(ValueError):
            bPoint.anchor = (51, 45, 67)

    def test_set_anchor_invalid_single_item_list(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(ValueError):
            bPoint.anchor = [51]

    def test_set_anchor_invalid_single_item_tuple(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(ValueError):
            bPoint.anchor = (51,)

    def test_set_anchor_invalidType_int(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.anchor = 51

    def test_set_anchor_invalidType_None(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.anchor = None

    # bcp in

    def test_get_bcpIn_corner(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.bcpIn,
            (0, 0)
        )

    def test_get_bcpIn_curve(self):
        bPoint = self.getBPoint_curve()
        self.assertEqual(
            bPoint.bcpIn,
            (-40, -12)
        )

    def test_set_bcpIn_corner_valid_tuple(self):
        bPoint = self.getBPoint_corner()
        bPoint.bcpIn = (51, 45)
        self.assertEqual(
            bPoint.bcpIn,
            (51, 45)
        )

    def test_set_bcpIn_corner_with_bcpOut(self):
        bPoint = self.getBPoint_corner_with_bcpOut()
        bPoint.bcpIn = (51, 45)
        self.assertEqual(
            bPoint.bcpIn,
            (51, 45)
        )

    def test_set_bcpIn_curve_valid_tuple(self):
        bPoint = self.getBPoint_curve()
        bPoint.bcpIn = (51, 45)
        self.assertEqual(
            bPoint.bcpIn,
            (51, 45)
        )

    def test_set_bcpIn_curve_firstPointOpenContour(self):
        bPoint = self.getBPoint_curve_firstPointOpenContour()
        with self.assertRaises(FontPartsError):
            bPoint.bcpIn = (10, 20)

    def test_set_bcpIn_valid_list(self):
        bPoint = self.getBPoint_corner()
        bPoint.bcpIn = [51, 45]
        self.assertEqual(
            bPoint.bcpIn,
            (51, 45)
        )

    def test_set_bcpIn_invalid_too_many_items(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(ValueError):
            bPoint.bcpIn = [51, 45, 67]

    def test_set_bcpIn_invalid_single_item_list(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(ValueError):
            bPoint.bcpIn = [51]

    def test_set_bcpIn_invalid_single_item_tuple(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.bcpIn = (51)

    def test_set_bcpIn_invalidType_int(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.bcpIn = 51

    def test_set_bcpIn_invalidType_None(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.bcpIn = None

    # bcp out

    def test_get_bcpOut_corner(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.bcpOut,
            (0, 0)
        )

    def test_get_bcpOut_curve(self):
        bPoint = self.getBPoint_curve()
        self.assertEqual(
            bPoint.bcpOut,
            (32, 10)
        )

    def test_set_bcpOut_corner_valid_tuple(self):
        bPoint = self.getBPoint_corner()
        bPoint.bcpOut = (51, 45)
        self.assertEqual(
            bPoint.bcpOut,
            (51, 45)
        )

    def test_set_bcpOut_corner_with_bcpIn(self):
        bPoint = self.getBPoint_corner_with_bcpIn()
        bPoint.bcpOut = (51, 45)
        self.assertEqual(
            bPoint.bcpOut,
            (51, 45)
        )

    def test_set_bcpOut_curve_valid_tuple(self):
        bPoint = self.getBPoint_curve()
        bPoint.bcpOut = (51, 45)
        self.assertEqual(
            bPoint.bcpOut,
            (51, 45)
        )

    def test_set_bcpOut_valid_list(self):
        bPoint = self.getBPoint_curve()
        bPoint.bcpOut = [51, 45]
        self.assertEqual(
            bPoint.bcpOut,
            (51, 45)
        )

    def test_set_bcpOut_curve_lastPointOpenContour(self):
        bPoint = self.getBPoint_curve_lastPointOpenContour()
        with self.assertRaises(FontPartsError):
            bPoint.bcpOut = (10, 20)

    def test_set_bcpOut_invalid_too_many_items(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(ValueError):
            bPoint.bcpOut = [51, 45, 67]

    def test_set_bcpOut_invalid_single_item_list(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(ValueError):
            bPoint.bcpOut = [51]

    def test_set_bcpOut_invalid_single_item_tuple(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.bcpOut = (51)

    def test_set_bcpOut_invalidType_int(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.bcpOut = 51

    def test_set_bcpOut_invalidType_None(self):
        bPoint = self.getBPoint_corner()
        with self.assertRaises(TypeError):
            bPoint.bcpOut = None

    # --------------
    # Identification
    # --------------

    # index

    def getBPoint_noParentContour(self):
        bPoint, _ = self.objectGenerator("bPoint")
        bPoint.anchor = (101, 202)
        bPoint.bcpIn = (-40, 0)
        bPoint.bcpOut = (50, 0)
        bPoint.type = "curve"
        return bPoint

    def test_get_index(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            bPoint.index,
            1
        )

    # def test_get_index_noParentContour(self):
    #     bPoint = self.getBPoint_noParentContour()
    #     self.assertEqual(
    #         bPoint.index,
    #         None
    #     )

    def test_set_index(self):
        point = self.getBPoint_corner()
        with self.assertRaises(FontPartsError):
            point.index = 0

    # identifier

    def test_identifier_get_none(self):
        bPoint = self.getBPoint_corner()
        self.assertIsNone(bPoint.identifier)

    def test_identifier_generated_type(self):
        bPoint = self.getBPoint_corner()
        bPoint.getIdentifier()
        self.assertIsInstance(bPoint.identifier, str)

    def test_identifier_consistency(self):
        bPoint = self.getBPoint_corner()
        bPoint.getIdentifier()
        # get: twice to test consistency
        self.assertEqual(bPoint.identifier, bPoint.identifier)

    def test_identifier_cannot_set(self):
        # identifier is a read-only property
        bPoint = self.getBPoint_corner()
        with self.assertRaises(FontPartsError):
            bPoint.identifier = "ABC"

    # def test_getIdentifer_no_contour(self):
    #     bPoint, _ = self.objectGenerator("bPoint")
    #     with self.assertRaises(FontPartsError):
    #         bPoint.getIdentifier()

    def test_getIdentifer_consistency(self):
        bPoint = self.getBPoint_corner()
        bPoint.getIdentifier()
        self.assertEqual(bPoint.identifier, bPoint.getIdentifier())

    # ----
    # Hash
    # ----

    def test_hash(self):
        bPoint = self.getBPoint_corner()
        self.assertEqual(
            isinstance(bPoint, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        bPoint_one = self.getBPoint_corner()
        self.assertEqual(
            bPoint_one,
            bPoint_one
        )

    def test_object_not_equal_other(self):
        bPoint_one = self.getBPoint_corner()
        bPoint_two = self.getBPoint_corner()
        self.assertNotEqual(
            bPoint_one,
            bPoint_two
        )

    def test_object_equal_self_variable_assignment(self):
        bPoint_one = self.getBPoint_corner()
        a = bPoint_one
        a.anchor = (51, 45)
        self.assertEqual(
            bPoint_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        bPoint_one = self.getBPoint_corner()
        bPoint_two = self.getBPoint_corner()
        a = bPoint_one
        self.assertNotEqual(
            bPoint_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        bPoint = self.getBPoint_corner()
        try:
            bPoint.selected = False
        except NotImplementedError:
            return
        bPoint.selected = True
        self.assertEqual(
            bPoint.selected,
            True
        )

    def test_selected_false(self):
        bPoint = self.getBPoint_corner()
        try:
            bPoint.selected = False
        except NotImplementedError:
            return
        bPoint.selected = False
        self.assertEqual(
            bPoint.selected,
            False
        )

    # ----
    # Copy
    # ----

    def test_copy_seperate_objects(self):
        bPoint = self.getBPoint_corner()
        copied = bPoint.copy()
        self.assertIsNot(
            bPoint,
            copied
        )

    def test_copy_different_contour(self):
        bPoint = self.getBPoint_corner()
        copied = bPoint.copy()
        self.assertIsNot(
            bPoint.contour,
            copied.contour
        )

    def test_copy_none_contour(self):
        bPoint = self.getBPoint_corner()
        copied = bPoint.copy()
        self.assertEqual(
            copied.contour,
            None
        )

    # def test_copy_same_type(self):
    #     bPoint = self.getBPoint_corner()
    #     copied = bPoint.copy()
    #     self.assertEqual(
    #         bPoint.type,
    #         copied.type
    #     )

    # def test_copy_same_anchor(self):
    #     bPoint = self.getBPoint_corner()
    #     copied = bPoint.copy()
    #     self.assertEqual(
    #         bPoint.anchor,
    #         copied.anchor
    #     )

    # def test_copy_same_bcpIn(self):
    #     bPoint = self.getBPoint_corner()
    #     copied = bPoint.copy()
    #     self.assertEqual(
    #         bPoint.bcpIn,
    #         copied.bcpIn
    #     )

    # def test_copy_same_bcpOut(self):
    #     bPoint = self.getBPoint_corner()
    #     copied = bPoint.copy()
    #     self.assertEqual(
    #         bPoint.bcpOut,
    #         copied.bcpOut
    #     )

    # def test_copy_same_identifier_None(self):
    #     bPoint = self.getBPoint_corner()
    #     bPoint.identifer = None
    #     copied = bPoint.copy()
    #     self.assertEqual(
    #         bPoint.identifier,
    #         copied.identifier,
    #     )

    # def test_copy_different_identifier(self):
    #     bPoint = self.getBPoint_corner()
    #     bPoint.getIdentifier()
    #     copied = bPoint.copy()
    #     self.assertNotEqual(
    #         bPoint.identifier,
    #         copied.identifier,
    #     )

    # def test_copy_generated_identifier_different(self):
    #     otherContour, _ = self.objectGenerator("contour")
    #     bPoint = self.getBPoint_corner()
    #     copied = bPoint.copy()
    #     copied.contour = otherContour
    #     bPoint.getIdentifier()
    #     copied.getIdentifier()
    #     self.assertNotEqual(
    #         bPoint.identifier,
    #         copied.identifier
    #     )

    # def test_copyData_type(self):
    #     bPoint = self.getBPoint_corner()
    #     bPointOther, _ = self.objectGenerator("bPoint")
    #     bPointOther.copyData(bPoint)
    #     self.assertEqual(
    #         bPoint.type,
    #         bPointOther.type,
    #     )

    # def test_copyData_anchor(self):
    #     bPoint = self.getBPoint_corner()
    #     bPointOther, _ = self.objectGenerator("bPoint")
    #     bPointOther.copyData(bPoint)
    #     self.assertEqual(
    #         bPoint.anchor,
    #         bPointOther.anchor,
    #     )

    # def test_copyData_bcpIn(self):
    #     bPoint = self.getBPoint_corner()
    #     bPointOther, _ = self.objectGenerator("bPoint")
    #     bPointOther.copyData(bPoint)
    #     self.assertEqual(
    #         bPoint.bcpIn,
    #         bPointOther.bcpIn,
    #     )

    # def test_copyData_bcpOut(self):
    #     bPoint = self.getBPoint_corner()
    #     bPointOther, _ = self.objectGenerator("bPoint")
    #     bPointOther.copyData(bPoint)
    #     self.assertEqual(
    #         bPoint.bcpOut,
    #         bPointOther.bcpOut,
    #     )

    # --------------
    # Transformation
    # --------------

    # transformBy

    def test_transformBy_valid_no_origin_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(
            bPoint.anchor,
            (199.0, 608.0)
        )

    def test_transformBy_valid_no_origin_bcpIn(self):
        bPoint = self.getBPoint_curve()
        bPoint.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(
            bPoint.bcpIn,
            (-80.0, -36.0)
        )

    def test_transformBy_valid_no_origin_bcpOut(self):
        bPoint = self.getBPoint_curve()
        bPoint.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(
            bPoint.bcpOut,
            (64.0, 30.0)
        )

    def test_transformBy_valid_origin_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(
            bPoint.anchor,
            (201.0, 402.0)
        )

    def test_transformBy_valid_origin_bcpIn(self):
        bPoint = self.getBPoint_curve()
        bPoint.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(
            bPoint.bcpIn,
            (-80.0, -24.0)
        )

    def test_transformBy_valid_origin_bcpOut(self):
        bPoint = self.getBPoint_curve()
        bPoint.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(
            bPoint.bcpOut,
            (64.0, 20.0)
        )

    def test_transformBy_invalid_one_string_value(self):
        point = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            point.transformBy((1, 0, 0, 1, 0, "0"))

    def test_transformBy_invalid_all_string_values(self):
        point = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            point.transformBy("1, 0, 0, 1, 0, 0")

    def test_transformBy_invalid_int_value(self):
        point = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            point.transformBy(123)

    # moveBy

    def test_moveBy_valid_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.moveBy((-1, 2))
        self.assertEqual(
            bPoint.anchor,
            (100.0, 204.0)
        )

    def test_moveBy_noChange_bcpIn(self):
        bPoint = self.getBPoint_curve()
        bPoint.moveBy((-1, 2))
        otherBPoint = self.getBPoint_curve()
        self.assertEqual(
            bPoint.bcpIn,
            otherBPoint.bcpIn
        )

    def test_moveBy_noChange_bcpOut(self):
        bPoint = self.getBPoint_curve()
        bPoint.moveBy((-1, 2))
        otherBPoint = self.getBPoint_curve()
        self.assertEqual(
            bPoint.bcpOut,
            otherBPoint.bcpOut
        )

    def test_moveBy_invalid_one_string_value(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            bPoint.moveBy((-1, "2"))

    def test_moveBy_invalid_all_strings_value(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            bPoint.moveBy("-1, 2")

    def test_moveBy_invalid_int_value(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            bPoint.moveBy(1)

    # scaleBy

    def test_scaleBy_valid_one_value_no_origin_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.scaleBy((-2))
        self.assertEqual(
            bPoint.anchor,
            (-202.0, -404.0)
        )

    def test_scaleBy_valid_two_values_no_origin_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.scaleBy((-2, 3))
        self.assertEqual(
            bPoint.anchor,
            (-202.0, 606.0)
        )

    def test_scaleBy_valid_two_values_origin_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(
            bPoint.anchor,
            (-199.0, 602.0)
        )

    def test_scaleBy_valid_two_values_origin_bcpIn(self):
        bPoint = self.getBPoint_curve()
        bPoint.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(
            bPoint.bcpIn,
            (80.0, -36.0)
        )

    def test_scaleBy_valid_two_values_origin_bcpOut(self):
        bPoint = self.getBPoint_curve()
        bPoint.scaleBy((-2, 3), origin=(1, 2))
        self.assertEqual(
            bPoint.bcpOut,
            (-64.0, 30.0)
        )

    def test_invalid_one_string_value_scaleBy(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            bPoint.scaleBy((-1, "2"))

    def test_invalid_two_string_values_scaleBy(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            bPoint.scaleBy("-1, 2")

    def test_invalid_tuple_too_many_values_scaleBy(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(ValueError):
            bPoint.scaleBy((-1, 2, -3))

    # rotateBy

    def test_rotateBy_valid_no_origin_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.rotateBy(45)
        self.assertEqual(
            [(round(bPoint.anchor[0], 3)), (round(bPoint.anchor[1], 3))],
            [-71.418, 214.253]
        )

    def test_rotateBy_valid_origin_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.rotateBy(45, origin=(1, 2))
        self.assertEqual(
            [(round(bPoint.anchor[0], 3)), (round(bPoint.anchor[1], 3))],
            [-69.711, 214.132]
        )

    def test_rotateBy_valid_origin_bcpIn(self):
        bPoint = self.getBPoint_curve()
        bPoint.rotateBy(45, origin=(1, 2))
        self.assertEqual(
            [(round(bPoint.bcpIn[0], 3)), (round(bPoint.bcpIn[1], 3))],
            [-19.799, -36.77]
        )

    def test_rotateBy_valid_origin_bcpOut(self):
        bPoint = self.getBPoint_curve()
        bPoint.rotateBy(45, origin=(1, 2))
        self.assertEqual(
            [(round(bPoint.bcpOut[0], 3)), (round(bPoint.bcpOut[1], 3))],
            [15.556, 29.698]
        )

    def test_rotateBy_invalid_string_value(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            bPoint.rotateBy("45")

    def test_rotateBy_invalid_too_large_value_positive(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(ValueError):
            bPoint.rotateBy(361)

    def test_rotateBy_invalid_too_large_value_negative(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(ValueError):
            bPoint.rotateBy(-361)

    # skewBy

    def test_skewBy_valid_no_origin_one_value_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.skewBy(100)
        self.assertEqual(
            [(round(bPoint.anchor[0], 3)), (round(bPoint.anchor[1], 3))],
            [-1044.599, 202.0]
        )

    def test_skewBy_valid_no_origin_two_values_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.skewBy((100, 200))
        self.assertEqual(
            [(round(bPoint.anchor[0], 3)), (round(bPoint.anchor[1], 3))],
            [-1044.599, 238.761]
        )

    def test_skewBy_valid_origin_one_value_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.skewBy(100, origin=(1, 2))
        self.assertEqual(
            [(round(bPoint.anchor[0], 3)), (round(bPoint.anchor[1], 3))],
            [-1033.256, 202.0]
        )

    def test_skewBy_valid_origin_two_values_anchor(self):
        bPoint = self.getBPoint_curve()
        bPoint.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(
            [(round(bPoint.anchor[0], 3)), (round(bPoint.anchor[1], 3))],
            [-1033.256, 238.397]
        )

    def test_skewBy_valid_origin_two_values_bcpIn(self):
        bPoint = self.getBPoint_curve()
        bPoint.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(
            [(round(bPoint.bcpIn[0], 3)), (round(bPoint.bcpIn[1], 3))],
            [28.055, -26.559]
        )

    def test_skewBy_valid_origin_two_values_bcpOut(self):
        bPoint = self.getBPoint_curve()
        bPoint.skewBy((100, 200), origin=(1, 2))
        self.assertEqual(
            [(round(bPoint.bcpOut[0], 3)), (round(bPoint.bcpOut[1], 3))],
            [-24.713, 21.647]
        )

    def test_skewBy_invalid_string_value(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(TypeError):
            bPoint.skewBy("45")

    def test_skewBy_invalid_too_large_value_positive(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(ValueError):
            bPoint.skewBy(361)

    def test_skewBy_invalid_too_large_value_negative(self):
        bPoint = self.getBPoint_curve()
        with self.assertRaises(ValueError):
            bPoint.skewBy(-361)

    # -------------
    # Normalization
    # -------------

    # round

    def getBPoint_curve_float(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((19.231, 121.291), "offcurve")
        contour.appendPoint((61.193, 190.942), "offcurve")
        contour.appendPoint((101.529, 202.249), "curve", smooth=True)
        contour.appendPoint((133.948, 212.193), "offcurve")
        contour.appendPoint((155.491, 147.314), "offcurve")
        contour.appendPoint((255.295, 147.314), "curve")
        bPoint = contour.bPoints[1]
        return bPoint

    def test_round_anchor(self):
        bPoint = self.getBPoint_curve_float()
        bPoint.round()
        self.assertEqual(
            bPoint.anchor,
            (102.0, 202.0)
        )

    def test_round_bcpIn(self):
        bPoint = self.getBPoint_curve_float()
        bPoint.round()
        self.assertEqual(
            bPoint.bcpIn,
            (-40.0, -11.0)
        )

    def test_round_bcpOut(self):
        bPoint = self.getBPoint_curve_float()
        bPoint.round()
        self.assertEqual(
            bPoint.bcpOut,
            (32.0, 10.0)
        )

import unittest
import collections
from fontParts.base import FontPartsError


class TestContour(unittest.TestCase):

    def getContour_bounds(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((100, 100), "line")
        contour.appendPoint((100, 0), "line")
        return contour

    # ----
    # Repr
    # ----

    def test_reprContents_noGlyph_noID(self):
        contour = self.getContour_bounds()
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        for i in value:
            self.assertIsInstance(i, str)

    def test_reprContents_noGlyph_ID(self):
        contour = self.getContour_bounds()
        contour.getIdentifier()
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        idFound = False
        for i in value:
            self.assertIsInstance(i, str)
            if i == "identifier='%r'" % contour.identifier:
                idFound = True
        self.assertTrue(idFound)

    def test_reprContents_Glyph_ID(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        contour.getIdentifier()
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        idFound = False
        glyphFound = False
        for i in value:
            self.assertIsInstance(i, str)
            if i == "identifier='%r'" % contour.identifier:
                idFound = True
            if i == "in glyph":
                glyphFound = True
        self.assertTrue(idFound)
        self.assertTrue(glyphFound)

    def test_reprContents_Glyph_noID(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        value = contour._reprContents()
        self.assertIsInstance(value, list)
        glyphFound = False
        for i in value:
            self.assertIsInstance(i, str)
            if i == "in glyph":
                glyphFound = True
        self.assertTrue(glyphFound)

    # ----
    # Copy
    # ----

    def test_copyData(self):
        contour = self.getContour_bounds()
        contourOther, _ = self.objectGenerator("contour")
        contourOther.copyData(contour)
        self.assertEqual(
            contour.bounds,
            contourOther.bounds
        )

    # -------
    # Parents
    # -------

    def test_parent_glyph_set_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        self.assertEqual(glyph, contour.glyph)

    def test_parent_glyph_set_glyph_None(self):
        contour = self.getContour_bounds()
        contour.glyph = None
        self.assertEqual(None, contour.glyph)

    def test_parent_glyph_set_already_set(self):
        glyph, _ = self.objectGenerator("glyph")
        glyph2, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour.glyph = glyph
        self.assertEqual(glyph, contour.glyph)
        with self.assertRaises(AssertionError):
            contour.glyph = glyph2

    def test_parent_glyph_get_none(self):
        contour = self.getContour_bounds()
        self.assertEqual(None, contour.glyph)

    def test_parent_glyph_get(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        contour = glyph.appendContour(contour)
        self.assertEqual(glyph, contour.glyph)

    def test_parent_font_set(self):
        font, _ = self.objectGenerator("font")
        contour = self.getContour_bounds()
        with self.assertRaises(FontPartsError):
            contour.font = font

    def test_parent_font_get_none(self):
        contour = self.getContour_bounds()
        self.assertEqual(None, contour.font)

    def test_parent_font_get(self):
        font, _ = self.objectGenerator("font")
        layer, _ = self.objectGenerator("layer")
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        layer.font = font
        glyph.layer = layer
        contour = glyph.appendContour(contour)
        self.assertEqual(font, contour.font)

    def test_parent_layer_set(self):
        layer, _ = self.objectGenerator("layer")
        contour = self.getContour_bounds()
        with self.assertRaises(FontPartsError):
            contour.layer = layer

    def test_parent_layer_get_none(self):
        contour = self.getContour_bounds()
        self.assertEqual(None, contour.layer)

    def test_parent_layer_get(self):
        layer, _ = self.objectGenerator("layer")
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        glyph.layer = layer
        contour = glyph.appendContour(contour)
        self.assertEqual(layer, contour.layer)

    # -----
    # Index
    # -----

    def test_index(self):
        glyph, _ = self.objectGenerator("glyph")
        contour1 = glyph.appendContour(self.getContour_bounds())
        contour2 = glyph.appendContour(self.getContour_bounds())
        contour3 = glyph.appendContour(self.getContour_bounds())
        self.assertEqual(contour1.index, 0)
        self.assertEqual(contour2.index, 1)
        self.assertEqual(contour3.index, 2)

    def test_set_index(self):
        glyph, _ = self.objectGenerator("glyph")
        contour1 = glyph.appendContour(self.getContour_bounds())
        contour2 = glyph.appendContour(self.getContour_bounds())
        contour3 = glyph.appendContour(self.getContour_bounds())

        contour1.index = 2
        self.assertEqual(contour1.index, 2)
        self.assertEqual(contour2.index, 0)
        self.assertEqual(contour3.index, 1)

        contour1.index = 1
        self.assertEqual(contour1.index, 1)
        self.assertEqual(contour2.index, 0)
        self.assertEqual(contour3.index, 2)

    # --------------
    # Identification
    # --------------

    def test_get_index_no_glyph(self):
        contour = self.getContour_bounds()
        self.assertEqual(contour.index, None)

    def test_get_index_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        contour = self.getContour_bounds()
        c1 = glyph.appendContour(contour)
        self.assertEqual(c1.index, 0)
        c2 = glyph.appendContour(contour)
        self.assertEqual(c2.index, 1)

    # ------
    # Bounds
    # ------

    def getContour_boundsExtrema(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 100), "line")
        contour.appendPoint((50, 100), "line")
        contour.appendPoint((117, 100), "offcurve")
        contour.appendPoint((117, 0), "offcurve")
        contour.appendPoint((50, 0), "curve")
        return contour

    def test_bounds_get(self):
        contour = self.getContour_bounds()
        self.assertEqual(
            contour.bounds,
            (0, 0, 100, 100)
        )

    def test_bounds_set_float(self):
        contour = self.getContour_bounds()
        contour.moveBy((0.5, -0.5))
        self.assertEqual(
            contour.bounds,
            (0.5, -0.5, 100.5, 99.5)
        )

    def test_bounds_point_not_at_extrema(self):
        contour = self.getContour_bounds()
        contour = self.getContour_boundsExtrema()
        bounds = tuple(int(round(i)) for i in contour.bounds)
        self.assertEqual(
            bounds,
            (0, 0, 100, 100)
        )

    def test_invalid_bounds_set(self):
        contour = self.getContour_bounds()
        with self.assertRaises(FontPartsError):
            contour.bounds = (1, 2, 3, 4)

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        contour_one = self.getContour_bounds()
        self.assertEqual(
            hash(contour_one),
            hash(contour_one)
        )

    def test_hash_object_other(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        self.assertNotEqual(
            hash(contour_one),
            hash(contour_two)
        )

    def test_hash_object_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        a = contour_one
        self.assertEqual(
            hash(contour_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        a = contour_one
        self.assertNotEqual(
            hash(contour_two),
            hash(a)
        )

    def test_is_hashable(self):
        contour_one = self.getContour_bounds()
        self.assertTrue(
            isinstance(contour_one, collections.Hashable)
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        contour_one = self.getContour_bounds()
        self.assertEqual(
            contour_one,
            contour_one
        )

    def test_object_not_equal_self(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        self.assertNotEqual(
            contour_one,
            contour_two
        )

    def test_object_equal_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        a = contour_one
        a.moveBy((0.5, -0.5))
        self.assertEqual(
            contour_one,
            a
        )

    def test_object_not_equal_self_variable_assignment(self):
        contour_one = self.getContour_bounds()
        contour_two = self.getContour_bounds()
        a = contour_one
        self.assertNotEqual(
            contour_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        contour = self.getContour_bounds()
        try:
            contour.selected = False
        except NotImplementedError:
            return
        contour.selected = True
        self.assertEqual(
            contour.selected,
            True
        )

    def test_selected_false(self):
        contour = self.getContour_bounds()
        try:
            contour.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selected,
            False
        )

    def test_selectedSegments_default(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selectedSegments,
            ()
        )

    def test_selectedSegments_setSubObject(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        segment2 = contour.segments[1]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        segment2.selected = True
        self.assertEqual(
            contour.selectedSegments == (segment2,),
            True
        )

    def test_selectedSegments_setFilledList(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        segment2 = contour.segments[1]
        try:
            segment1.selected = False
        except NotImplementedError:
            return
        contour.selectedSegments = [segment1, segment2]
        self.assertEqual(
            contour.selectedSegments,
            (segment1, segment2)
        )

    def test_selectedSegments_setEmptyList(self):
        contour = self.getContour_bounds()
        segment1 = contour.segments[0]
        try:
            segment1.selected = True
        except NotImplementedError:
            return
        contour.selectedSegments = []
        self.assertEqual(
            contour.selectedSegments,
            ()
        )

    def test_selectedPoints_default(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selectedPoints,
            ()
        )

    def test_selectedPoints_setSubObject(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        point2 = contour.points[1]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        point2.selected = True
        self.assertEqual(
            contour.selectedPoints,
            (point2,)
        )

    def test_selectedPoints_setFilledList(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        point2 = contour.points[1]
        try:
            point1.selected = False
        except NotImplementedError:
            return
        contour.selectedPoints = [point1, point2]
        self.assertEqual(
            contour.selectedPoints,
            (point1, point2)
        )

    def test_selectedPoints_setEmptyList(self):
        contour = self.getContour_bounds()
        point1 = contour.points[0]
        try:
            point1.selected = True
        except NotImplementedError:
            return
        contour.selectedPoints = []
        self.assertEqual(
            contour.selectedPoints,
            ()
        )

    def test_selectedBPoints_default(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            contour.selectedBPoints,
            ()
        )

    def test_selectedBPoints_setSubObject(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        bPoint2 = contour.bPoints[1]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        bPoint2.selected = True
        self.assertEqual(
            contour.selectedBPoints,
            (bPoint2,)
        )

    def test_selectedBPoints_setFilledList(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        bPoint2 = contour.bPoints[1]
        try:
            bPoint1.selected = False
        except NotImplementedError:
            return
        contour.selectedBPoints = [bPoint1, bPoint2]
        self.assertEqual(
            contour.selectedBPoints,
            (bPoint1, bPoint2)
        )

    def test_selectedBPoints_setEmptyList(self):
        contour = self.getContour_bounds()
        bPoint1 = contour.bPoints[0]
        try:
            bPoint1.selected = True
        except NotImplementedError:
            return
        contour.selectedBPoints = []
        self.assertEqual(
            contour.selectedBPoints,
            ()
        )

    # --------
    # Segments
    # --------

    def test_segments_offcurves_end(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")
        contour.appendPoint((46, 64), "curve")
        contour.appendPoint((76, 64), "offcurve")
        contour.appendPoint((84, 28), "offcurve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["line", "curve", "curve"]
        )

    def test_segments_offcurves_begin_end(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((84, 28), "offcurve")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")
        contour.appendPoint((46, 64), "curve")
        contour.appendPoint((76, 64), "offcurve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["line", "curve", "curve"]
        )

    def test_segments_offcurves_begin(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((76, 64), "offcurve")
        contour.appendPoint((84, 28), "offcurve")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")
        contour.appendPoint((46, 64), "curve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["line", "curve", "curve"]
        )

    def test_segments_offcurves_middle(self):
        contour, _ = self.objectGenerator("contour")
        contour.appendPoint((46, 64), "curve")
        contour.appendPoint((76, 64), "offcurve")
        contour.appendPoint((84, 28), "offcurve")
        contour.appendPoint((84, 0), "curve")
        contour.appendPoint((0, 0), "line")
        contour.appendPoint((0, 28), "offcurve")
        contour.appendPoint((10, 64), "offcurve")

        segments = contour.segments
        self.assertEqual(
            [segment.type for segment in segments], ["curve", "line", "curve"]
        )

    def test_segments_empty(self):
        contour, _ = self.objectGenerator("contour")
        segments = contour.segments
        self.assertEqual(segments, [])

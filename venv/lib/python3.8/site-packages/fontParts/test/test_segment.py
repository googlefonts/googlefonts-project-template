import unittest
import collections


class TestSegment(unittest.TestCase):

    def getSegment_line(self):
        contour, unrequested = self.objectGenerator("contour")
        unrequested.append(contour)
        contour.appendPoint((0, 0), "move")
        contour.appendPoint((101, 202), "line")
        segment = contour[1]
        return segment

    # ----
    # Type
    # ----

    def test_type_get(self):
        segment = self.getSegment_line()
        self.assertEqual(
            segment.type,
            "line"
        )

    def test_set_move(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(
            segment.type,
            "move"
        )

    def test_len_move(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(
            len(segment.points),
            1
        )

    def test_oncuve_type_move(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(
            segment.onCurve.type,
            "move"
        )

    def test_oncuve_x_y(self):
        segment = self.getSegment_line()
        segment.type = "move"
        self.assertEqual(
            (segment.onCurve.x, segment.onCurve.y),
            (101, 202)
        )

    def test_set_curve(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        self.assertEqual(
            segment.type,
            "curve"
        )

    def test_len_curve(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        self.assertEqual(
            len(segment.points),
            3
        )

    def test_curve_pt_types(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        types = tuple(point.type for point in segment.points)
        self.assertEqual(
            types,
            ("offcurve", "offcurve", "curve")
        )

    def test_curve_pt_x_y(self):
        segment = self.getSegment_line()
        segment.type = "curve"
        coordinates = tuple((point.x, point.y) for point in segment.points)
        self.assertEqual(
            coordinates,
            ((0, 0), (101, 202), (101, 202))
        )

    def test_set_qcurve(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        self.assertEqual(
            segment.type,
            "qcurve"
        )

    def test_len_qcurve(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        self.assertEqual(
            len(segment.points),
            3
        )

    def test_qcurve_pt_types(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        types = tuple(point.type for point in segment.points)
        self.assertEqual(
            types,
            ("offcurve", "offcurve", "qcurve")
        )

    def test_qcurve_pt_x_y(self):
        segment = self.getSegment_line()
        segment.type = "qcurve"
        coordinates = tuple((point.x, point.y) for point in segment.points)
        self.assertEqual(
            coordinates,
            ((0, 0), (101, 202), (101, 202))
        )

    def test_set_invalid_segment_type_string(self):
        segment = self.getSegment_line()
        with self.assertRaises(ValueError):
            segment.type = "xxx"

    def test_set_invalid_segment_type_int(self):
        segment = self.getSegment_line()
        with self.assertRaises(TypeError):
            segment.type = 123

    def test_offCurve_only_segment(self):
        contour, unrequested = self.objectGenerator("contour")
        unrequested.append(contour)
        contour.appendPoint((0, 0), "offcurve")
        contour.appendPoint((100, 0), "offcurve")
        contour.appendPoint((100, 100), "offcurve")
        contour.appendPoint((0, 100), "offcurve")
        segment = contour[0]
        self.assertEqual(
            len(contour),
            1
        )
        # onCurve is a dummy None value, telling this is an on-curve-less quad blob
        self.assertIsNone(
            segment.onCurve,
        )
        self.assertEqual(
            segment.points,
            segment.offCurve
        )
        self.assertEqual(
            segment.type,
            "qcurve"
        )


    # ----
    # Hash
    # ----

    def test_hash(self):
        segment = self.getSegment_line()
        self.assertEqual(
            isinstance(segment, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        segment_one = self.getSegment_line()
        self.assertEqual(
            segment_one,
            segment_one
        )

    def test_object_not_equal_other(self):
        segment_one = self.getSegment_line()
        segment_two = self.getSegment_line()
        self.assertNotEqual(
            segment_one,
            segment_two
        )

    def test_object_equal_self_variable_assignment(self):
        segment_one = self.getSegment_line()
        a = segment_one
        self.assertEqual(
            segment_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        segment_one = self.getSegment_line()
        segment_two = self.getSegment_line()
        a = segment_one
        self.assertNotEqual(
            segment_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        segment = self.getSegment_line()
        try:
            segment.selected = False
        except NotImplementedError:
            return
        segment.selected = True
        self.assertEqual(
            segment.selected,
            True
        )

    def test_selected_false(self):
        segment = self.getSegment_line()
        try:
            segment.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            segment.selected,
            False
        )

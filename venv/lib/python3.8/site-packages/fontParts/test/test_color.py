import unittest
from fontParts.base.color import Color


class TestComponent(unittest.TestCase):

    def test_color_r(self):
        color = Color((1.0, 0, 0, 0))
        self.assertEqual(color.r, 1.0)

    def test_color_g(self):
        color = Color((0, 1.0, 0, 0))
        self.assertEqual(color.g, 1.0)

    def test_color_b(self):
        color = Color((0, 0, 1.0, 0))
        self.assertEqual(color.b, 1.0)

    def test_color_a(self):
        color = Color((0, 0, 0, 1.00))
        self.assertEqual(color.a, 1.0)

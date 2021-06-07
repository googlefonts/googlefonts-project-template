#!/usr/bin/env python2
#
# Copyright 2011-2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import unittest

import sre_yield


class AnchorTest(unittest.TestCase):
    """Test that allowed anchors in allowed positions work."""

    def testAnchorsCaret(self):
        parsed = sre_yield.Values("^[ab]")
        self.assertEqual(["a", "b"], list(parsed))

    def testAnchorsA(self):
        parsed = sre_yield.Values("\\A[ab]")
        self.assertEqual(["a", "b"], list(parsed))

    def testAnchorsMultiCaret(self):
        parsed = sre_yield.Values("^(\\b^([ab]))")
        self.assertEqual(["a", "b"], list(parsed))

    def testParseErrorInMiddle(self):
        self.assertRaises(sre_yield.ParseError, sre_yield.Values, "a\\bb")
        self.assertRaises(sre_yield.ParseError, sre_yield.Values, "a^b")
        self.assertRaises(sre_yield.ParseError, sre_yield.Values, "a$b")

    def testParseErrorNotBoundary(self):
        self.assertRaises(sre_yield.ParseError, sre_yield.Values, "\\Ba")
        self.assertRaises(sre_yield.ParseError, sre_yield.Values, "a\\B")
        self.assertRaises(sre_yield.ParseError, sre_yield.Values, "a\\Bb")

    def testAnchorsDollar(self):
        parsed = sre_yield.Values("[ab]$")
        self.assertEqual(["a", "b"], list(parsed))

    def testAnchorsZ(self):
        parsed = sre_yield.Values("[ab]\\Z")
        self.assertEqual(["a", "b"], list(parsed))

    def testAnchorsCombined(self):
        parsed = sre_yield.Values("^[ab]$")
        self.assertEqual(["a", "b"], list(parsed))

    def testAnchorsBoundary(self):
        parsed = sre_yield.Values("ab\\b")
        self.assertEqual(["ab"], list(parsed))
        parsed = sre_yield.Values("\\bab")
        self.assertEqual(["ab"], list(parsed))
        parsed = sre_yield.Values("\\bab\\b")
        self.assertEqual(["ab"], list(parsed))

    def testAnchorsRepeated(self):
        parsed = sre_yield.Values(r"^\b^[ab]")
        self.assertEqual(["a", "b"], list(parsed))

    def testAnchorsRepeated(self):
        parsed = sre_yield.Values(r"[ab]$\b$")
        self.assertEqual(["a", "b"], list(parsed))

    def testAnchorsEmptyString(self):
        parsed = sre_yield.Values(r"^^^$\b$")
        self.assertEqual([""], list(parsed))


if __name__ == "__main__":
    unittest.main()

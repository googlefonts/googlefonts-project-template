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


class SlowYieldTest(unittest.TestCase):
    """Test that regular expressions give the right lists."""

    def testDotStarCase(self):
        test_size = sre_yield.AllStrings(".*", re.DOTALL).__len__()
        actual_size = 0
        for _ in range(65536):
            actual_size = actual_size * 256 + 1
        self.assertEqual(test_size, actual_size)

    def testContentsNearBreak(self):
        # This specific location is on either side of offset_break in sre_yield.py
        v = sre_yield.Values(".*")
        a = v[70386233652806655][:10]
        self.assertEqual("\xff\xff\xff\xff\xff\xff\xff", a)
        b = v[70386233652806656][:10]
        self.assertEqual("\x00\x00\x00\x00\x00\x00\x00\x00", b)
        c = v[70386233652806657][:10]
        self.assertEqual("\x00\x00\x00\x00\x00\x00\x00\x01", c)


if __name__ == "__main__":
    unittest.main()

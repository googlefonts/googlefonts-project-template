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

import unittest

from sre_yield import cachingseq


class CachingFuncSequenceTest(unittest.TestCase):
    def testLimits(self):
        c = cachingseq.CachingFuncSequence(lambda i: i, 10)
        self.assertEqual(9, c[9])
        self.assertEqual(9, c[-1])
        self.assertEqual(0, c[0])
        self.assertEqual(0, c[-10])
        self.assertRaises(IndexError, lambda: c[10])
        self.assertRaises(IndexError, lambda: c[11])
        self.assertRaises(IndexError, lambda: c[-11])
        self.assertRaises(IndexError, lambda: c[-12])
        self.assertEqual(2, len(c._cache))

        # Make sure .func is settable at runtime...
        c.func = lambda i: "bbb"
        self.assertEqual("bbb", c[1])
        # ...and that we don't call it again.
        self.assertEqual(0, c[0])

    def testIter(self):
        c = cachingseq.CachingFuncSequence(lambda i: i, 10)
        # Cache empty on construction
        self.assertEqual(0, len(c._cache))

        self.assertEqual(10, len(c))
        self.assertEqual(list(range(10)), list(c))

        # Cache full after iteration
        self.assertEqual(10, len(c._cache))

    def testIncFunc(self):
        def first_func(x):
            assert x == 0
            return 1

        def inc_func(i, prev):
            return prev * 2

        c = cachingseq.CachingFuncSequence(first_func, 10, inc_func)
        self.assertEqual([1, 2, 4, 8, 16, 32, 64, 128, 256, 512], list(c))

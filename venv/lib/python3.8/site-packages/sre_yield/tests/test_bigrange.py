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

import sys
import unittest

import sre_yield

# fmt: off
TESTCASES = [
    (5,),
    (1, 5),
    (1, 5, 1),
    (1, 10, 2),
    (10, 1, -1),
    (10, -1, -1),
]
# fmt: on


def test_all():
    for t in TESTCASES:
        yield runner, t


def runner(packed_test):
    expected = list(range(*packed_test))
    print("expected", expected)
    actual = list(sre_yield._bigrange(*packed_test))
    print("actual", actual)
    assert expected == actual


def test_bignum():
    # xrange(start, stop) raises OverflowError in py2.7
    start = sys.maxsize
    stop = sys.maxsize + 5

    l = list(sre_yield._bigrange(start, stop))
    assert len(l) == 5

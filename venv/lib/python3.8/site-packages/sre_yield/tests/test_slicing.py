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

import itertools
import unittest

import sre_yield


class ExtractSliceType(object):
    """
    This exists so we can index obj[a:b:c] and get back a slice type without
    worrying about whether its arguments get mangled.
    """

    def __getitem__(self, n):
        return n


E = ExtractSliceType()

# Confirm that the new slice_indices function behaves like SliceType.indices

ARR = list(map(str, list(range(100))))
REG = sre_yield.AllStrings("\d{1}|1\d|2\d|3\d|4\d|5\d|6\d|7\d|8\d|9\d")


def test_prereqs():
    # TODO: Order of sre_yield may change at some point, to increment LSB
    # first.
    assert ARR == list(REG)


NUMS = [None, 0, 2, 5, 80, 90, -20, -10, -1, 100, 110]

TESTCASES = list(itertools.combinations(NUMS, 3))


def test_parity():
    for (start, stop, step) in TESTCASES:
        yield indices_runner, start, stop, step
        yield content_runner, start, stop, step


def indices_runner(start, stop, step):
    st = E[start:stop:step]
    expected = st.indices(100)
    print("expected", expected)
    actual = sre_yield.slice_indices(st, 100)
    print("actual", actual)
    print("array", ARR[st])
    assert expected == actual


def content_runner(start, stop, step):
    st = E[start:stop:step]
    indices = st.indices(100)
    print("indices", indices)
    expected = ARR[st]
    print("expected", expected)
    actual = list(REG[st])
    print("actual", actual)
    assert expected == actual

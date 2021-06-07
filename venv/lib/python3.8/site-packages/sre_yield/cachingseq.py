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
#
# vim: sw=2 sts=2 et


class CachingFuncSequence(object):
    def __init__(self, func, length, inc_func=None):
        """
        length: Length of this sequence.
        func: function(index)
        inc_func: function(index, value_of_previous)
        """

        self.func = func
        self.inc_func = inc_func
        self.length = length
        self._cache = {}

    def __getitem__(self, i):
        if i < 0:
            i += self.length
        if i < 0 or i >= self.length:
            raise IndexError()

        v = self._cache.get(i)
        if v is not None:
            return v

        if self.inc_func and i - 1 in self._cache:
            v = self.inc_func(i, self._cache[i - 1])
        else:
            v = self.func(i)

        self._cache[i] = v
        return v

    def __len__(self):
        return self.length

    def __iter__(self):
        for i in range(self.length):
            yield self[i]

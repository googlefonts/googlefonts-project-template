#!/usr/bin/env python2
#
# Copyright 2011-2016 Google Inc.
# Copyright 2018-2019 Tim Hatch
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

from math import log

try:
    long = long  # py2.7 compat
except NameError:
    long = int

__all__ = ["divmod_iter", "find_largest_power", "powersum"]


def find_largest_power(less_than, base):
    """
    Returns the largest power of `base` that is less than or equal to
    `less_than`.
    """
    # avoid div by zero
    if less_than == 0:
        return 0
    power = int(log(less_than) / log(base))
    return base ** power


def divmod_iter(x, by, chunk=None):
    """
    Generate successive (x % by); x /= by
    """
    if not isinstance(x, (int, long)):
        raise TypeError("`x` must be an int")
    if not isinstance(by, (int, long)):
        raise TypeError("`by` must be an int")
    if chunk is not None and not isinstance(chunk, (int, long)):
        raise TypeError("`chunk` must be an int")

    if x < by:
        return [x]

    if hasattr(x, "bit_length"):
        # crude log(2, x)
        divisions = x.bit_length() // by.bit_length()
    else:
        # This code path is intended for ints, but on <2.7 or alternate
        # implementation that does not support bit_length.  It is not covered by
        # current tests.
        divisions = log(x) // log(by)

    if divisions < 1024:
        return divmod_iter_basic(x, by, chunk)
    else:
        return divmod_iter_chunking(x, by, chunk)


def divmod_iter_chunking(x, by, chunk=None):
    """Generate successive (x % by); x /= by, but faster.

    If provided, |chunk| must be a power of |by| (otherwise it is determined
    automatically for 1024 per inner loop, based on analysis of bench_fastdivmod.py)
    """

    if by == 1:
        if x != 0:
            raise ValueError(
                "x=0 by=1 is allowed as a base case, but no other x may have " "by=1"
            )
        yield 0
        return

    if chunk is None:
        digits_per_chunk = 1024
        chunk = by ** digits_per_chunk
    else:
        digits_per_chunk = int(round(log(chunk) / log(by)))
        if (by ** digits_per_chunk) != chunk:
            raise ValueError("Chunk=%d must be a power of by=%d" % (chunk, by))

    assert digits_per_chunk > 0

    while x:
        x, this_chunk = divmod(x, chunk)
        # this_chunk = int(this_chunk)
        for _ in range(digits_per_chunk):
            this_chunk, m = divmod(this_chunk, by)
            yield m

            if this_chunk == 0 and x == 0:
                break


def divmod_iter_basic(x, by, chunk=None):
    """Generate successive (x % by); x /= by, the obvious way.

    Chunk is ignored.
    """
    while x:
        x, m = divmod(x, by)
        yield m


def powersum(x, low, high):
    # http://mikestoolbox.com/powersum.html
    xm1 = x - 1
    if xm1 == 0:
        return high - low + 1
    a = x ** (high + 1)
    b = x ** low
    return (a - b) // xm1

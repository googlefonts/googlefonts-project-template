#!/usr/bin/env python2
#
# Copyright 2011-2016 Google Inc.
# Copyright 2019 Tim Hatch
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
import random
import sys
import unittest

from sre_yield.fastdivmod import (
    divmod_iter,
    divmod_iter_basic,
    divmod_iter_chunking,
    find_largest_power,
    powersum,
)


class FastDivmodTest(unittest.TestCase):
    def test_find_largest_power(self):
        inputs = list(range(20))
        outputs = [find_largest_power(n, 2) for n in inputs]
        self.assertEqual(
            [0, 1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16, 16, 16], outputs
        )
        for (n, r) in zip(inputs[1:], outputs[1:]):
            self.assertLessEqual(r, n)

    def test_divmod_iter_switching(self):
        n = 2 ** 999 - 1
        count = 0
        v1 = []
        for v in divmod_iter(n, 2):
            count += 1
            v1.append(v)
        self.assertEqual(999, count)

        n = 2 ** 5000 - 1
        count = 0
        for v in divmod_iter(n, 2):
            count += 1
        self.assertEqual(5000, count)

    def test_divmod_iter_basic(self):
        v = divmod_iter_basic(1234, 10)
        self.assertEqual([4, 3, 2, 1], list(v))

    def test_basics(self):
        v = divmod_iter_chunking(1234, 10, 10)
        self.assertEqual([4, 3, 2, 1], list(v))

        v = divmod_iter_chunking(1234, 10, 100)
        self.assertEqual([4, 3, 2, 1], list(v))

        v = divmod_iter_chunking(1234, 10, 1000)
        self.assertEqual([4, 3, 2, 1], list(v))

    def test_bad_chunk_sizes(self):
        g = divmod_iter_chunking(1234, 10, 11)
        self.assertRaises(ValueError, lambda: next(g))

    def test_huge_number_1(self):
        v = divmod_iter_chunking(70110209207109374, 255)
        self.assertEqual([254, 254, 254, 254, 254, 254, 254], list(v))

    def test_huge_number_2(self):
        bignum = 1162523670191533212890624

        assert 255 ** 11 > bignum
        v = divmod_iter_chunking(bignum, 255, 255 ** 11)
        self.assertEqual(
            [254, 254, 254, 254, 254, 254, 254, 254, 254, 254], list(map(int, v))
        )

        assert 255 ** 9 < bignum
        v = divmod_iter_chunking(bignum, 255, 255 ** 9)
        self.assertEqual(
            [254, 254, 254, 254, 254, 254, 254, 254, 254, 254], list(map(int, v))
        )

    def test_huge_number_3(self):
        # this comes from '(?:[a-z]{,100}){,1000}'
        bignum = """
    139213503685244597631306906207129822718492493625765750638187
    422145221183403064209962632287600238213133585396115931858640
    397088297104215182062999160404977511404583694567955555693092
    391036971333019826503501322158903350288733318674828830355923
    498349990520184425817007399901916816311858669171276285561444
    611974044222858238401727502198428055979152449344112286300623
    398354626165755088011934430203904483146569680889715180212280
    311248065736587077721378474313074197745251681417858985013997
    376497357630123665969920348446238536919778668008199819062912
    209813948299604964182291901185954692403715976394605180757601
    560022975631875217270554188664960698779556224408710087910153
    388864065024676909905249179066904314719710199479087036266636
    486812383614637270104664243861433698340337270580924018081122
    972273102228069375608688078248241826230313720562480029591592
    545905659922877348183737039792218885258459176312595646776711
    788617588135808104772314342665930082373643028802685991791918
    926674139428325541968355964156198980323655477930065908769084
    934150892324757190759583195473467803980939672995083413559493
    917611589310185589660702265554321021096049823204800056794809
    973664250322419064982583391166478099231214825415574566705912
    248472806014274543228627658095513550473626381033015045051724
    852199012031842402809388416425577314128095191867797687492456
    679728567750494783710131249615739065586686514755989308471095
    118505256601463774083310772237026000
    """.replace(
            " ", ""
        ).replace(
            "\n", ""
        )
        bignum = int(bignum)
        bignum2 = 3268647867246256383381332100041691484373976788312974266629140102414955744756908184404049903032490380904202638084876187965749304595652472251350

        v = divmod_iter_chunking(bignum, bignum2)
        # there are at least 3 terms
        next(v)
        next(v)
        next(v)
        for i in v:
            pass
        # ...and it finishes


def test_correctness_big_numbers():
    random.seed(1)
    for _ in range(100):
        x = random.randint(1, 2 ** 32)
        for base in (2, 10, 255, 256):
            for chunk in (base, base ** 2, base ** 3, base ** 4):
                yield runner, x, base, chunk

    for _ in range(10):
        x = random.randint(1, 2 ** 32) * sys.maxsize ** 6
        for base in (2, 10, 255, 256):
            for chunk in (base, base ** 2, base ** 3, base ** 4):
                yield runner, x, base, chunk


def runner(x, base, chunk):
    try:
        zip_longest = itertools.izip_longest
    except AttributeError:
        zip_longest = itertools.zip_longest
    for i, j in zip_longest(
        divmod_iter_chunking(x, base, chunk), divmod_iter_basic(x, base)
    ):
        if i is None:
            print("phooey")
        else:
            assert i == j


def test_powersum():
    for base in (1, 2, 7, 256):
        yield powersum_runner, base, 0, 0
        yield powersum_runner, base, 0, 1
        yield powersum_runner, base, 1, 2
        yield powersum_runner, base, 1, 10
        yield powersum_runner, base, 99, 104
        yield powersum_runner, base, 1, 2 ** 14


def powersum_runner(base, low, high):
    expected = sum([base ** i for i in range(low, high + 1)])
    actual = powersum(base, low, high)
    assert expected == actual

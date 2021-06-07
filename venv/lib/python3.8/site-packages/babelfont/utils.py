import math


def _toFlagBits(value):
    modifier = 1
    bits = []
    while value > 0:
        if value & 1:
            bits.append( int(math.log(modifier)/math.log(2)))
        modifier = modifier << 1
        value = value >> 1
    return bits

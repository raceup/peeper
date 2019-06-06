# -*- coding: utf-8 -*-

"""CAN utils"""

import codecs
import binascii
import struct


def apply_functions(lst, functions):
    """
    :param lst: list of values
    :param functions: list of functions to apply to each value.
    Each function has 2 inputs: index of value and value
    :return: [func(x) for x in lst], i.e apply the respective function to each
    of the values
    """

    assert len(lst) == len(functions)

    for i, item in enumerate(lst):
        func = functions[i]  # get function
        lst[i] = func(i, item)  # apply function

    return lst


def hex2dec(x):
    x = int(str(x), 16)
    return x


def twos_complement(val, bits):
    # if sign bit is set e.g., 8bit: 128-255
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)  # compute negative value

    return val  # return positive value as is


def dec2hex(x):
    x = int(x)  # parse from string
    return hex(x).split('x')[-1]


def byte2hex(x):
    x = int(x)
    if x < 0:
        x += 256

    return dec2hex(x)


def bytes2int32(bytes_list, convert_to='I'):
    ints = [
        hex2dec(x)
        for x in bytes_list
    ]
    raw_list = binascii.hexlify(bytearray(ints))
    raw = struct.unpack(convert_to, codecs.decode(raw_list, 'hex_codec'))
    result = int(raw[0])
    return result

# -*- coding: utf-8 -*-

"""Parses CAN data"""

from parsers.can.utils import apply_functions, twos_complement


class BytesParser:
    """ Parses raw bytes """

    NANO_SCALING = 10 ** -9
    MILLI_SCALING = 10 ** -6
    MICRO_SCALING = 10 ** -3

    def __init__(self, byte_0=None, byte_1=None, byte_2=None, byte_3=None,
                 byte_4=None, byte_5=None, byte_6=None, byte_7=None):
        self.bytes = [
            byte_0, byte_1, byte_2, byte_3, byte_4, byte_5, byte_6, byte_7
        ]

    @staticmethod
    def apply_scaling(x, scaling):
        return x * scaling

    @staticmethod
    def from_nano(x):
        return BytesParser.apply_scaling(x, BytesParser.NANO_SCALING)

    @staticmethod
    def from_micro(x):
        return BytesParser.apply_scaling(x, BytesParser.MICRO_SCALING)

    @staticmethod
    def from_milli(x):
        return BytesParser.apply_scaling(x, BytesParser.MILLI_SCALING)

    @staticmethod
    def toggle_endianness(values):
        """Toggle endianness of values

        :param values: list of bytes, ints ...
        :return: values with other endianness (little -> big, big -> little)
        """

        return list(reversed(values))

    @staticmethod
    def to_binary(val, expected_length=8, append_left=True):
        """Converts decimal value to binary

        :param val: decimal
        :param expected_length: length of data
        :param append_left: append extra 0s to the left? or to the right?
        :return: binary value
        """

        val = bin(val)[2:]  # to binary

        while len(val) < expected_length:
            if append_left:
                val = "0" + val
            else:
                val = val + "0"

        return val

    @staticmethod
    def hexs_to_dec(hex_values):
        try:
            return int(hex_values, 16)
        except:  # is a list
            if isinstance(hex_values, list):
                all_together = ''.join(hex_values)
                return BytesParser.hexs_to_dec(all_together)

            return []

    @staticmethod
    def parse_bytes(raw_values, lengths, scalings):
        while len(raw_values) < 8:
            raw_values.append('0')

        return BytesParser(*raw_values).parse(lengths, scalings)

    @staticmethod
    def parse_string(string, lengths, scalings):
        raw_values = string.split()
        return BytesParser.parse_bytes(raw_values, lengths, scalings)

    def split_by_lengths(self, lenghts):
        start_index = 0
        current_len = 0
        raw_values = []

        while start_index < len(self.bytes) and current_len < len(lenghts):
            raw_len = lenghts[current_len]
            end_index = start_index + raw_len
            raw_values.append(self.bytes[start_index: end_index])

            start_index = end_index
            current_len += 1

        return raw_values

    def parse(self, lengths, scalings=None, two_complement=False,
              toggle_endianness=True):
        def func(index, raw_byte):
            x = raw_byte

            if toggle_endianness:
                x = self.toggle_endianness(x)

            x = BytesParser.hexs_to_dec(x)

            if two_complement:
                x = twos_complement(x, 16)

            if scalings:
                x *= scalings[index]

            return x

        transformation_functions = len(lengths) * [func]

        raw_values = self.split_by_lengths(lengths)
        raw_values = apply_functions(raw_values, transformation_functions)

        return raw_values

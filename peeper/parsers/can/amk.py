# -*- coding: utf-8 -*-

"""Parses AMK data"""

from parsers.can.utils import hex2dec, bytes2int32, twos_complement
from parsers.can.models import BytesParser


class AMKParser(BytesParser):
    @staticmethod
    def bytes2int32(byte_list):
        byte_list = [
            hex2dec(x)
            for x in byte_list
        ]

        least_sign = int(byte_list[0])
        most_sign = int(byte_list[1])
        factor = 2 ** 8

        return factor * most_sign + least_sign

    def get_as_setpoint(self):
        byte_num = 2
        num_values = 4
        scaling = 0.1  # deci-percentage

        raw_values = self.split_by_lengths(
            num_values * [byte_num]
        )

        raw_control = hex2dec(raw_values[0][1])  # first byte is always 0
        raw_values[0] = self.to_binary(raw_control, 8)  # control is in bits

        raw_values[1] = self.bytes2int32(raw_values[1])  # target velocity

        raw_values[2] = self.bytes2int32(raw_values[2])  # add 2 extra bytes to convert to int32
        raw_values[2] = twos_complement(raw_values[2], 16) * scaling

        raw_values[3] = bytes2int32(raw_values[3] + ['0', '0'])  # add 2 extra bytes to convert to int32
        raw_values[3] = twos_complement(raw_values[3], 16) * scaling

        return raw_values

    def get_as_actual_values_1(self):
        byte_num = 2
        num_values = 4
        scaling = 107.2 / 16384.0

        raw_values = self.split_by_lengths(
            num_values * [byte_num]
        )

        raw_control = hex2dec(raw_values[0][1])  # first byte is always 0
        raw_values[0] = self.to_binary(raw_control, 8)  # status is in bits

        raw_values[1] = self.bytes2int32(raw_values[1])  # actual velocity
        raw_values[1] = twos_complement(raw_values[1], 16) * 0.01  # x100 rpm

        raw_values[2] = twos_complement(self.bytes2int32(raw_values[2]), 16) * scaling  # torque current
        raw_values[3] = twos_complement(self.bytes2int32(raw_values[3]), 16) * scaling  # magnet current

        calc_torque = 0.243 * raw_values[2] + (9 * 10 ** -4) * raw_values[2] * raw_values[3]
        raw_values.append(calc_torque)

        return raw_values

    def get_as_actual_values_2(self):
        byte_num = 2
        num_values = 4

        raw_values = self.parse(
            num_values * [byte_num], [10 ** -1, 10 ** -1, 1, 10 ** -1],
            toggle_endianness=False, two_complement=True
        )
        raw_values[2] = self.to_binary(raw_values[2], 16)  # in bits
        return raw_values

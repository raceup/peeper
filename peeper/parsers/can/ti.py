# -*- coding: utf-8 -*-

"""Parses TI data"""

from parsers.can.models import BytesParser
from parsers.can.utils import bytes2int32


class TIParser(BytesParser):
    def get_as_potentiometers(self):
        scaling = 10 ** -7

        throttle = bytes2int32(self.bytes[:4])
        throttle *= scaling

        brake = bytes2int32(self.bytes[4:])
        brake *= scaling

        return [
            throttle,
            brake
        ]

    def get_as_steering(self):
        scaling = 10 ** -7

        steering = bytes2int32(self.bytes[:4])
        steering *= scaling
        steering = steering * 72 / 43 - 15804 / 43  # empirical value

        ti_core_temp = bytes2int32(self.bytes[4:])
        ti_core_temp *= scaling
        ti_core_temp -= 100.0  # empirical value

        return [
            steering,
            ti_core_temp
        ]

    def get_as_brakes(self):
        scaling = 10 ** -7

        front_break = bytes2int32(self.bytes[:4])
        front_break *= scaling
        front_break -= 111.25

        rear_break = bytes2int32(self.bytes[4:])
        rear_break *= scaling
        rear_break -= 111.25

        return [front_break, rear_break]

    def get_as_suspensions_1(self):
        byte_num = 4
        num_values = 2

        susps = self.parse(
            num_values * [byte_num], [10 ** -4, 10 ** -4],
            toggle_endianness=True, two_complement=True
        )
        for i, susp in enumerate(susps):
            susps[i] = (susp - 434) / 70

        return susps

    def get_as_suspensions_2(self):
        return self.get_as_suspensions_1()

    def get_as_current_sensor(self):
        raw_curr = bytes2int32(self.bytes[:4], 'f')
        real_curr = 100 * ((raw_curr * 5 / 5.1) - 2.5)
        real_curr = - real_curr  # sensor was mounted the other way around
        return [real_curr]

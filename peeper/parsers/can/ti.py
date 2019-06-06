# -*- coding: utf-8 -*-

"""Parses TI data"""

from parsers.can.models import BytesParser
from parsers.can.utils import bytes2int32, twos_complement


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
        potentiometers_length_mm = 220

        right = bytes2int32(self.bytes[:4], 'f')
        right *= -10 ** -2 / (14 * 2)
        right *= potentiometers_length_mm

        left = bytes2int32(self.bytes[4:], 'f')
        left *= 10 ** -2 / (9 * 2)
        left *= potentiometers_length_mm

        return [
            right, left
        ]

    def get_as_suspensions_2(self):
        return self.get_as_suspensions_1()

    def get_as_current_sensor(self):
        raw_curr = bytes2int32(self.bytes[:4], 'I')
        real_curr = (raw_curr * 5 / 5.1) - 2.5
        real_curr = - real_curr  # sensor was mounted the other way around
        return [real_curr]

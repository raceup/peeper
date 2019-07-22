# -*- coding: utf-8 -*-

"""Parses TI data"""

from parsers.can.models import BytesParser
from parsers.can.utils import bytes2short


class TIParser(BytesParser):
    def get_all(self):
        throttle = bytes2short(self.bytes[0:2])
        brake = bytes2short(self.bytes[2:4])
        steering = bytes2short(self.bytes[4:6]) - 105  # offset
        speed_kmh = bytes2short(self.bytes[6:8])

        return [
            throttle,
            brake,
            steering,
            speed_kmh
        ]

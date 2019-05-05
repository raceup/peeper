# -*- coding: utf-8 -*-

"""Parses YOLO .csv file"""

from parsers.can.utils import byte2hex, dec2hex
from parsers.logs.models import LineLogParser
from parsers.models.can import CanbusMessage


class YOLOLogParser(LineLogParser):
    def parse_file(self, skip_lines=1):
        super().parse_file(skip_lines=skip_lines)

    def parse_line(self, line):
        tokens = line.strip().split(',')  # raw csv format
        real_time = float(tokens[0]) / (1000 * 1000)  # us -> s

        if len(tokens) == 12:  # time + ID + flags + CAN data
            data = tokens[4:]
            data = list(map(byte2hex, data))

            return CanbusMessage(
                0,
                dec2hex(tokens[1]),  # ID is in dec format
                int(tokens[3]),
                data,
                real_time,
                'R'
            )

        return None

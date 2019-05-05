# -*- coding: utf-8 -*-

"""Parses Kvaser output window from a .log file"""

from parsers.logs.models import LineLogParser
from parsers.models.can import CanbusMessage


class KvaserLogParser(LineLogParser):
    def parse_line(self, line):
        tokens = line.split()

        if 5 <= len(tokens) <= 5 + 8:  # min CAN len is 0, max is 8
            data = tokens[3:-2]

            return CanbusMessage(
                tokens[0],
                tokens[1],
                tokens[2],
                data,
                tokens[-2],
                tokens[-1]
            )

        return None

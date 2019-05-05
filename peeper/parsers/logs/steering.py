# -*- coding: utf-8 -*-

"""Parses steering wheel output window from a .log file"""

from parsers.logs.models import LineLogParser
from parsers.models.can import CanbusMessage


def parse_can_message(message):
    message = message.strip()  # remove spurious blanks
    can_bytes = message.split(' ')
    can2hex = lambda x: hex(int(x))[2:].upper()
    hex_bytes = map(can2hex, can_bytes)  # dec -> hex
    return list(hex_bytes)


class SteeringWheelLogParser(LineLogParser):
    CAN_IDS = ['283', '285', '184', '284', '286', '185', '287', '289', '188',
               '288', '28A', '189']

    def parse_file(self, skip_lines=2):
        super().parse_file(skip_lines=skip_lines)

    def parse_line(self, line):
        tokens = line.split(',')[:-1]  # simple CSV format, last is null
        raw_messages = tokens[12:]  # first 12 are floats
        can_messages = []

        for i, raw_message in enumerate(raw_messages):
            ms_time = float(tokens[0])
            s_time = ms_time / 1000.0
            data = parse_can_message(raw_message)

            message = CanbusMessage(
                0,
                self.CAN_IDS[i],
                len(data),  # DLC
                data,  # bytes all together
                s_time,
                'R'  # all messages are sent from someone else
            )

            can_messages.append(message)

        return can_messages

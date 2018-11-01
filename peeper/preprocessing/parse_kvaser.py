# -*- coding: utf-8 -*-

"""Parses Kvaser Output window from a .log file"""

import argparse
import os

from hal.streams.pretty_table import pretty_format_table
from parse import parse

from preprocessing.ellipse2n import get_STATUS_01, get_IMU_INFO, get_IMU_ACCEL

DATA_FIELD_FORMATTERS = [
    " {:d}    {:d}         {:d}" + "  {:x}" * i + "    " * (8 - i) +
    "     {:f} {:w}"
    for i in range(9)  # message data field can have 0 to 8 bytes
]


class CanbusMessage:
    MESSAGE_IN = "RX"
    MESSAGE_OUT = "TX"

    def __init__(self, can_channel, msg_id, dlc, data, timestamp, trx):
        """
        :param can_channel: Number of channel
        :param msg_id: Id of message
        :param dlc: DLC
        :param data: list of bytes in data field of message
        :param timestamp: time of message (seconds)
        :param trx: R or T
        """

        self.channel = can_channel
        self.msg_id = msg_id
        self.dlc = dlc
        self.data = list(data)
        self.timestamp = timestamp
        self.trx = self.MESSAGE_IN if trx.lower() == "r" else self.MESSAGE_OUT

        while len(self.data) < 8:
            self.data.append(0)  # null value

    def __str__(self):
        return " ".join([
            str(val) for val in
            self.get_values()
        ])

    def get_values(self):
        values = [
                     self.channel, self.msg_id, self.dlc
                 ] + self.data + [self.timestamp, self.trx]
        return values

    def parse_data(self, func):
        """Parses data field to get real value

        :param func: function that accepts 8 args (byte 0, ...)
        :return: Result of parsing
        """

        return func(*self.data)

    @staticmethod
    def parse_kvaser(raw_line):
        """Parses raw Kvaser data line

        :param raw_line: line of Kvaser output window
        :return: CanbusMessage
        """

        for formatter in DATA_FIELD_FORMATTERS:
            parsed = parse(formatter, raw_line)
            if parsed:
                parsed = parsed.fixed
                data = parsed[3:-2]

                return CanbusMessage(
                    parsed[0],
                    parsed[1],
                    parsed[2],
                    data,
                    parsed[-2],
                    parsed[-1]
                )

        return None


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-i <input file> '
                                           '-h for full usage')
    parser.add_argument('-i', dest='file',
                        help='file to parse', required=True)
    return parser


def parse_args(parser):
    """
    :param parser: ArgumentParser
        Object that holds cmd arguments.
    :return: tuple
        Values of arguments.
    """

    args = parser.parse_args()
    file = str(args.file)

    assert os.path.exists(file)

    return file


def parse_messages(messages, msg_id, func, result_labels):
    """Parses Ellipse2N messages

    :param messages: list of messages
    :param msg_id: ID of messages to parse
    :param func: callable to parse data
    :param result_labels: labels of result
    :return: Shows parsed data
    """

    messages = [
        message.get_values() + list(message.parse_data(func))
        for message in messages
        if message.msg_id == msg_id  # just this ID
    ]

    labels = ["Channel", "ID (hex)", "DLC"] + [
        "Byte " + str(i)
        for i in range(8)
    ] + ["Timestamp (s)",
         "Transmission"] + \
             result_labels

    print(pretty_format_table(labels, messages))


def parse_file(path):
    """Parses .log file

    :param path: path to file
    :return: Shows file contents
    """

    lines = open(path, "r").readlines()
    messages = [
        CanbusMessage.parse_kvaser(line)
        for line in lines
    ]

    parse_messages(messages, 100, get_STATUS_01,
                   ["TIME_STAMP (s)", "GENERAL_STATUS", "CLOCK_STATUS"])
    parse_messages(messages, 120, get_IMU_INFO,
                   ["TIME_STAMP (s)", "IMU_STATUS", "TEMPERATURE (°C)"])
    parse_messages(messages, 121, get_IMU_ACCEL,
                   ["ACCEL_X (m/s²)", "ACCEL_Y (m/s²)", "ACCEL_Z (m/s²)"])


def main():
    file = parse_args(create_args())
    parse_file(file)


if __name__ == '__main__':
    main()
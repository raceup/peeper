# -*- coding: utf-8 -*-

"""Parses Kvaser output window from a .log file"""


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
        self.data = data
        self.timestamp = timestamp
        self.trx = self.MESSAGE_IN if trx.lower() == 'r' else self.MESSAGE_OUT

        while len(self.data) < 8:
            self.data.append(0)  # null value at the end

    def __str__(self):
        return ' '.join([
            str(val) for val in
            self.get_values()
        ])

    def get_values(self):
        values = [
                     self.channel, self.msg_id, self.dlc
                 ] + self.data + [self.timestamp, self.trx]
        return values

    def parse_data(self, bytes_parser, func):
        data_parser = bytes_parser(*self.data)
        return func(data_parser)

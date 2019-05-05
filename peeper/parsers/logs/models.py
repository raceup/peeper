# -*- coding: utf-8 -*-

"""Parses CAN .log file"""

import abc
import json


def get_as_hex_id(x):
    x = str(x).lower()

    if x.startswith('0x'):
        return int(x.split('x')[-1])

    try:
        return hex(int(x)).split('x')[-1]
    except:
        dec_val = int(x, 16)
        return hex(dec_val).split('x')[-1]


def same_id(x, y):
    x = get_as_hex_id(x)
    y = get_as_hex_id(y)
    return x == y


class LogParser:
    DEFAULT_LABELS = [
                         "Byte " + str(i) for i in range(8)
                     ] + ["Timestamp (s)"]

    def __init__(self, file_path):
        self.file_path = file_path
        self.messages = []
        self.parse_file()

    def find_all_ids(self):
        ids = [
            int(str(message.msg_id), 16)
            for message in self.messages
        ]
        return sorted(set(ids))

    def filter_by_id(self, msg_id):
        return [
            message
            for message in self.messages
            if same_id(message.msg_id, msg_id)
        ]

    def get_messages(self, bytes_parser, func, msg_id=None):
        if msg_id:
            messages = self.filter_by_id(msg_id)
        else:
            messages = self.messages

        messages = [
            message.get_values() + list(message.parse_data(bytes_parser, func))
            for message in messages
        ]  # get data
        messages = [
            content[3:11] +  # raw bytes
            [content[11]] +  # time stamp
            content[13:]  # everything else
            for content in messages
        ]
        return messages

    @abc.abstractmethod
    def parse_file(self):
        pass


class LineLogParser(LogParser):
    def parse_file(self, skip_lines=0):
        lines = open(self.file_path, 'r').readlines()
        lines = lines[skip_lines:]

        self.messages = []

        for line in lines:
            parsed = self.parse_line(line)
            if isinstance(parsed, list):
                self.messages += parsed
            else:
                self.messages.append(parsed)

    @abc.abstractmethod
    def parse_line(self, line):
        pass


class JsonLogParser(LogParser):
    def parse_file(self):
        self.messages = json.load(self.file_path)  # it's a array

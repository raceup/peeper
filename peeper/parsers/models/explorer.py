# -*- coding: utf-8 -*-

""" Parses CAN log file """

from hal.streams.pretty_table import pretty_format_table
from matplotlib import pyplot as plt
import numpy as np


class LogExplorer:
    def __init__(self, file_path, file_parser, message_classes):
        self.parser = file_parser(file_path)
        self.message_classes = message_classes

    def get_messages(self, bytes_parser, func, msg_id=None):
        return self.parser.get_messages(
            bytes_parser,
            func,
            msg_id
        )

    def pretty_print(self, messages_list, labels_list):
        for messages, labels in zip(messages_list, labels_list):
            labels = self.parser.DEFAULT_LABELS + labels
            table = pretty_format_table(labels, messages)
            print(table)

    @staticmethod
    def plot(messages, labels, time_index, y_indexes):
        timestamps = [
            float(message[time_index])
            for message in messages
        ]

        for i, label in enumerate(labels):
            try:
                y_col = y_indexes[i]  # column to get
                y = [
                    float(message[y_col])
                    for message in messages
                ]

                plt.plot(timestamps, y, label=label)
            except:
                pass  # todo print exc

        plt.xlabel('Timestamp (s)')
        plt.legend()

    @staticmethod
    def plot_gps(lats, longs, title='GPS'):
        plt.plot(lats, longs, label='GPS')

        plt.title(title)

        plt.xlabel('Latitude (dec)')
        plt.ylabel('Longitude (dec)')
        plt.legend()

        plt.tick_params(axis='x', labelrotation=90)
        plt.subplots_adjust(bottom=0.15)

# -*- coding: utf-8 -*-

""" Parses CAN log file """
import math
import os

import pandas as pd
from hal.streams.pretty_table import pretty_format_table
from matplotlib import pyplot as plt


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

    def save_to_csv(self, messages, labels, file_path):
        df = pd.DataFrame(
            messages,
            columns=self.parser.DEFAULT_LABELS + labels
        )
        df.to_csv(file_path, index=False)

    def save_many_to_csv(self, messages_list, labels_list, names_list, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for (messages, labels, file_name) in zip(messages_list, labels_list, names_list):
            file_path = '{}.csv'.format(file_name)  # .csv extension
            file_path = os.path.join(folder_path, file_path)

            self.save_to_csv(messages, labels, file_path)

    def plot(self, messages_list, labels_list):
        for i in range(1, 8, 2):
            plt.subplot(2, 2, int(i / 2) + 1)  # select subplot

            # labels = [labels_list[i][1]]
            # y_indexes = [10, 11, 12, 13]

            labels = [labels_list[i][0], labels_list[i][1], labels_list[i][3]]
            y_indexes = [9, 10, 12]

            self._plot(messages_list[i], labels, time_index=8, y_indexes=y_indexes)

        # show plots
        plt.show()

    def get_lists(self, message_classes):
        messages_list = [
            self.get_messages(
                message_class['bytes parser'],
                message_class['func'],
                msg_id=message_class['id']
            )
            for message_class in message_classes
        ]  # parse
        labels_list = [
            message_class['labels']
            for message_class in message_classes
        ]
        files_list = [
            message_class['filename']
            for message_class in message_classes
        ]
        return messages_list, labels_list, files_list

    def save(self, messages_list, labels_list, files_list, output_folder):
        if output_folder:
            print('Saving to {}'.format(output_folder))
            self.save_many_to_csv(
                messages_list,
                labels_list,
                files_list,
                output_folder
            )

    @staticmethod
    def _min2sec(seconds, seconds_in_minute=60):
        time_sec = int(seconds % seconds_in_minute)
        time_min = int(math.floor(seconds / seconds_in_minute))
        return '{}\' {}"'.format(time_min, time_sec)

    @staticmethod
    def _plot(messages, labels, time_index, y_indexes):
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

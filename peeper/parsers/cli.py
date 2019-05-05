# -*- coding: utf-8 -*-

""" Parses CAN log file """

import argparse
import os

from matplotlib import pyplot as plt

from parsers.can.amk import AMKParser
from parsers.can.ti import TIParser
from parsers.logs.yolo import YOLOLogParser
from parsers.models.explorer import LogExplorer


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


def get_plot(messages, labels, time_index, y_indexes):
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

            yield (timestamps, y, label)
        except:
            pass  # todo print exc


def parse_file(file_path):
    message_classes = [
        {
            "id": "13",
            "labels": ["throttle (%)", "brake (%)"],
            "bytes parser": TIParser,
            "func": TIParser.get_as_potentiometers
        },
        {
            "id": "23",
            "labels": ["current sensor (A)"],
            "bytes parser": TIParser,
            "func": TIParser.get_as_current_sensor
        },
        {
            "id": "283",
            "labels": ["FL actual velocity (rpm)", "FL calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        },
        {
            "id": "284",
            "labels": ["FR actual velocity (rpm)", "FR calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        },
        {
            "id": "287",
            "labels": ["RL actual velocity (rpm)", "RL calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        },
        {
            "id": "288",
            "labels": ["RR actual velocity (rpm)", "RR calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        }
    ]

    explorer = LogExplorer(file_path, YOLOLogParser, message_classes)

    messages_list = [
        explorer.get_messages(
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
        message_class['id']
        for message_class in message_classes
    ]

    # save to .csv
    output_folder = os.path.join(os.getcwd(), 'out')
    explorer.save_many_to_csv(
        messages_list,
        labels_list,
        files_list,
        output_folder
    )

    # print all classes
    # explorer.pretty_print(messages_list, labels_list)

    # 2 x 2 plots
    for i in range(1, 5, 1):
        plt.subplot(2, 2, i)  # select subplot

        explorer.plot(messages_list[0], labels_list[0], time_index=8, y_indexes=[9, 10])  # throttle brake
        explorer.plot(messages_list[1], labels_list[1], time_index=8, y_indexes=[9])  # current
        explorer.plot(messages_list[i + 1], labels_list[i + 1], time_index=8, y_indexes=[10, 13])

    # show plots
    plt.show()


def main():
    file_path = parse_args(create_args())
    parse_file(file_path)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

""" Parses CAN log file """

import argparse
import os

from hal.files.models.files import Document
from hal.files.models.system import ls_recurse, is_file
from matplotlib import pyplot as plt

from config.amk import AMK_VALUES_1, Motors, AMK_VALUES_2
from parsers.can.amk import AMKParser
from parsers.logs.yolo import YOLOLogParser
from parsers.models.explorer import LogExplorer

DEFAULT_OUTPUT_FOLDER = os.path.join(os.getcwd(), 'out')


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-i <input file> '
                                           '-h for full usage')
    parser.add_argument('-i', dest='file',
                        help='file to parse', required=True)
    parser.add_argument('-o', dest='out',
                        help='output folder', default=DEFAULT_OUTPUT_FOLDER, required=False)
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
    out = str(args.out)

    assert os.path.exists(file)

    return file, out


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


def get_explorer(file_path):
    message_classes = [
        {
            "id": AMK_VALUES_1[Motors.FL],
            "filename": "AMK1_FL",
            "labels": ["FL status", "FL actual velocity (x100 rpm)", "FL torque curr (A)", "FL mag curr (A)",
                       "FL calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        },
        {
            "id": AMK_VALUES_2[Motors.FL],
            "filename": "AMK2_FL",
            "labels": ["FL T motor (°C)", "FL T inverter (°C)", "FL error", "FL T IGBT (°C)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_2
        },
        {
            "id": AMK_VALUES_1[Motors.FR],
            "filename": "AMK1_FR",
            "labels": ["FR status", "FR actual velocity (x100 rpm)", "FR torque curr (A)", "FR mag curr (A)",
                       "FR calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        },
        {
            "id": AMK_VALUES_2[Motors.FR],
            "filename": "AMK2_FR",
            "labels": ["FR T motor (°C)", "FR T inverter (°C)", "FR error", "FR T IGBT (°C)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_2
        },
        {
            "id": AMK_VALUES_1[Motors.RL],
            "filename": "AMK1_RL",
            "labels": ["RL status", "RL actual velocity (x100 rpm)", "RL torque curr (A)", "RL mag curr (A)",
                       "RL calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        },
        {
            "id": AMK_VALUES_2[Motors.RL],
            "filename": "AMK2_RL",
            "labels": ["RL T motor (°C)", "RL T inverter (°C)", "RL error", "RL T IGBT (°C)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_2
        },
        {
            "id": AMK_VALUES_1[Motors.RR],
            "filename": "AMK1_RR",
            "labels": ["RR status", "RR actual velocity (x100 rpm)", "RR torque curr (A)", "RR mag curr (A)",
                       "RR calc torque (Nm)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_1
        },
        {
            "id": AMK_VALUES_2[Motors.RR],
            "filename": "AMK2_RR",
            "labels": ["RR T motor (°C)", "RR T inverter (°C)", "RR error", "RR T IGBT (°C)"],
            "bytes parser": AMKParser,
            "func": AMKParser.get_as_actual_values_2
        }
    ]  # todo read .json

    explorer = LogExplorer(file_path, YOLOLogParser, message_classes)
    return explorer, message_classes


def plot(explorer, messages_list, labels_list):
    for i in range(1, 8, 2):
        plt.subplot(2, 2, int(i / 2) + 1)  # select subplot

        # labels = [labels_list[i][1]]
        # y_indexes = [10, 11, 12, 13]

        labels = [labels_list[i][0], labels_list[i][1], labels_list[i][3]]
        y_indexes = [9, 10, 12]

        explorer.plot(messages_list[i], labels, time_index=8, y_indexes=y_indexes)

    # show plots
    plt.show()


def save(explorer, messages_list, labels_list, files_list, output_folder):
    if output_folder:
        print('Saving to {}'.format(output_folder))
        explorer.save_many_to_csv(
            messages_list,
            labels_list,
            files_list,
            output_folder
        )


def print_log(explorer, messages_list, labels_list):
    explorer.pretty_print(messages_list, labels_list)


def get_lists(explorer, message_classes):
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
        message_class['filename']
        for message_class in message_classes
    ]
    return messages_list, labels_list, files_list


def main():
    folder_path, out_folder = parse_args(create_args())
    file_extension = ".csv"
    files = sorted([
        file
        for file in ls_recurse(folder_path)
        if is_file(file) and Document(file).extension == file_extension
    ])

    for file_path in files:
        output_folder_name = os.path.basename(file_path).replace(file_extension, '')
        output_folder = os.path.join(out_folder, output_folder_name)

        explorer, message_classes = get_explorer(file_path)
        messages_list, labels_list, files_list = get_lists(explorer, message_classes)
        plot(explorer, messages_list, labels_list)
        save(explorer, messages_list, labels_list, files_list, output_folder)
        # print_log(explorer, messages_list, labels_list)


if __name__ == '__main__':
    main()

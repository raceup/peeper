# -*- coding: utf-8 -*-

""" Parses CAN log file """

import argparse
import json
import os

from hal.files.models.files import Document
from hal.files.models.system import ls_recurse, is_file

from parsers.logs.yolo import YOLOLogParser
from parsers.models.explorer import LogExplorer

# needed dynamic import:

THIS_FOLDER = os.getcwd()
DEFAULT_OUTPUT_FOLDER = os.path.join(THIS_FOLDER, 'out')
DEFAULT_CONFIG_FILE = os.path.join(THIS_FOLDER, 'config.json')


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
    parser.add_argument('-c', dest='config',
                        help='config messages', default=DEFAULT_CONFIG_FILE, required=False)
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
    config = str(args.config)

    assert os.path.exists(file)
    assert os.path.exists(config)

    return file, out, config


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


def get_explorer(file_path, config_file):
    with open(config_file, 'r') as json_data:
        data = json.load(json_data)
        message_classes = data["messages"]
        for i, message_class in enumerate(message_classes):
            byte_parser = globals()[message_class["bytes parser"]]
            func = getattr(byte_parser, message_classes[i]["func"])

            message_classes[i]["bytes parser"] = byte_parser
            message_classes[i]["func"] = func

        explorer = LogExplorer(file_path, YOLOLogParser, message_classes)
        return explorer, message_classes


def main():
    folder_path, out_folder, config = parse_args(create_args())
    file_extension = ".csv"
    files = sorted([
        file
        for file in ls_recurse(folder_path)
        if is_file(file) and Document(file).extension == file_extension
    ])  # finds files

    for file_path in files:
        output_folder_name = os.path.basename(file_path).replace(file_extension, '')
        output_folder = os.path.join(out_folder, output_folder_name)

        explorer, message_classes = get_explorer(file_path, config)
        messages_list, labels_list, files_list = explorer.get_lists(message_classes)
        # explorer.plot(messages_list, labels_list)
        explorer.save(messages_list, labels_list, files_list, output_folder)


if __name__ == '__main__':
    main()

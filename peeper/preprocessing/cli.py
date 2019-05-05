# -*- coding: utf-8 -*-

"""Command line interface"""

import argparse
import os

from hal.files.models.system import is_folder, ls_recurse, \
    get_parent_folder_name
from hal.streams.logger import log_message

from peeper.preprocessing.models import Processer


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-i <input folder> '
                                           '-h for full usage')
    parser.add_argument('-i', dest='dir',
                        help='directory to use', required=True)
    return parser


def parse_args(parser):
    """
    :param parser: ArgumentParser
        Object that holds cmd arguments.
    :return: tuple
        Values of arguments.
    """

    args = parser.parse_args()
    directory = str(args.dir)

    assert os.path.exists(directory)

    return directory


def get_output_file(folder):
    """Finds output file suitable for input folder

    :param folder: input folder
    :return: output file
    """

    folders = folder.split(os.path.sep)
    data_time = folders[-2]
    data_day = folders[-3]
    output_file = "sensors.csv"
    output_folder = folder
    for _ in range(4):
        output_folder = os.path.dirname(output_folder)
    output_folder = os.path.join(output_folder, "output", data_day, data_time)
    output_file = os.path.join(output_folder, output_file)

    if not os.path.exists(output_folder):  # create necessary folders
        os.makedirs(output_folder)

    if os.path.exists(output_file):  # remove any previous outputs
        os.remove(output_file)

    return output_file


def pre_process_test(folder):
    """Pre-process test

    :param folder: test folder
    :return: Saves processed data
    """

    log_message("Pre-processing", get_parent_folder_name(folder))
    output_file = get_output_file(folder)

    driver = Processer(folder)
    driver.combine_into(output_file)

    log_message("Merged into", output_file)


def pre_process_day(folder):
    """Pre-process day

    :param folder: day folder
    :return: Saves processed data
    """

    folders = [
        folder
        for folder in ls_recurse(folder)
        if is_folder(folder)
    ]
    folders = [
        folder
        for folder in folders
        if "Accelerometer.csv" in os.listdir(folder)
    ]

    for folder in folders:
        pre_process_test(folder)


def main():
    """CLI driver

    :return: Creates args and execute pre-processing
    """
    folder = parse_args(create_args())
    pre_process_day(folder)


if __name__ == '__main__':
    main()

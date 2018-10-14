# -*- coding: utf-8 -*-

"""Command line interface"""

import argparse
import os

from hal.streams.logger import log_message

from peeper.preprocessing.models import Merger


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-d <directory to parse> '
                                           '-h for full usage')
    parser.add_argument('-d', dest='dir',
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
    data_time = folders[-3]
    data_day = folders[-4]
    output_file = "sensors.csv"
    output_folder = folder
    for _ in range(5):
        output_folder = os.path.dirname(output_folder)
    output_folder = os.path.join(output_folder, "output", data_day, data_time)
    output_file = os.path.join(output_folder, output_file)

    if not os.path.exists(output_folder):  # create necessary folders
        os.makedirs(output_folder)

    if os.path.exists(output_file):  # remove any previous outputs
        os.remove(output_file)

    return output_file


def main():
    folder = parse_args(create_args())
    log_message("Using folder", folder)

    output_file = get_output_file(folder)

    driver = Merger(folder)
    driver.merge_into(output_file)

    log_message("Merged into", output_file)


if __name__ == '__main__':
    main()

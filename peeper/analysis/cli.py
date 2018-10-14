# -*- coding: utf-8 -*-

"""Command line interface"""

import argparse
import os

from hal.files.models.files import Document
from hal.files.models.system import ls_recurse, is_file
from hal.streams.logger import log_message

from peeper.analysis.models import Plotter


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-i <input folder> '
                                           '-h for full usage')
    parser.add_argument('-i', dest='folder',
                        help='input folder', required=True)
    return parser


def parse_args(parser):
    """
    :param parser: ArgumentParser
        Object that holds cmd arguments.
    :return: tuple
        Values of arguments.
    """

    args = parser.parse_args()
    folder = str(args.folder)

    assert os.path.exists(folder)

    return folder


def get_output_file(file):
    """Finds output file suitable for input file

    :param file: input file
    :return: output file
    """

    output_file = "sensors.png"
    output_folder = os.path.dirname(file)
    output_file = os.path.join(output_folder, output_file)

    if not os.path.exists(output_folder):  # create necessary folders
        os.makedirs(output_folder)

    if os.path.exists(output_file):  # remove any previous outputs
        os.remove(output_file)

    return output_file


def analyze_test(file):
    """Analyze test

    :param file: test file
    :return: Analyzes data
    """

    output_file = get_output_file(file)

    driver = Plotter(file)
    driver.save(output_file)

    log_message("Plot saved to", output_file)


def analyze_day(folder):
    """Analyze day

    :param folder: day folder
    :return: Analyzes data
    """

    files = [
        file
        for file in ls_recurse(folder)
        if is_file(file) and Document(file).extension == ".csv"
    ]

    for file in files:
        log_message("Analyzing file", file)
        analyze_test(file)


def main():
    """CLI driver

    :return: Creates args and execute pre-processing
    """
    folder = parse_args(create_args())
    analyze_day(folder)


if __name__ == '__main__':
    main()

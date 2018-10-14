# -*- coding: utf-8 -*-

"""Command line interface"""

import argparse
import os

from hal.files.models.files import Document
from hal.streams.logger import log_message

from peeper.analysis.models import Plotter


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-i <input file> '
                                           '-h for full usage')
    parser.add_argument('-i', dest='file',
                        help='input file', required=True)
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
    assert Document(file).extension == ".csv"

    return file


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


def main():
    file = parse_args(create_args())
    log_message("Using file", file)

    output_file = get_output_file(file)

    driver = Plotter(file)
    driver.save(output_file)

    log_message("Plot saved to", output_file)


if __name__ == '__main__':
    main()

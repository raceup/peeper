# -*- coding: utf-8 -*-

"""Command line interface for pre-processing models"""

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
    assert (os.path.exists(directory))

    return directory


def main():
    folder = parse_args(create_args())
    log_message("Using folder", folder)

    output_file = "Merged.csv"
    output_file = os.path.join(os.path.dirname(folder), output_file)

    if os.path.exists(output_file):  # remove any previous outputs
        os.remove(output_file)

    driver = Merger(folder)
    driver.merge_into(output_file)

    log_message("Merged into", output_file)


if __name__ == '__main__':
    main()

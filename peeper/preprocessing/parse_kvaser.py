# -*- coding: utf-8 -*-

"""Parses Kvaser Output window from a .log file"""

import argparse

import os


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


def parse_file(path):
    """Parses .log file

    :param path: path to file
    :return: Shows file contents
    """

    print("Hello World!")


def main():
    file = parse_args(create_args())
    parse_file(file)


if __name__ == '__main__':
    main()

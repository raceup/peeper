# -*- coding: utf-8 -*-

"""Command line interface"""

import argparse
import os

import matplotlib.pyplot as plt
from hal.files.models.system import get_parent_folder_name, get_folder_name

from config.amk import MOTOR_LABELS
from peeper.analysis.models import Plotter


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-i <input path> '
                                           '-h for full usage')
    parser.add_argument('-i', dest='input_path',
                        help='input path', required=True)
    return parser


def parse_args(parser):
    """
    :param parser: ArgumentParser
        Object that holds cmd arguments.
    :return: tuple
        Values of arguments.
    """

    args = parser.parse_args()
    input_path = str(args.input_path)

    assert os.path.exists(input_path)

    return input_path


def analyze_test(file):
    """Analyze test

    :param file: test file
    :return: Analyzes data
    """

    driver = Plotter(file)
    driver.plot("T motor (°C)")
    driver.plot("T inverter (°C)")
    driver.plot("T IGBT (°C)")

    parent_folder = get_parent_folder_name(file)
    file_name = os.path.basename(file)
    title = '{}/{}'.format(parent_folder, file_name)
    plt.title(title)
    plt.show()


def analyze_motors(folder):
    files = [
        os.path.join(folder, "AMK2_{}.csv".format(motor))
        for motor in MOTOR_LABELS
    ]
    ti_file = os.path.join(folder, "TI.csv")

    # 2 x 2 plots

    ti_plotter = Plotter(ti_file)
    ti_plots = ["throttle (%)", "brake (%)"]

    for i, file in enumerate(files):
        plt.subplot(2, 2, i + 1)  # select subplot

        driver = Plotter(file)
        # driver.plot("actual velocity (x100 rpm)")
        driver.plot("T motor (°C)", with_trend=True)
        driver.plot("T inverter (°C)", with_trend=True)
        driver.plot("T IGBT (°C)", with_trend=True)

        for k in ti_plots:
            ti_plotter.plot(k)

    folder_name = get_folder_name(folder)
    title = '{}'.format(folder_name)
    plt.suptitle(title)
    plt.show()


def main():
    input_path = parse_args(create_args())
    analyze_motors(input_path)
    # analyze_test(file)


if __name__ == '__main__':
    main()

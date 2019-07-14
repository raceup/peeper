# -*- coding: utf-8 -*-

"""Module containing analysis models"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def interpol_function(x, a, b, c):
    # return a * (1 - np.exp(b * x)) + c
    return a * np.log(np.multiply(x, b)) + c
    # return a - np.divide(b, np.multiply(x, c))


def log_interpol_events(x, y):
    coeffs, covariance = curve_fit(interpol_function, x, y)

    def interpol(x_data):
        return interpol_function(x_data, *coeffs)

    return interpol, coeffs


class Plotter:
    """Plots data in file"""

    def __init__(self, file):
        """
        :param file: folder where there are the input files
        """

        self.path = file
        self.data = self._parse()
        self.plots = self._create_plots()

    def _parse(self, time_index="Timestamp (s)"):
        data = pd.read_csv(self.path)
        data = data.set_index(time_index)
        data.index.names = [time_index]
        return data

    def _create_plots(self):
        """Create plots from data

        :return: dictionary with title and data to plot
        """

        data_keys = filter(
            lambda label: not label.startswith("Byte"),
            self.data.keys()
        )  # just parsed data, not raw bytes
        plots = {
            key: self.data[key]
            for key in data_keys
        }  # column name -> df[time, column values]

        return plots

    @staticmethod
    def _pretty_number(x):
        x = str(x).strip()
        if not x.startswith('+') and not x.startswith('-'):
            x = '+ ' + x

        return x

    def plot(self, column_name):
        df = self.plots[column_name]
        x, y = df.index.tolist(), df.values.tolist()
        interpol, coeffs = log_interpol_events(x, y)

        y_trend = interpol(x)
        diff = y - y_trend
        std, mean = np.std(diff), np.mean(diff)

        x_pred = range(int(min(x)), 1800, 3)
        y_pred = interpol(x_pred)

        label = '{} std: {:.2f}, mean: {:.2f}'.format(column_name, std, mean)

        plt.plot(x, y, label=column_name)
        plt.plot(x_pred, y_pred, color='r', linestyle='--', label=label)
        plt.gcf().autofmt_xdate()  # prettify X-axis
        plt.xlabel('Time (s)')

        plt.legend()

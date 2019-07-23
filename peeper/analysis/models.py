# -*- coding: utf-8 -*-

"""Module containing analysis models"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.tools.combos import get_combo
from analysis.tools.interpol import log_interpol_events


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

    @staticmethod
    def _plot_data(x, y, label):
        plt.plot(x, y, label=label)

    @staticmethod
    def _plot_trend(x, y, label):
        interpol, coeffs = log_interpol_events(x, y)

        y_trend = interpol(x)
        diff = y - y_trend
        std, mean = np.std(diff), np.mean(diff)

        x_pred = range(int(min(x)), 900, 3)
        y_pred = interpol(x_pred)

        label = '{} std: {:.2f}, mean: {:.2f}'.format(label, std, mean)

        plt.plot(x_pred, y_pred, color='r', linestyle='--', label=label)

    @staticmethod
    def _finalize():
        plt.gcf().autofmt_xdate()  # prettify X-axis
        plt.xlabel('Time (s)')
        plt.legend()

    def _get_time_index(self):
        return self.data.index.tolist()

    def _get_combo(self, labels, f):
        values = [
            self.plots[label].values.tolist()
            for label in labels
        ]
        return get_combo(values, f)

    def plot(self, column_name, with_trend=False):
        df = self.plots[column_name]
        x, y = df.index.tolist(), df.values.tolist()
        plt.plot(x, y, label=column_name)

        if with_trend:
            self._plot_trend(x, y, column_name)

        self._finalize()

    def plot_values(self, values, label, with_filter=None):
        x = self._get_time_index()
        plt.plot(x, values, label=label)

        if with_filter:
            y_filtered = with_filter(values)
            label = '{} (filtered)'.format(label)
            plt.plot(x, y_filtered, label=label)

        self._finalize()

    def plot_combo(self, labels, f, label, with_trend=False):
        y = self._get_combo(labels, f)
        x = self.plots[labels[0]].index.tolist()  # the same for all
        plt.plot(x, y, label=label)

        if with_trend:
            self._plot_trend(x, y, label)

        self._finalize()

    def plot_filter(self, column_name, f):
        df = self.plots[column_name]
        x, y = df.index.tolist(), df.values.tolist()
        y_filtered = f(y)
        label = '{} (filtered)'.format(column_name)
        plt.plot(x, y_filtered, label=label)
        self._finalize()

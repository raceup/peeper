# -*- coding: utf-8 -*-

"""Module containing analysis models"""

import matplotlib.pyplot as plt
import pandas as pd
from hal.files.models.system import get_parent_folder_name


class Plotter:
    """Plots data in file"""

    def __init__(self, file):
        """
        :param file: folder where there are the input files
        """

        self.path = file
        self.data = self._parse()
        self.plots = self._create_plots()

    def _parse(self):
        """Parses input file

        :return: data in file
        """

        data = pd.read_csv(self.path)
        data = data.set_index("Milliseconds")
        data.index.names = ["Seconds"]
        data = data.rename(index={
            x: x / 1000.0
            for x in data.index
        })  # convert to s

        return data

    def _create_plots(self):
        """Create plots from data

        :return: dictionary with title and data to plot
        """

        labels = {
            "Compass": [
                key
                for key in self.data.keys()
                if key.startswith("Compass")
            ],
            "RotationVector": [
                key
                for key in self.data.keys()
                if key.startswith("RotationVector")
            ],
            "AccelerometerLinear": [
                key
                for key in self.data.keys()
                if key.startswith("AccelerometerLinear")
            ],
            "Gyroscope": [
                key
                for key in self.data.keys()
                if key.startswith("Gyroscope")
            ]
        }

        plots = {
            key: self.data[column_names]
            for key, column_names in labels.items()
        }
        for key, plot in plots.items():
            new_columns = {
                column: column.replace(key, "").strip()  # remove unnecessary
                for column in plot.keys()
            }
            plots[key] = plot.rename(columns=new_columns)

        return plots

    def save(self, output_file):
        """Saves plot to output

        :param output_file: output file (where to write data)
        """

        fig, ax = plt.subplots(2, 2, sharex="all")
        title = get_parent_folder_name(self.path)
        title = "Telemetry data from " + title.replace("-", ":")
        fig.suptitle(title)

        self.plots["Compass"].plot(ax=ax[0, 0], title="Compass")
        self.plots["RotationVector"].plot(ax=ax[0, 1], title="Rotation vector")
        self.plots["AccelerometerLinear"] \
            .plot(ax=ax[1, 0], title="Accelerations")
        self.plots["Gyroscope"].plot(ax=ax[1, 1], title="Gyro")

        plt.savefig(
            output_file,
            dpi=400,
            quality=100,
            orientation="landscape",
            papertype="a4",
            format="png"
        )
        plt.show()

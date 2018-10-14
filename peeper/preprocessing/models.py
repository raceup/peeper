# -*- coding: utf-8 -*-

"""Module containing pre-processing models"""

import numpy as np
import pandas as pd
from hal.files.models.files import Document
from hal.files.models.system import ls_dir


def sample_by_frequency(data, hertz):
    """Samples data with given frequency. Averages values if multiple

    :param data: data frame
    :param hertz: frequency, e.g 5 Hz => 1 / 5s => one sample each 0.2s
    :return: sampled data
    """

    freq = 1000.0 / hertz  # ms interval between 2 samples
    sampled_time = 0.0
    sampled_data = []  # sampled data (each row)
    start_sample_index = 0  # sample from this index ...

    for i, ms in enumerate(data.index):
        delta = ms - data.index[start_sample_index]

        if delta >= freq:  # end sample here
            end_sample_index = i

            while delta > freq and start_sample_index <= end_sample_index:
                delta = data.index[end_sample_index] - \
                        data.index[start_sample_index]
                end_sample_index -= 1

            sampled_time += freq
            sample_data = data.iloc[start_sample_index: end_sample_index]

            averages = sample_data.apply(np.nanmean, axis=0)  # average sample
            row = [sampled_time] + averages.tolist()
            for j, val in enumerate(row):
                if np.isnan(val):
                    row[j] = sampled_data[-1][j]  # last known value

            sampled_data.append(row)

            start_sample_index = end_sample_index + 1

    # build data frame from samples
    sampled_label = "Sample milliseconds"
    columns = [sampled_label] + list(data.keys())
    sampled_data = pd.DataFrame(data=sampled_data, columns=columns)
    sampled_data = sampled_data.set_index(sampled_label)

    return sampled_data


# todo handle removed data (if there are holes in between -> interpolate)
def remove_null_values(data, epsilon):
    """Removes rows that are null (under epsilon)

    :param data: data frame
    :param epsilon: remove all rows that are under this value
    :return: data frame
    """

    to_drop = []

    for i in data.index:
        row = data.loc[i]
        accelerations = [
            row["AccelerometerLinear X"],
            row["AccelerometerLinear Y"],
            row["AccelerometerLinear Z"]
        ]

        magnitude = np.linalg.norm(accelerations)
        if magnitude < epsilon:
            to_drop.append(i)

    return data.drop(to_drop)


class Merger:
    """Merges multiple .csv data files into a big one"""

    def __init__(self, folder):
        """
        :param folder: folder where there are the input files
        """

        self.path = folder
        self.data = {
            file: pd.read_csv(file)
            for file in self._find_files()
        }  # dictionary file name -> file data (as pandas data frame)

    def _find_files(self):
        """Finds files in folder

        :return: list of input files in folder
        """

        files = ls_dir(self.path)
        files = [
            file
            for file in files
            if Document(file).extension == ".csv"  # just csv files
        ]
        return files

    def _merge(self):
        """Merges data frames into one big

        :return: one big data frame with data from all input files
        """

        dfs = []  # list of data frames
        for file, data in self.data.items():
            file_name = Document(file).name
            data = data.drop(["Timestamp"], axis=1)  # remove column
            data = data.set_index("Milliseconds")  # set index
            data = data.groupby(data.index).first()  # remove duplicate index

            # rename columns
            new_columns = {
                col: file_name + " " + col
                for col in data.keys()
            }
            data = data.rename(index=str, columns=new_columns)  # rename columns

            dfs.append(data)

        data = pd.concat(dfs, axis=1, sort=True)  # merge

        # rename rows (convert to float)
        new_rows = {
            row: float(row)
            for row in data.index
        }
        data = data.rename(index=new_rows)
        data = data.sort_index()  # sort by index

        return data

    def _process(self):
        """Process data

        :return: data frame
        """
        data = self._merge()
        data = sample_by_frequency(data, 10)
        data = remove_null_values(data, 1)
        return data

    def merge_into(self, output_file):
        """Merges all inputs files into one

        :param output_file: output file (where to write data)
        """

        data = self._process()
        data.to_csv(output_file, index_label="Milliseconds")

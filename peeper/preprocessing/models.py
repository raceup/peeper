# -*- coding: utf-8 -*-

"""Module containing pre-processing models"""

import pandas as pd

from hal.files.models.files import Document
from hal.files.models.system import ls_dir


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

    def merge_into(self, output_file):
        """Merges all inputs files into one

        :param output_file: output file (where to write data)
        """

        data = self._merge()
        data.to_csv(output_file, index_label="Milliseconds")

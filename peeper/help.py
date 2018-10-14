# -*- coding: utf-8 -*-

"""Module containing bug report helper(s)."""

import json
import platform

from peeper import __version__ as peeper_version
from hal.data.dicts import get_inner_data
from hal.streams.markdown import MarkdownTable
from hal.streams.pretty_table import SqlTable


class BugReporter:
    """Generates reports on module installation"""
    def __init__(self):
        self.report = self.get_bug_report()

    @staticmethod
    def get_platform_info():
        """Gets platform info

        :return: platform info
        """

        try:
            system_name = platform.system()
            release_name = platform.release()
        except:
            system_name = "Unknown"
            release_name = "Unknown"

        return {
            'system': system_name,
            'release': release_name,
        }

    @staticmethod
    def get_bug_report():
        """Generate information for a bug report

        :return: information for bug report
        """
        platform_info = BugReporter.get_platform_info()
        module_info = {
            'version': peeper_version.__version__,
            'build': peeper_version.__build__
        }

        return {
            'platform': platform_info,
            'peeper': module_info
        }

    def _get_table(self):
        """Gets report as table (with columns)

        :return: column names and data
        """
        data = get_inner_data(self.report)
        labels = data.keys()
        row = [
            data[key]
            for key in labels
        ]
        return list(labels), [row]  # as matrix

    def as_json(self):
        """Gets report as json

        :return: json-formatted report
        """

        return json.dumps(self.report, sort_keys=True, indent=2)

    def as_sql(self):
        """Gets report as json

        :return: json-formatted report
        """

        labels, data = self._get_table()
        table = SqlTable(labels, data, "{:.3f}", "\n")
        return str(table)

    def as_markdown(self):
        """Gets report as json

        :return: json-formatted report
        """

        labels, data = self._get_table()
        table = MarkdownTable(labels, data)
        return str(table)


def main():
    """Pretty-print the bug information as JSON"""

    reporter = BugReporter()

    print("JSON report:")
    print(reporter.as_json())
    print()

    print("Markdown report:")
    print(reporter.as_markdown())

    print("SQL report:")
    print(reporter.as_sql())

    print("Choose the appropriate format (if you're submitting a Github Issue "
          "please chose the Markdown report) and paste it!")


if __name__ == '__main__':
    main()

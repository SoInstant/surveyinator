"""Provides utility functions.

This module contains utility functions for main.py and analyse.py.
Those functions are placed into this module to prevent spaghetti code in
both of those scripts.
"""
# Imports
import os
import pickle
from random import choices
from string import ascii_letters, digits

import plotly
from flask import Markup

from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter


# Misc

def secure(length):
    """Returns a random string of length"""
    return "".join(choices(ascii_letters + digits, k=length))


# File Utils
def parse_excel(excel_file):
    """Parses an Excel file by column

    Parse the Excel file, which has the responses to a survey,
    represented by excel_file, by column

    For example:
     |        A          |
    1|Do you like python?|
    2|Yes                |
    3|No                 |
    4|Yes                |

    Args:
        excel_file(str): The file name of the excel_file to be parsed

    Returns:
        A dictionary mapping the question to a tuple of responses
        For example:
        {"Do you like Python?": ("Yes","No","Yes")}

    Raises:
        KeyError: Question not present in column {i+1}
    """
    wb = load_workbook(excel_file)
    ws = wb.active
    cell_values = []
    for i, col in enumerate(ws.columns):
        if col[0].value:
            cell_values.append(
                [str(cell.value) for cell in col if cell.value is not None]
            )
        else:
            raise KeyError(f"Question not present in column {get_column_letter(i + 1)}")
    return dict([(col[0], col[1:]) for col in cell_values])


def parse_config(config_file):
    """Parses a config file

    Parses a config file represented by config_file. Config file
    contains the data-type of the responses.

    For example:
    1 categorical
    2 numerical
    3 ignore
    4 openended

    Args:
        config_file(str): The filename of the config file to be parsed

    Returns:
        A dictionary mapping the datatype to the question number
        For example:
        {1: "categorical", 2: "numerical", 3: "ignore", 4: "openended"}

    Raises:
        ValueError: Data-type not supported
    """
    with open(config_file, mode="r", encoding="utf-8") as f:
        lines = [line.lower() for line in f.read().split("\n") if line != ""]
        lines = [line.split(" ") for line in lines]
        accepted = ("ignore", "numerical", "categorical", "openended",)
        for i in lines:
            if not i[0].isdigit() or i[1] not in accepted:
                raise TypeError(
                    f"Line'{i}': parse_config only accepts lines with format <qn_no> <qn_type>"
                )
        lines = [(int(line[0]), line[1]) for line in lines]
        return dict(lines)


def to_config(directory, config):
    """"Creates/modifies a config file

    Creates/modifies a config file based on config given
    If config_file exists, it will modify the given config_file;
    else, it will create a new config file

    Args:
        directory(str) : Directory to save config file in
        config(dict) : Dictionary mapping datatype to question number
    Returns:
        String containing the path to the config file
    """
    to_write = [f"{i[0]} {i[1]}\n" for i in config.items()]
    file_path = os.path.join(directory, "config_file.txt")
    with open(file_path, "w") as config_f:
        config_f.writelines(to_write)
    return file_path


# Prediction
class Predictor(object):
    """TextBlob classifier that predicts if qn is either
    categorical, numerical, or openended.
    """

    def __init__(self):
        """Loads pre-trained TextBlob classifier."""
        with open("model.pickle", "rb") as f:
            self.classifier = pickle.load(f)

    def predict(self, qns):
        """Predicts if qns in qns are either categorical, numerical, or openended."""
        return [self.classifier.classify(qn) for qn in qns]


# Plotting
def pie(title, labels, values, hole=0.4):
    """Creates a pie chart

    Parses data passed in and creates a pie chart.

    Args:
        title(str): Title of the pie chart
        labels(list): Labels of each slice in the pie chart
        values(list): Value of each slice
        hole(float): Size of the hole in the pie chart

    Returns:
        HTML div of the pie chart
    """
    colors = ["#1cc88a", "#36b9cc", "#4e73df", "#f6c23e", "#e74a3b"]
    fig = plotly.graph_objs.Figure(
        data=[
            plotly.graph_objs.Pie(
                labels=labels,
                values=values,
                hole=hole,
                hoverinfo="label+percent",
                text=labels,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                sort=False,
                showlegend=False,
            )
        ]
    )

    fig.layout.font = dict(family="Nunito", size=18, color="#858796")

    return Markup(plotly.offline.plot(fig, include_plotlyjs=False, output_type="div"))


def split_lines(text, length=50):
    """Splits text

    Splits text into multiple lines without breaking words

    Args:
        text(str): Text to be split
        length(int): Size of each line

    Returns:
        String containing text split into lines
    """
    output = [""]
    for word in text.split(" "):
        if len(word) > length:
            output.append(word + "<br>")
        else:
            if len(output[-1]) + len(word) <= length:
                output[-1] += word + " "
            else:
                output[-1] += "<br>"
                output.append(word + " ")
    return "".join(output)


def chunk(input, size):
    """Splits iterable into chunks

    Splits iterable into multiple chunks

    Args:
        input(iterable): Iterable to be split
        size(int): Size of each chunk

    Yields:
        One chunk
    """
    for i in range(0, len(input), size):
        yield input[i: (i + size)]


if __name__ == "__main__":
    pass  # Testing is over :D

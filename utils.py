from openpyxl import load_workbook
import pickle
import plotly
from flask import Markup

# Parsing Utils
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
    """

    wb = load_workbook(excel_file)
    ws = wb.active
    cell_values = []
    for col in ws.columns:
        col_values = [cell.value for cell in col]
        cell_values.append(col_values)
    qn_response = {}
    for col in cell_values:
        qn_response[col[0]] = tuple(col[1:])
    return qn_response


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
        A tuple of the data-types
        For example:
        ("categorical","numerical","ignore","openended")

    Raises:
        ValueError: Data-type not supported
    """
    with open(config_file, mode="r", encoding="utf-8") as f:
        qn_categories = [line.split(" ") for line in f.read().split("\n")][:-1]
        qn_categories = [line[1].lower() for line in qn_categories]

    # Idiot-proofing
    allowed = ("ignore", "numerical", "categorical", "openended")
    for i, category in enumerate(qn_categories):
        if category not in allowed:
            raise ValueError(f"Qn{i}: Data-type not supported")
    return tuple(qn_categories)


# Prediction
class Predictor(object):
    def __init__(self):
        with open("model.pickle", "rb") as f:
            self.classifier = pickle.load(f)

    def predict(self, qns):
        return [self.classifier.classify(qn) for qn in qns]


# Ploting
def pie(title, labels, values, hole=0.4):
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
            )
        ]
    )

    newtitle = []
    for i in range(0, len(title), 30):
        newtitle.append(title[i : i + 30] + "<br>")
    fig.layout.title = "".join(newtitle)
    fig.layout.font = dict(family="Nunito", size=18, color="#858796")

    return Markup(plotly.offline.plot(fig, include_plotlyjs=False, output_type="div"))


def chunk(input, size):
    for i in range(0, len(input), size):
        yield input[i : i + size]

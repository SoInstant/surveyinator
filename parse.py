from openpyxl import load_workbook


def open_excel(excel_file):
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


def open_config(config_file):
    """Parses a config file

    Parses a config file represented by config_file. Config file
    contains the data-type of the responses.
    For example:
    1 Categorical

    Args:
        config_file(str): The filename of the config file to be parsed

    Returns:
        A tuple of the data-types
        For example:
        ("categorical")

    Raises:
        ValueError: Data-type not supported
    """
    with open(config_file, mode="r", encoding="utf-8") as f:
        qn_categories = [line.split(" ") for line in f.read().split("\n")][:-1]
        qn_categories = [line[1] for line in qn_categories]

    # Idiot-proofing
    allowed = ("ignore", "numerical", "categorical", "openended")
    for category in qn_categories:
        if category.lower() not in allowed:
            raise ValueError("Data-type not supported")
    return tuple(qn_categories)

from openpyxl import load_workbook

# File Parsing
def open_excel(excel_file):
    wb = load_workbook(excel_file)
    ws = wb.active
    cell_values = []
    for col in ws.columns:
        col_values = [cell.value for cell in col]
        cell_values.append(col_values)
    qn_response = {}
    for col in cell_values:
        qn_response[col[0]] = col[1:]
    return qn_response


def open_config(config_file):
    with open(config_file, mode="r", encoding="utf-8") as f:
        qn_categories = [line.split(" ") for line in f.read().split("\n")][:-1]
        qn_categories = [line[1] for line in qn_categories]
    # Idiot-proofing
    allowed = ("ignore", "numerical", "categorical", "openended")
    for category in qn_categories:
        if category.lower() not in allowed:
            raise ValueError("Data-type not supported")
    return qn_categories


def categorise(responses, categories):
    output = {}
    for i, items in enumerate(responses.items()):
        output[items[0]] = tuple([categories[i], items[1]])
    return output


def numerical(responses):
    pass


def categorical(responses):
    pass


def openended(responses):
    pass


def analyse(file, config_file):

    responses = open_excel(file)
    qn_categories = open_config(config_file)

    if len(qn_categories) != len(responses.values()):
        raise IndexError(
            "Config file does not have same number of questions as excel file"
        )

    categorised_responses = categorise(responses, qn_categories)
    for qn, responses in categorised_responses.items():
        category = responses[0]
        list_of_responses = responses[1]
        if category == "ignore":
            continue
        elif category == "numerical":
            numerical(list_of_responses)
        elif category == "categorical":
            categorical(list_of_responses)
        elif category == "openended":
            openended(list_of_responses)


if __name__ == "__main__":
    print(analyse("responses.xlsx", "config_file.txt"))

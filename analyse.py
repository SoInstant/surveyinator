from openpyxl import load_workbook

# File Parsing
def open_excel(excel_file):
    with load_workbook(filename="responses.xlsx") as wb:
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


def categorise(responces, categories):
    output = {}
    for pointer, items in enumerate(responces.items()):
        output[items[0]] = tuple([categories[pointer], items[1]])
    return output


def analyse(file, config_file):

    responces = open_excel(file)
    qn_categories = open_config(config_file)

    if len(qn_categories) != len(responces.values()):
        raise IndexError(
            "Config file does not have same number of questions as excel file"
        )

    categorised_responses = categorise(responces, qn_categories)
    for qn, responce in categorised_responses.items():
        category = response[0]
        list_of_responses = response[1]
        if category == "ignore":
            continue
        elif category == "numerical":
            numerical(list_of_responses)
        elif category == "categorical":
            categorical(list_of_responses)
        elif category == "openended":
            openended(list_of_responses)


if __name__ == "__main__":
    print(analyse("responces.xlsx", "config_file.txt"))

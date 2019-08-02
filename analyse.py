from openpyxl import load_workbook
from numpy import mean, median
from scipy.stats import mode

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
    central_tendencies = {
        "Mean": mean(responses),
        "Median": median(responses),
        "Mode": mode(responses),
    }
    return central_tendencies


def categorical(responses):
    categories = {}
    # Count responses per category
    for i in responses:
        if i not in categories.keys():
            categories[i] = 1
        else:
            categories[i] += 1

    # Find mode and percentage
    max_freq = max(categories.values())
    modes = []
    for category, freq in categories.items():
        if freq == max_freq:
            modes.append(category)
        categories[category] = freq / len(responses)
    return {"Percentages": categories, "Modes": modes}


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

    analysis = {}
    for qn, responses in categorised_responses.items():
        category = responses[0]
        list_of_responses = responses[1]
        if category == "ignore":
            continue
        elif category == "numerical":
            analysed = numerical(list_of_responses)
        elif category == "categorical":
            analysed = categorical(list_of_responses)
        elif category == "openended":
            analysed = openended(list_of_responses)
        analysis[qn] = analysed
    return analysis


if __name__ == "__main__":
    print(analyse("responses.xlsx", "config_file.txt"))

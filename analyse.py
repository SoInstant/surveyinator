from openpyxl import load_workbook


def open_excel(excel_file):
    wb = load_workbook(filename="responses.xlsx")
    ws = wb.active
    cell_values = []
    for col in ws.columns:
        col_values = [cell.value for cell in col]
        cell_values.append(col_values)
    qn_response = {}
    for col in cell_values:
        qn_response[col[0]] = col[1:]
    return qn_response


def analyse(file, config_file):
    responces = open_excel(file)
    with open(config_file, mode="r", encoding="utf-8") as f:
        qn_categories = [line for line in f.read().split("\n")][:-1]
    categorised_responses = {}
    try:
        for pointer, items in enumerate(responces.items()):
            categorised_responses[items[0]] = tuple([qn_categories[pointer], items[1]])
        print(categorised_responses)
    except IndexError:
        # This should output to website to warn user (Fatal Error if ML doesnt work)
        print("config_file has too little questions")

print(analyse("responces.xlsx","config_file.txt"))

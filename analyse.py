from openpyxl import load_workbook


def open_excel(file):
    wb = load_workbook(filename="responses.xlsx")
    ws = wb.active
    cell_values = []
    for col in ws.columns:
        col_values = [cell.value for cell in col]
        cell_values.append(col_values)
    qn_and_response = {}
    for col in cell_values:
        qn_and_response[col[0]] = col[1:]
    return qn_and_response


def analyse(file):
    responces = open_excel(file)
    categorised = {"Categorical": [], "Numerical": [], "Open-ended": []}
    return categorised


print(analyse("responces.xlsx"))

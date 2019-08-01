from openpyxl import load_workbook

def analyse(file):

    wb = load_workbook(filename = 'empty_book.xlsx')
    sheet_ranges = wb['range names']
    print(sheet_ranges['D18'].value)

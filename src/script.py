import os
from dotenv import load_dotenv
import gspread
from datetime import datetime, timedelta

load_dotenv()

credentials_path = os.getenv("GOOGLE_SHEET_CREDENTIALS")
gc = gspread.service_account(filename=credentials_path)
tabDates = ["SATURDAY", "SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]

def find_ambassador_block(worksheet, start_row):
    """Finds how many ambassador rows exist starting from a row in column B"""
    col_b = worksheet.col_values(1)
    row = start_row
    while row <= len(col_b) and col_b[row - 1].strip():
        if col_b[row - 1].strip() == "PERFORMANCE":
            break
        row += 1
    return start_row, row - 1

sheets = gc.openall()

for sheet in sheets:
    print(sheet)
    for worksheet in sheet.worksheets():
        if worksheet.title in tabDates:
            start, end = find_ambassador_block(worksheet, 5)
            worksheet.batch_clear([f'B{start}:P{end}'])
            p_start = end + 4
            p_start, p_end = find_ambassador_block(worksheet, p_start)
            worksheet.batch_clear([f'B{p_start}:P{p_end}'])

            if worksheet.title == "SATURDAY":
                
                current_date_str = worksheet.acell("A1").value
                try:
                    current_date = datetime.strptime(current_date_str, "%m/%d/%Y")
                    new_date = current_date + timedelta(days=7)
                    new_date_str = new_date.strftime("%m/%d/%Y")

                    worksheet.update("A1", [[new_date_str]])
                except ValueError:
                    print(f"⚠️ Could not parse date in {sheet.title} - SATURDAY!A1: '{current_date_str}'")
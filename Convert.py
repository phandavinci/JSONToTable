import pandas as pd
from openpyxl import Workbook
import docx
from openpyxl.styles import Font, Border, Side
import os


def ToExcel(parsedJSON):
    if os.path.exists('output.xlsx'): os.remove('output.xlsx')
    wb = Workbook()
    ws = wb.active
    row=1
    headers = ["Field Name", "Type"]
    tablename_font = Font(size=16, color='0f4761')
    header_font = Font(size=12, color='FF0000', bold=True)
    row1_font = Font(size=12, color='000000', bold=True)
    row2_font = Font(size=12, color="00339b", bold=True)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for table_name, table_data in parsedJSON.items():
        ws.append([table_name])
        ws.cell(row=row, column=1).font = tablename_font
        row+=1
        ws.append(headers)
        ws.cell(row=row, column=1).font = header_font
        ws.cell(row=row, column=2).font = header_font
        row+=1
        for rowitems in table_data:
            for field_name, field_type in rowitems.items():
                ws.append([field_name, field_type])
                ws.cell(row=row, column=1).font = row1_font
                ws.cell(row=row, column=2).font = row2_font
                row+=1
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.border = border
    wb.save("output.xlsx")
    return wb

    # with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    #     start_row = 0
    #     for table_name, table_data in parsedJSON.items():
    #         rows = []
    #         df_header = pd.DataFrame({table_name: []})
    #         df_header.to_excel(writer, sheet_name='Sheet1', startrow=start_row, index=False)
    #         start_row+=1
    #         for row in table_data:
    #             for field_name, field_type in row.items():
    #                 rows.append({"Field Name": field_name, "Type": field_type})
    #         df_rows = pd.DataFrame(rows)
    #         df_rows.to_excel(writer, sheet_name='Sheet1', startrow=start_row, index=False)
    #         start_row+= len(df_rows)+2

def ToWord():
    pass
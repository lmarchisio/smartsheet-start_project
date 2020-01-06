import smartsheet
import logging
import os

map_of_sheets = {}
row_map = {}
column_map = {}

def get_cell(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)

def evaluate_row(source_row):
    status_cell = get_cell(source_row, "Project #")
    status_value = status_cell.display_value
    if status_value == this_project[0:6]:
        smart.Sheets.delete_rows(
            2762627773425540,
            [source_row.id])

# Set API access token
access_token = None

# initialize client
smart = smartsheet.Smartsheet(access_token)
# make sure we don't miss any errors
smart.errors_as_exceptions(True)
# log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

_dir = os.path.abspath('C:/Users/lisam/AppData/Local/Programs/Python/Python37-32/Smartsheet/project management/exported archives')

# input sheet name
print('Enter number and name (ALL CAPS) of project to be archived')
this_project = input()

# create sheet map
response = smart.Sheets.list_sheets(include_all=True)
sheets = response.data

for sheet in sheets:
    map_of_sheets[sheet.name] = sheet.id

# export sheet as excel
smart.Sheets.get_sheet_as_excel(
    map_of_sheets[this_project],
    _dir)

# delete sheet
smart.Sheets.delete_sheet(map_of_sheets[this_project])

# check for overview sheet
for sheet in sheets:
    if sheet.name == this_project + ' Overview':
        # delete overview sheet
        smart.Sheets.delete_sheet(map_of_sheets[this_project + ' Overview'])

# delete line in project status
# get status sheet
sheet = smart.Sheets.get_sheet(2762627773425540)

for row in sheet.rows:
    row_map[row.row_number] = row.id

for column in sheet.columns:
    column_map[column.title] = column.id

for row in sheet.rows:
    evaluate_row(row)

import smartsheet
import logging

# Set API access token
access_token = None
project_column_map = {}
sheet_map = {}
writeRows = []

# initialize client
smart = smartsheet.Smartsheet(access_token)
# make sure we don't miss any errors
smart.errors_as_exceptions(True)
# log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

# initial inputs
print('enter project name (ALL CAPS)')
this_project = input()
print('PM email address?')
pm = input()

# helper functions to make column updates
def make_it(source_row, project_manager):
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = project_column_map['PM']
    new_cell.value = project_manager

    new_row = smartsheet.models.Row()
    new_row.id = source_row.id
    new_row.cells.append(new_cell)

    return new_row

# make a sheet map
response = smart.Sheets.list_sheets(include_all=True)
sheets = response.data

for sheet in sheets:
    sheet_map[sheet.name] = sheet.id

# make a column map
sheet = smart.Sheets.get_sheet(sheet_map[this_project])

for column in sheet.columns:
    project_column_map[column.title] = column.id

# make PM column row updates
print('working . . .')

for row in sheet.rows:
    write_row = make_it(row, pm)
    writeRows.append(write_row)
    print('...')

# write the updated rows
updated_row = smart.Sheets.update_rows(
        sheet.id,
        writeRows)

# update PM in status sheet
status_sheet = smart.Sheets.get_sheet(2762627773425540)

status_column_map = {}
status_rows = {}

for column in status_sheet.columns:
    status_column_map[column.title] = column.id

for rows in status_sheet.rows:
    status_rows[row.row_number] = row.id

def get_cell(row, column_name):
    column_id = status_column_map[column_name]
    return row.get_column(column_id)

for row in status_sheet.rows:
    project_number = get_cell(row, 'Project #')
    number_value = project_number.display_value
    project_name = get_cell(row, 'Project Name')
    name_value = project_name.display_value
    if str(number_value) + ' ' + str(name_value) == str(this_project):

        new_cell = smart.models.Cell()
        new_cell.column_id = status_column_map['Project Manager']
        new_cell.value = pm
        new_cell.strict = False

        new_row = smart.models.Row()
        new_row.id = row.id
        new_row.cells.append(new_cell)

        updated_row = smart.Sheets.update_rows(
            2762627773425540,
            [new_row])


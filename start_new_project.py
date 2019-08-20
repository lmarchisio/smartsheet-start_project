import smartsheet
import logging
from playsound import playsound
import timeit

# this script creates an entire new project

# creates the new project sheet in open projects workspace
# creates new overview sheet
# builds cross sheet references between the project and overview sheets
# builds new rows with appropriate formulas and xsheet references in overview

# Set API access token
access_token = None

project_columns = {}    # a place to map project column names to column IDs
overview_columns = {}   # a place to map overview column names to column IDs
project_rows = {}   # a place to map project rows numbers to row IDs
status_columns = {} # you get the idea
status_rows = {}
map_of_sheets = {}  # a place to map sheet names to sheet IDs

departments = ['Shipping',
               'Sculpt',
               'Paint',
               'Metal',
               'Install',
               'Fab',
               'Design',
               'CNC']

# functions to create cross sheet references
def make_start_reference(dept, source, destination):
    xref = ss_client.models.CrossSheetReference({
        'name': dept + ' Start Range',
        'source_sheet_id': int(source),
        'start_column_id': project_columns[dept + ' Start'],
        'end_column_id': project_columns[dept + ' Start']
        })

    result = ss_client.Sheets.create_cross_sheet_reference(
           destination, xref)

def make_finish_reference(dept, source, destination):
        xref = ss_client.models.CrossSheetReference({
        'name': dept + ' Finish Range',
        'source_sheet_id': int(source),
        'start_column_id': project_columns[dept + ' Finish'],
        'end_column_id': project_columns[dept + ' Finish']
        })

        result = ss_client.Sheets.create_cross_sheet_reference(
           destination, xref)

# initialize client
ss_client = smartsheet.Smartsheet(access_token)
# make sure we don't miss any errors
ss_client.errors_as_exceptions(True)
# log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

print('What is the project we are starting? (xx-xxx PROJECT NAME)')
this_project = input()

# start timer
start = timeit.default_timer()

# ---------- create new project sheet ----------
print('task 1 of 6: create new project sheet')

# create copy of template in workspace Projects, Open
response = ss_client.Sheets.copy_sheet(
    3222758374041476,
    smartsheet.models.ContainerDestination({
        'destination_type': 'workspace',
        'destination_id': 8881208101758852,
        'new_name': this_project
    }),
    include=['data', 'cellLinks']
)

print('task 1 done')

# ---------- create new tally sheet ----------
print('task 2 of 6: create new IMS overview sheet')

sheet_spec = ss_client.models.Sheet({
    'name': this_project + ' Overview',
    'columns': [{
        'title': 'Project Name',
        'primary': True,
        'type': 'TEXT_NUMBER',
        }, {
        'title': 'Resource',
        'type': 'PICKLIST',
        'options': [
            'CNC',
            'Design',
            'Fab',
            'Install',
            'Metal',
            'Paint',
            'Sculpt',
            'Shipping']
        }, {
        'title': 'Start',
        'type': 'DATE',
        }, {
        'title': 'Finish',
        'type': 'DATE',
        }
    ]
})

response = ss_client.Workspaces.create_sheet_in_workspace(
    2148322879268740,   # ID of IMS workspace
    sheet_spec)
new_sheet = response.result

print('task 2 done')

# ---------- create new rows for overview sheet ----------
print('task 3 of 6: write rows in IMS overview sheet')

# build sheet map
response = ss_client.Sheets.list_sheets(include_all=True)
sheets = response.data

for sheet in sheets:
    map_of_sheets[sheet.name] = sheet.id

# get source sheet
sheet = ss_client.Sheets.get_sheet(map_of_sheets[this_project])

# create column map for source sheet
for column in sheet.columns:
    project_columns[column.title] = column.id

# get overview sheet
sheet = ss_client.Sheets.get_sheet(map_of_sheets[this_project + ' Overview'])

# create column map for overview sheet
for column in sheet.columns:
    overview_columns[column.title] = column.id

for department in departments:
    make_start_reference(department, map_of_sheets[this_project], sheet.id)
    make_finish_reference(department, map_of_sheets[this_project], sheet.id)
    
    row_a = ss_client.models.Row()
    row_a.to_top = True
    row_a.cells.append({
        'column_id': overview_columns['Project Name'],
        'value': sheet.name[0:len(sheet.name)-9]
    })
    row_a.cells.append({
        'column_id': overview_columns['Resource'],
        'value': department
    })
    row_a.cells.append({
        'column_id': overview_columns['Start'],
        'formula': '=MIN({' + department + ' Start Range})'
    })
    row_a.cells.append({
        'column_id': overview_columns['Finish'],
        'formula': '=MAX({' + department + ' Finish Range})'
    })
    response = ss_client.Sheets.add_rows(
        sheet.id,
        [row_a])

print('task 3 done')

# ---------- update Project Status sheet ----------
print('task 4 of 6: add project to project status sheet')

# get project sheet
sheet = ss_client.Sheets.get_sheet(map_of_sheets[this_project])

# build row map of project sheet
for row in sheet.rows:
    project_rows[row.row_number] = row.id

# get project status sheet
sheet = ss_client.Sheets.get_sheet(2762627773425540)

# create column map for project status sheet
for column in sheet.columns:
    status_columns[column.title] = column.id

# specify new cell values for new row in project status
row_a = ss_client.models.Row()
row_a.to_top = True
row_a.cells.append({
  'column_id': status_columns['Project #'],
  'value': this_project[0:6],
  'hyperlink': {'sheetId': map_of_sheets[this_project]}
})
row_a.cells.append({
  'column_id': status_columns['Project Name'],
  'value': this_project[7:len(this_project)]
})

# add row to project status sheet
response = ss_client.Sheets.add_rows(
    2762627773425540,
    [row_a])

# refresh project status
sheet = ss_client.Sheets.get_sheet(2762627773425540)

# build row map of status sheet for use below
for row in sheet.rows:
    status_rows[row.row_number] = row.id

print('task 4 done')

# ---------- update exp start and finish in new row in status ----------
print('task 5 of 6: add cell links to project status sheet')

# create cell link from project sheet line 1 start
cell_link = ss_client.models.CellLink()
cell_link.sheet_id = map_of_sheets[this_project]
cell_link.row_id = project_rows[1]
cell_link.column_id = project_columns['Start']

# build new cell value
new_cell = ss_client.models.Cell()
new_cell.column_id = status_columns['Exp Start']
new_cell.link_in_from_cell = cell_link
new_cell.value = ss_client.models.ExplicitNull()

# build the row to update
new_row = ss_client.models.Row()
new_row.id = status_rows[1]
new_row.cells.append(new_cell)

# update rows
update_row = ss_client.Sheets.update_rows(
    2762627773425540,
    [new_row])

# create cell link from project sheet line 1 finish
cell_link = ss_client.models.CellLink()
cell_link.sheet_id = map_of_sheets[this_project]
cell_link.row_id = project_rows[1]
cell_link.column_id = project_columns['Finish']

# build new cell value
new_cell = ss_client.models.Cell()
new_cell.column_id = status_columns['Exp Finish']
new_cell.link_in_from_cell = cell_link
new_cell.value = ss_client.models.ExplicitNull()

# build the row to update
new_row = ss_client.models.Row()
new_row.id = status_rows[1]
new_row.cells.append(new_cell)

# update rows
update_row = ss_client.Sheets.update_rows(
    2762627773425540,
    [new_row])

print('task 5 of 6: expected start and finish links completed')

# ---------- update design start and finish in new row in status ----------
# create cell link from project sheet line 1 start
cell_link = ss_client.models.CellLink()
cell_link.sheet_id = map_of_sheets[this_project]
cell_link.row_id = project_rows[6]
cell_link.column_id = project_columns['Start']

# build new cell value
new_cell = ss_client.models.Cell()
new_cell.column_id = status_columns['Design Start']
new_cell.link_in_from_cell = cell_link
new_cell.value = ss_client.models.ExplicitNull()

# build the row to update
new_row = ss_client.models.Row()
new_row.id = status_rows[1]
new_row.cells.append(new_cell)

# update rows
update_row = ss_client.Sheets.update_rows(
    2762627773425540,
    [new_row])

# create cell link from project sheet line 1 finish
cell_link = ss_client.models.CellLink()
cell_link.sheet_id = map_of_sheets[this_project]
cell_link.row_id = project_rows[6]
cell_link.column_id = project_columns['Finish']

# build new cell value
new_cell = ss_client.models.Cell()
new_cell.column_id = status_columns['Design Finish']
new_cell.link_in_from_cell = cell_link
new_cell.value = ss_client.models.ExplicitNull()

# build the row to update
new_row = ss_client.models.Row()
new_row.id = status_rows[1]
new_row.cells.append(new_cell)

# update rows
update_row = ss_client.Sheets.update_rows(
    2762627773425540,
    [new_row])

print('task 5 of 6: design start and finish links completed')

# ---------- update fab start and finish in new row in status ----------
# create cell link from project sheet line 1 start
cell_link = ss_client.models.CellLink()
cell_link.sheet_id = map_of_sheets[this_project]
cell_link.row_id = project_rows[18]
cell_link.column_id = project_columns['Start']

# build new cell value
new_cell = ss_client.models.Cell()
new_cell.column_id = status_columns['Fab Start']
new_cell.link_in_from_cell = cell_link
new_cell.value = ss_client.models.ExplicitNull()

# build the row to update
new_row = ss_client.models.Row()
new_row.id = status_rows[1]
new_row.cells.append(new_cell)

# update rows
update_row = ss_client.Sheets.update_rows(
    2762627773425540,
    [new_row])

# create cell link from project sheet line 1 finish
cell_link = ss_client.models.CellLink()
cell_link.sheet_id = map_of_sheets[this_project]
cell_link.row_id = project_rows[18]
cell_link.column_id = project_columns['Finish']

# build new cell value
new_cell = ss_client.models.Cell()
new_cell.column_id = status_columns['Fab Finish']
new_cell.link_in_from_cell = cell_link
new_cell.value = ss_client.models.ExplicitNull()

# build the row to update
new_row = ss_client.models.Row()
new_row.id = status_rows[1]
new_row.cells.append(new_cell)

# update rows
update_row = ss_client.Sheets.update_rows(
    2762627773425540,
    [new_row])

print('task 5 of 6: fab start and finish links completed')
print('task 5 done')

# ---------- update exp start and finish in new row in status ----------
print('task 6 of 6: creating webhook')

# get project sheet
sheet = ss_client.Sheets.get_sheet(map_of_sheets[this_project])

# create webhook
Webhook = ss_client.Webhooks.create_webhook(
    smartsheet.models.Webhook({
        'name': 'Webhook_' + str(sheet.name),
        'callbackUrl': 'https://us-central1-subtle-bit-245615.cloudfunctions.net/function-1',
        'scope': 'sheet',
        'scopeObjectId': int(sheet.id),
        'events': ['*.*'],
        'version': 1}))

print('task 6 of 6: enabeling webhook')
map_of_webhooks = {}

IndexResult = ss_client.Webhooks.list_webhooks(
    page_size=100,
    page=1,
    include_all=False)

a = json.loads(str(IndexResult))
b = a.get('data', 0)

for n in range(len(b)):
    c = b[n]
    map_of_webhooks[str(c['name'])] = int(c['id'])
    
Webhook = ss_client.Webhooks.update_webhook(
    map_of_webhooks['Webhook_' + str(sheet.name)],
    ss_client.models.Webhook({
        'enabled': True}))

# end timer
stop = timeit.default_timer()

# Finish it
print('We made it this far.')
print('Good Job.')
print('Duration of Smartsheet stuff was: ', stop - start)
playsound('Gong.wav')



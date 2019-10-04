import smartsheet
import logging

project_columns = {}

# helper functions to create cross sheet references
def make_start_reference(dept, source, destination, token):
    ss_client = smartsheet.Smartsheet(token)
    xref = ss_client.models.CrossSheetReference({
        'name': dept + ' Start Range',
        'source_sheet_id': int(source),
        'start_column_id': project_columns[dept + ' Start'],
        'end_column_id': project_columns[dept + ' Start']
        })

    result = ss_client.Sheets.create_cross_sheet_reference(
           destination, xref)

def make_finish_reference(dept, source, destination, token):
    ss_client = smartsheet.Smartsheet(token)
    xref = ss_client.models.CrossSheetReference({
        'name': dept + ' Finish Range',
        'source_sheet_id': int(source),
        'start_column_id': project_columns[dept + ' Finish'],
        'end_column_id': project_columns[dept + ' Finish']
        })

    result = ss_client.Sheets.create_cross_sheet_reference(
           destination, xref)

def create_overview_columns(project, token):
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)
    # build sheet map
    response = ss_client.Sheets.list_sheets(include_all=True)
    sheets = response.data
    map_of_sheets = {}
    overview_columns = {}
    departments = ['Shipping',
               'Sculpt',
               'Paint',
               'Metal',
               'Install',
               'Fab',
               'Design',
               'CNC']

    for sheet in sheets:
        map_of_sheets[sheet.name] = sheet.id

    # get source sheet
    sheet = ss_client.Sheets.get_sheet(map_of_sheets[project])

    # create column map for source sheet
    for column in sheet.columns:
        project_columns[column.title] = column.id

    # get overview sheet
    sheet = ss_client.Sheets.get_sheet(map_of_sheets[project + ' Overview'])

    # create column map for overview sheet
    for column in sheet.columns:
        overview_columns[column.title] = column.id

    for department in departments:
        make_start_reference(department, map_of_sheets[project], sheet.id, token)
        make_finish_reference(department, map_of_sheets[project], sheet.id, token)
    
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

    print('done')

import smartsheet
import logging

column_map = {}

def make_pm_row(source_row, source_pm, token):
    ss_client = smartsheet.Smartsheet(token)
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = column_map['PM']
    new_cell.value = source_pm
    new_cell.strict = False

    new_row = smartsheet.models.Row()
    new_row.id = source_row.id
    new_row.cells.append(new_cell)

    return new_row

def add_pm(project, pm, token):
    import smartsheet
    import logging

    sheet_map = {}
    
    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    # sheet map
    response = ss_client.Sheets.list_sheets(include_all=True)
    sheets = response.data

    for sheet in sheets:
        sheet_map[sheet.name] = sheet.id

    # get sheet
    sheet = ss_client.Sheets.get_sheet(sheet_map[project])

    # column map
    for column in sheet.columns:
        column_map[column.title] = column.id

    rows_to_add = []

    for row in sheet.rows:
        rows_to_add.append(make_pm_row(row, pm, token))

    updated_row = ss_client.Sheets.update_rows(
        sheet_map[project],
        rows_to_add)

    print('done')
 


def add_pm(pm, token):
    import smartsheet
    import logging
    
    status_columns = {}
    status_rows = {}

    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    # get project status sheet
    sheet = ss_client.Sheets.get_sheet(2762627773425540)

    # create column map for project status sheet
    for column in sheet.columns:
        status_columns[column.title] = column.id

    # build row map of status sheet for use below
    for row in sheet.rows:
        status_rows[row.row_number] = row.id
    
    new_cell = ss_client.models.Cell()
    new_cell.column_id = status_columns['Project Manager']
    new_cell.value = pm
    new_cell.strict = False

    new_row = ss_client.models.Row()
    new_row.id = status_rows[1]
    new_row.cells.append(new_cell)

    updated_row = ss_client.Sheets.update_rows(
        2762627773425540,
        [new_row])

    print('done')

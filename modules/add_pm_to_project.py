def add_pm(project, pm, token):
    import smartsheet
    import logging

    sheet_map = {}
    column_map = {}
    
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

    for row in sheet.rows:
        new_cell = smartsheet.models.Cell()
        new_cell.column_id = column_map['PM']
        new_cell.value = pm
        new_cell.strict = False

        new_row = smartsheet.models.Row()
        new_row.id = row.id
        new_row.cells.append(new_cell)

        updated_row = ss_client.Sheets.update_rows(
            sheet_map[project],
            [new_row])

    print('done')
 

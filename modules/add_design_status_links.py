def design_links(project, token):
    import smartsheet
    import logging

    map_of_sheets = {}
    project_columns = {}
    project_rows = {}
    status_columns = {}
    status_rows = {}

    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    # list sheets
    response = ss_client.Sheets.list_sheets(include_all=True)
    sheets = response.data

    # build sheet map
    for sheet in sheets:
        map_of_sheets[sheet.name] = sheet.id

    # get project sheet
    sheet = ss_client.Sheets.get_sheet(map_of_sheets[project])

    # create column map for project sheet
    for column in sheet.columns:
        project_columns[column.title] = column.id

    # build row map of project sheet
    for row in sheet.rows:
        project_rows[row.row_number] = row.id

    # get project status sheet
    sheet = ss_client.Sheets.get_sheet(2762627773425540)

    # create column map for project status sheet
    for column in sheet.columns:
        status_columns[column.title] = column.id

    # build row map of status sheet for use below
    for row in sheet.rows:
        status_rows[row.row_number] = row.id

    # create cell link from project sheet line 1 start
    cell_link = ss_client.models.CellLink()
    cell_link.sheet_id = map_of_sheets[project]
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
    cell_link.sheet_id = map_of_sheets[project]
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

    print('done')


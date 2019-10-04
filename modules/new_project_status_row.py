def new_project_status_row(project, token):
    import smartsheet
    import logging
    
    map_of_sheets = {}
    project_rows = {}
    status_columns = {}
   
    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    # list sheets
    response = ss_client.Sheets.list_sheets(include_all=True)
    sheets = response.data

    # make sheet map
    for sheet in sheets:
        map_of_sheets[sheet.name] = sheet.id
    
    # get project sheet
    sheet = ss_client.Sheets.get_sheet(map_of_sheets[project])

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
      'value': project[0:6],
      'hyperlink': {'sheetId': map_of_sheets[project]}
    })
    row_a.cells.append({
      'column_id': status_columns['Project Name'],
      'value': project[7:len(project)]
    })

    # add row to project status sheet
    response = ss_client.Sheets.add_rows(
        2762627773425540,
        [row_a])

    print('done')


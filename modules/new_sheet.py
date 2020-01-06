def new_sheet(project, token):
    import smartsheet
    import logging

    project_columns = {}
    project_rows = {}
    map_of_sheets = {}
    
    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    # copy template sheet
    # must be done with a sheet instead of a template.
    # template does not allow purchase email in purchase approved workflow to be copied to new sheet.
    response = ss_client.Sheets.copy_sheet(
        3222758374041476,
        smartsheet.models.ContainerDestination({
            'destination_type': 'workspace',
            'destination_id': 8881208101758852,
            'new_name': project
        }),
        include=['data', 'cellLinks', 'rules', 'ruleRecipients']
    )

    # list sheets
    response = ss_client.Sheets.list_sheets(include_all=True)
    sheets = response.data

    # build sheet map
    for sheet in sheets:
        map_of_sheets[sheet.name] = sheet.id

    # get project sheet
    sheet = ss_client.Sheets.get_sheet(map_of_sheets[project])

    # build project column map
    for column in sheet.columns:
        project_columns[column.title] = column.id

    # build project row map
    for row in sheet.rows:
        project_rows[row.row_number] = row.id

    # add project name to top row of project sheet
    new_cell = smartsheet.models.Cell()
    new_cell.column_id = project_columns['Item or Task Description']
    new_cell.value = project
    new_cell.strict = False

    new_row = smartsheet.models.Row()
    new_row.id = project_rows[1]
    new_row.cells.append(new_cell)

    updated_row = ss_client.Sheets.update_rows(
        map_of_sheets[project],
        [new_row])
    
    print('done')


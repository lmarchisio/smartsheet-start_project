def new_tally(project_name, token):
    import smartsheet
    import logging
    
    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    # create new IMS sheet in project management workspace
    sheet_spec = ss_client.models.Sheet({
        'name': project_name + ' Overview',
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
                'Shipping',]
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
        2148322879268740, #ID of IMS workspace
        sheet_spec)
    new_sheet = response.result

    print('done')
                

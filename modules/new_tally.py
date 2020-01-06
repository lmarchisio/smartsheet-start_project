def new_tally(project_name, token):
    import smartsheet
    import logging
    
    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    # copy overview template
    response = ss_client.Sheets.copy_sheet(
        6257571175655300,
        smartsheet.models.ContainerDestination({
            'destination_type': 'workspace',
            'destination_id': 2148322879268740,
            'new_name': project_name + ' Overview'
        }),
        include=['data']
    )

    print('done')
                


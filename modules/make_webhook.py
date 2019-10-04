def make_webhook(project, token):
    import smartsheet
    import json
    import logging

    map_of_sheets = {}
    project_columns = {}
    map_of_webhooks = {}

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

    # create webhook
    Webhook = ss_client.Webhooks.create_webhook(
        smartsheet.models.Webhook({
            'name': 'Webhook_' + str(sheet.name),
            'callbackUrl': 'https://us-central1-subtle-bit-245615.cloudfunctions.net/function-1',
            'scope': 'sheet',
            'scopeObjectId': int(sheet.id),
            'events': ['*.*'],
            'version': 1}))

    # list webhooks
    IndexResult = ss_client.Webhooks.list_webhooks(
        page_size=100,
        page=1,
        include_all=False)

    # convert webhook list from json to python
    a = json.loads(str(IndexResult))

    # pull data
    b = a.get('data', 0)

    # build webhook map
    for n in range(len(b)):
        c = b[n]
        map_of_webhooks[str(c['name'])] = int(c['id'])

    # update webhook
    Webhook = ss_client.Webhooks.update_webhook(
        map_of_webhooks['Webhook_' + str(sheet.name)],
        ss_client.models.Webhook({
            'enabled': True}))

    print('done')

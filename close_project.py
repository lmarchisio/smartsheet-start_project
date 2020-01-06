import smartsheet
import logging
import json
import pprint

map_of_sheets = {}
map_of_hooks = {}

# Set API access token
access_token = None

# initialize client
smart = smartsheet.Smartsheet(access_token)
# make sure we don't miss any errors
smart.errors_as_exceptions(True)
# log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

# input sheet name
print('Enter number and name (ALL CAPS) of project to be closed')
this_project = input()

# create sheet map
response = smart.Sheets.list_sheets(include_all=True)
sheets = response.data

for sheet in sheets:
    map_of_sheets[sheet.name] = sheet.id

# create webhook map
IndexResult = smart.Webhooks.list_webhooks(
    page_size=100,
    page=1,
    include_all=False)

a = json.loads(str(IndexResult))
b = a.get('data', 0)

for n in range(len(b)):
    c = b[n]
    map_of_hooks[str(c['name'])] = int(c['id'])

# delete webhooks
smart.Webhooks.delete_webhook(
    map_of_hooks['Webhook_' + str(this_project)])

smart.Webhooks.delete_webhook(
    map_of_hooks['PM_Webhook_' + str(this_project)])

# move sheet to projects, complete
sheet = smart.Sheets.move_sheet(
    map_of_sheets[this_project],
    smart.models.ContainerDestination({
        'destination_type': 'workspace',
        'destination_id': 8670101869225860
    })
)

# move overview to projects, complete
sheet = smart.Sheets.move_sheet(
    map_of_sheets[this_project + ' Overview'],
    smart.models.ContainerDestination({
        'destination_type': 'workspace',
        'destination_id': 8670101869225860
    })
)

# from playsound import playsound
import timeit
from modules import new_sheet
from modules import new_tally
from modules import create_overview_columns
from modules import new_project_status_row
from modules import add_startfinish_status_links
from modules import add_design_status_links
from modules import add_fab_status_links
from modules import add_pm_to_status
from modules import make_webhook
from modules import add_pm_to_project

# this creates an entire new project

# creates the new project sheet in open projects workspace
# creates new overview sheet in project management workspace
# builds cross sheet references between the project and overview sheets
# builds new rows with appropriate formulas and xsheet references in overview
# 5.0 creates and enables webhook to google cloud function
# 5.1 now updates project manager in project status sheet
# 5.2 set first line of project sheet to name of project
# 5.3-4 separate into modules

# Set API access token
access_token = None

print('What is the project we are starting? (xx-xxx PROJECT NAME)')
this_project = input()

print('what is the project manager email?')
project_manager = input()

# start timer
start = timeit.default_timer()

print('creating new project sheet')
new_sheet.new_sheet(this_project, access_token)
print('creating new IMS overview sheet')
new_tally.new_tally(this_project, access_token)
print('adding pm to project sheet')
add_pm_to_project.add_pm(this_project, project_manager, access_token)
print('writing rows in IMS overview sheet')
create_overview_columns.create_overview_columns(this_project)
print('adding project to project status sheet')
new_project_status_row.new_project_status_row(this_project, access_token)
print('adding exp start and finish links to project status sheet')
add_startfinish_status_links.exp_startfinish(this_project, access_token)
print('adding design start and finish links to project status sheet')
add_design_status_links.design_links(this_project, access_token)
print('adding fab start and finish links to project status sheet')
add_fab_status_links.fab_links(this_project, access_token)
print('adding project manager to project status sheet')
add_pm_to_status.add_pm(project_manager, access_token)
print('creating webhook')
make_webhook.make_webhook(this_project, access_token)

# end timer
stop = timeit.default_timer()

# Finish it
print('all tasks complete')
print('Duration of Smartsheet API activity was: ', stop - start)
# playsound('Gong.wav')

print('press Enter key to close')
input()

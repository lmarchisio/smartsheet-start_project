import smartsheet
import logging

def sort_project_status(token):
    import smartsheet
    import logging

    sheet_map = {}
    
    # initialize client
    ss_client = smartsheet.Smartsheet(token)
    # make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    # log all calls
    logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    sort_specifier = smartsheet.models.SortSpecifier({
        'sort_criteria': [smartsheet.models.SortCriterion({
            'column_id': 7164751437424516,  # Exp Finish
            'direction': 'ASCENDING',
            'column_id': 4957636463486852,  # Schedule Status
            'direction': 'ASCENDING',
            'column_id': 5049912694990724,  # Project Manager
            'direction': 'ASCENDING'
        })]
    })
    sheet = ss_client.Sheets.sort_sheet(2762627773425540, sort_specifier)

    print('done')
 

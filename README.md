# smartsheet-start_new_project
## Introduction
This python script creates a new project and Integrated Master Schedule (IMS) sheet in Smartsheet.  It also adds the project to the Project Status sheet with appropriate cell links and cross-sheet references.  Specifically, it performs the following tasks:

1. Creates new project sheet from template
2. Creates new IMS overview sheet
3. Creates new rows in IMS overview sheet, including creating new cross-sheet references
4. Updates the Project Status sheet by creating a new line
5. Adds cell links between appropriate cells in the new Project Sheet and Project Status*

\* Note that this task is separate from 4 because the API does not allow the creation of cell links as part of the create new line command, it must be done as part of the update line command.

After running, there are a few manual actions required to complete project setup:
1. Set PM in Project Status
2. Add project to PMs schedule overview report
3. Add project to PMs portfolio report

This file contains examples of:
* Functions to create cross-sheet references
* Sheet map, column map, row map
* Cell links

## Requirements
* Smartsheet API & Python SDK
* timeit
* playsound
* Gong.wav (not strictly required, delete or comment out final line if not using)

## Setup
* Install the Smartsheet Python SDK `pip install smartsheet --upgrade`
* Update the API access token in start_new_project.py
* Run start_new_project.py

## Goals/To-Dos
- [x] Make many cross-sheet references
- [x] Make many cross-sheet references without having the script take 2 hours to run
- [x] Make cell links
- [x] Figure out why cell links are not working when creating a new line
- [ ] Figure out how to set PM in Project Status as part of script
- [ ] Add inputting shop loads to step 4

# smartsheet-start_new_project
## Introduction
This python script creates a new project and Integrated Master Schedule (IMS) sheet in Smartsheet.  It also adds the project to the Project Status sheet with appropriate cell links and cross-sheet references.  Specifically, it performs the following tasks:

1. Creates new project sheet from template
2. Creates new IMS overview sheet
3. Creates new rows in IMS overview sheet, including creating new cross-sheet references
4. Updates the Project Status sheet by creating a new line
5. Adds cell links between appropriate cells in the new Project Sheet and Project Status*
6. Adds project manager in the Project Manager column of Project Status
7. Creates and enables a new webhook from sheet to Google Cloud Function.
8. Sorts Project Status sheet.

\* Note that this task is separate from 4 because the API does not allow the creation of cell links as part of the create new line command, it must be done as part of the update line command.

This file contains examples of:
* Functions to create cross-sheet references
* Sheet map, column map, row map, webhook map
* Cell links

## Requirements
* Smartsheet API & Python SDK
* timeit

## Setup
* Install the Smartsheet Python SDK `pip install smartsheet --upgrade`
* Update the API access token in start_new_project.py
* Run start_new_project.py

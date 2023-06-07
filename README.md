# Personal Organizer App

- [Personal Organizer App](#personal-organizer-app)
  - [Video Demo](#video-demo)
  - [Description](#description)
  - [Considerations while coding](#considerations-while-coding)
  - [Files](#files)
  - [Code Breakout](#code-breakout)
    - [Imported libraries](#imported-libraries)
    - [Initial variables and program configurations](#initial-variables-and-program-configurations)
    - [index route](#index-route)
    - [add route](#add-route)
    - [list items route](#list-items-route)
    - [item details route](#item-details-route)
    - [update item route](#update-item-route)
    - [search route](#search-route)
    - [recycle route](#recycle-route)
    - [move to recycle route](#move-to-recycle-route)
    - [remove from recycle route](#remove-from-recycle-route)
    - [apology response](#apology-response)
    - [build item name list function](#build-item-name-list-function)
    - [build item type list function](#build-item-type-list-function)
    - [build item location list function](#build-item-location-list-function)
    - [display item list function](#display-item-list-function)
  - [Testing](#testing)
  - [Usage](#usage)
  - [Support/Roadmap/Project Status](#supportroadmapproject-status)
  - [Authors and Acknowledgment](#authors-and-acknowledgment)

## Video Demo

[Personal Organizer App Demo](https://vimeo.com/833895634?share=copy)

## Description

- This, as the simple app title implies, is a digital personal organizer.
- A user can add, update, and remove items.
- An item can save its name, type, location, and description.
- As well, the date the item was initially added to the database will be recorded, along with the most recent update date, and date recycled (when that is true).

## Considerations while coding

- Initially, I was going to utilize 2 separate CSV files. One for all 'current' items, and a second to hold the 'recycle bin' items.
- Having to manage (open, manipulate, and close) 2 separate CSV databases was quickly proving to be cumbersome and easy to make mistakes when moving items between the 2.
- Ultimately, I went with a simple filtering of what to display and delete, as this was similar in fashion to the update and search functions I was intending to implement as well.

## Files

- **app.py** -- the main flask application
- **app_config.py** -- small configuration file for running a test vs live environment
- **test_app.py** -- application to extensively test the app.py flask apps multiple routes and functions
- **item_database.csv** -- initial database of 'generic' items for demoing

## Code Breakout

### Imported libraries

- import **csv** -- used for manipulating CSV file data
- import **os** -- used for system functions, like creating CSV file
- import **urllib.parse** -- used to handle URL variables
- from **datetime** import **datetime** -- used to generate a 'time stamp'
- from **flask** import **Flask, redirect, render_template, request** -- used to create and manage a flask application

### Initial variables and program configurations

- There is some initial Flask app configuration, including setting the live environment
- If no database is detected, a new empty one is created
- Multiple routes are then defined for various purposes, as described below...

### index route

- Nothing more than the 'landing page'

### add route

- Form to add a new item
- Name, Type, and Location fields are required
  - Detail field is optional
- Returns an apology for duplicate named item and missing require fields

### list items route

- Allows a user to request a list of items based on type, location, or both
- Returns an apology if no items match the request

### item details route

- Displays all saved information on a selected item
- User can add/remove an item from the recycle bin from this page
- Returns an apology if the item requested does not exist

### update item route

- Form similar to the add item form, but pre-filled with current item info
- Same checks as adding a new item, no duplicates and required vs optional fields

### search route

- Allows a user to search the database, limiting by specific fields if they choose
- Returns a list of all items that match the search term
- Returns an apology if no items match the search term and options

### recycle route

- Displays all items that are listed as recycled but not yet deleted
- User can remove an item from the recycle bin by clicking a button
- Returns an apology if the recycle bin is empty

### move to recycle route

- Route used to move the selected item into the recycle bin

### remove from recycle route

- Route used to move the selected item out of the recycle bin

### apology response

- Dynamically created 'error' page
- Called from the app and passed the error code and message to display

### build item name list function

- Function used to create a list of item names
- Can be filtered based on type, location, and/or recycled status

### build item type list function

- Function to create a set of all unique types saved in the database

### build item location list function

- Function to create a set of all unique locations saved in the database

### display item list function

- Function to build the item display list for the list, search, and recycle routes
- Utilizes the *item_name_list* function

## Testing

- Testing is accomplished using pytest
- Every route and multiple methods of some routes are tested
  - Adding new items
  - Updating item information
  - Listing, displaying, and searching for items
  - Adding/Removing items from recycle bin
  - Emptying recycle bin

## Usage

- Generally, the web app interface is point and click along with keyboard entry for the text fields

## Support/Roadmap/Project Status

- There will be no further updates or support to this release.
- Project is considered **Complete**
- 6 June 2023

## Authors and Acknowledgment

- Christopher E Lorr
- Created as the final project for [CS50p](https://learning.edx.org/course/course-v1:HarvardX+CS50P+Python/home)

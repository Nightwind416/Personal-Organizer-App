import csv
import os
import urllib.parse
from datetime import datetime

from flask import Flask, redirect, render_template, request

# Setup flask app
flask_app = Flask(__name__)


# Set flask app environment
flask_app.config.from_object("app_config.LiveEnv")
# flask_app.config.from_object("app_config.TestEnv")

# Configure to prevent caching
@flask_app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Create new empty item database, if one does not exist
if os.path.isfile(flask_app.config['CSV_FILENAME']) == False:
    database = open(flask_app.config['CSV_FILENAME'], 'w', newline='')
    database_writer = csv.writer(database)
    # Add Sthe first row as colum labels
    database_writer.writerow(['Item Name', 'Item Type', 'Location', 'Detailed Info', 'Date Added', 'Date Updated', 'Date Recycled'])
    database.close()


# Define the index route
@flask_app.route("/")
@flask_app.route("/index")
def index():
    return render_template("index.html")


# Define a route to add new items to the database
@flask_app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get item details from form
        item_name = request.form.get("name")
        item_type = request.form.get("type")
        item_location = request.form.get("location")
        item_details = request.form.get("details")
        # Check if form entries were left blank
        if not item_name:
            return apology("You must enter an item name", 400)
        elif item_name in get_item_name_list():
            return apology("Sorry, that item name is already used (no duplicates)", 400)
        elif not item_type:
            return apology("You must enter an item type", 400)
        elif not item_location:
            return apology("You must enter an item location", 400)
        elif not item_details:
            item_details = "*No details provided"
        # Create new item to add to database
        date_added = datetime.today().strftime('%Y-%m-%d')
        date_updated = datetime.today().strftime('%Y-%m-%d')
        date_recycled = "None"
        new_item = [item_name,item_type,item_location,item_details,date_added,date_updated,date_recycled]
        # Add new item to database
        with open(flask_app.config['CSV_FILENAME'], 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_item)
        return render_template("item_details.html", reason="New item added", item=new_item)
    else:
        return render_template("add.html")


# Define a route to list items by type and/or location
@flask_app.route("/list_request", methods=["GET", "POST"])
def list_request():
    if request.method == "POST":
        # Get item and type from form
        location_name = request.form["location_list"]
        type_name = request.form["type_list"]
        # Build list of items to display
        item_name_list = get_item_name_list(location_name, type_name)
        display_list = build_list_to_display(item_name_list)
        # Check if list is empty
        if len(display_list) == 0:
            return apology("No items matched your search", 400)
        return render_template('list_results.html', display_list=display_list)
    else:
        # Build location and type dropdown lists
        location_list = get_location_name_list()
        type_list = get_item_type_list()
        return render_template('list_request.html', location_list=location_list, type_list=type_list)


# Define a route to list an items details, when requested
@flask_app.route('/item_details', methods=["GET"])
def item():
    # Get item name from request
    html_item_name = request.args.get('item_name')
    if html_item_name is not None:
            item_name = urllib.parse.unquote(html_item_name)
    else:
        item_name = ""
    # Get item details from database
    item = []
    with open(flask_app.config['CSV_FILENAME'], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Item Name'] == item_name:
                item = [row['Item Name'],row['Item Type'],row['Location'],row['Detailed Info'],row['Date Added'],row['Date Updated'],row['Date Recycled']]
    if item == []:
        return apology("Sorry, that item does not exist", 400)
    return render_template("item_details.html", reason="Detailed Item View", item=item)


# Define a route to search the database
@flask_app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Get search query and options from form
        search_query = request.form.get("search_query")
        options = {
            'option1': 'option1' in request.form,
            'option2': 'option2' in request.form,
            'option3': 'option3' in request.form,
            'option4': 'option4' in request.form,
            'option5': 'option5' in request.form,
            'option6': 'option6' in request.form,
            'option7': 'option7' in request.form
        }
        # Build list of items to display
        display_list = []
        with open(flask_app.config['CSV_FILENAME'], 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if search_query is not None and options.get('option1') and search_query in row['Item Name'].lower():
                    display_list.append(row)
                elif search_query is not None and options.get('option2') and search_query in row['Item Type'].lower():
                    display_list.append(row)
                elif search_query is not None and options.get('option3') and search_query in row['Location'].lower():
                    display_list.append(row)
                elif search_query is not None and options.get('option4') and search_query in row['Detailed Info'].lower():
                    display_list.append(row)
                elif search_query is not None and options.get('option5') and search_query in row['Date Added'].lower():
                    display_list.append(row)
                elif search_query is not None and options.get('option6') and search_query in row['Date Updated'].lower():
                    display_list.append(row)
                elif search_query is not None and options.get('option7') and search_query in row['Date Recycled'].lower():
                    display_list.append(row)
        # Check if list is empty
        if len(display_list) == 0:
            return apology("No items matched your search", 400)
        return render_template("search_results.html", display_list=display_list, search_query=search_query)
    else:
        return render_template("search.html")


# Define a route to update an item
@flask_app.route("/update_item", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        # Get item details from form
        original_item_name = request.form.get("original_item_name")
        item_name = request.form["name"]
        item_type = request.form.get("type")
        item_location = request.form.get("location")
        item_details = request.form.get("details")
        # Check if form entries were left blank
        if not item_name:
            return apology("You must enter an item name", 400)
        elif not item_type:
            return apology("You must enter an item type", 400)
        elif not item_location:
            return apology("You must enter an item location", 400)
        elif not item_details:
            item_details = "*No details provided"
        # Update item details in the database csv
        updated_item = []
        rows = []
        with open(flask_app.config['CSV_FILENAME'], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Item Name'] == original_item_name:
                    row['Item Name'] = item_name
                    row['Item Type'] = item_type
                    row['Location'] = item_location
                    row['Detailed Info'] = item_details
                    updated_item = [row['Item Name'], row['Item Type'], row['Location'], row['Detailed Info'], row['Date Added'], row['Date Updated'], row['Date Recycled']]
                rows.append(row)
        with open(flask_app.config['CSV_FILENAME'], 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return render_template("item_details.html", reason="Item updated", item=updated_item)
    else:
        # Get item name from request
        html_item_name = request.args.get('item_name')
        if html_item_name is not None:
            item_name = urllib.parse.unquote(html_item_name)
        else:
            item_name = ""
        # Get item details from database
        item = []
        with open(flask_app.config['CSV_FILENAME'], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Item Name'] == item_name:
                    item = [row ['Item Name'],row['Item Type'],row['Location'],row['Detailed Info'],row['Date Added'],row['Date Updated'],row['Date Recycled']]
        return render_template("update_item.html", item=item)
    

# Define a route to view and empty the recycled items
@flask_app.route("/recycle", methods=["GET", "POST"])
def recycle():
    if request.method == "POST":
        # open and read the database csv into a temp list, skipping recycled items
        rows = []
        with open(flask_app.config['CSV_FILENAME'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Date Recycled'] == 'None':
                    rows.append(row)
                else:
                    print(row['Item Name'] + " recycled")
        # write the updated temp list back to the database csv
        with open(flask_app.config['CSV_FILENAME'], 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return redirect("/recycle")
    else:
        # Build list of recycled items to display
        item_name_list = get_item_name_list(recycle=True)
        display_list = build_list_to_display(item_name_list)
        # Check if list is empty
        if len(display_list) == 0:
            return apology("Recycle bin is empty", 400)
        return render_template('recycle.html', display_list=display_list)


# Define a route to move an item to the recycle bin
@flask_app.route("/move_to_recycle", methods=["GET", "POST"])
def move_to_recycle():
    # Get item name depending on request method
    if request.method == "POST":
        item_name = request.form.get("item_name")
    else:
        html_item_name = request.args.get('item_name')
        if html_item_name is not None:
            item_name = urllib.parse.unquote(html_item_name)
        else:
            return apology("No item selected for recycling", 400)
    # open and read the database csv into a temp list, upadating the date field of the recycled item
    rows = []
    with open(flask_app.config['CSV_FILENAME'], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Item Name"] == item_name:
                row["Date Recycled"] = datetime.today().strftime("%Y-%m-%d")
            rows.append(row)
    # write the updated temp list back to the database csv
    with open(flask_app.config['CSV_FILENAME'], 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return redirect("/recycle")


# Define a route to remove an item from the recycle bin
@flask_app.route("/remove_from_recycle", methods=["GET", "POST"])
def remove_from_recycle():
    # Get item name depending on request method
    if request.method == "POST":
        item_name = request.form.get("item_name")
    else:
        html_item_name = request.args.get('item_name')
        if html_item_name is not None:
            item_name = urllib.parse.unquote(html_item_name)
        else:
            item_name = ""
    # open and read the database csv into a temp list
    rows = []
    with open(flask_app.config['CSV_FILENAME'], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    # update items date field, to indicate it was 'un-recycled'
    for row in rows:
        if row["Item Name"] == item_name:
            row["Date Recycled"] = "None"
    # write the updated temp list back to the database csv
    with open(flask_app.config['CSV_FILENAME'], 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return redirect("/recycle")


# Define a function to generate and render an 'apology' page
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Define a function to build an item name list based on location, type, and recycle status
def get_item_name_list(location_name="None", type_name="None", recycle=False):
    # Build a list of item names based on location, type, and recycle status
    item_name_list = []
    with open(flask_app.config['CSV_FILENAME'], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        if recycle:
            for row in reader:
                if row['Date Recycled'] != "None":
                    item_name_list.append(row['Item Name'])
        else:
            for row in reader:
                if row['Date Recycled'] != "None":
                    continue
                elif location_name == "None" and type_name == "None":
                    item_name_list.append(row['Item Name'])
                elif location_name != "None" and type_name == "None":
                    if row['Location'] == location_name:
                        item_name_list.append(row['Item Name'])
                elif location_name == "None" and type_name != "None":
                    if row['Item Type'] == type_name:
                        item_name_list.append(row['Item Name'])
                elif location_name != "None" and type_name != "None":
                    if (row['Location'] == location_name) and (row['Item Type'] == type_name):
                        item_name_list.append(row['Item Name'])
    # Sort and remove duplicates from the list
    if len(item_name_list) > 1:
        item_name_list = sorted(set(item_name_list))
    return item_name_list


# Define a function to create and return a list of all item types
def get_item_type_list():
    # Build a list of item types
    item_type_list = []
    with open(flask_app.config['CSV_FILENAME'], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_type_list.append(row['Item Type'])
    # Sort and remove duplicates from the list
    if len(item_type_list) > 1:
        item_type_list.sort()
        item_type_list = sorted(set(item_type_list))
    return item_type_list


# Define a function to create and return a list of all location names
def get_location_name_list():
    # Build a list of location names
    location_name_list = []
    with open(flask_app.config['CSV_FILENAME'], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            location_name_list.append(row['Location'])
    # Sort and remove duplicates from the list
    if len(location_name_list) > 1:
        location_name_list = sorted(set(location_name_list))
    return location_name_list


# Define a function to return a list of items to display
def build_list_to_display(item_name_list):
    # Build a list of items to display
    list_to_display = []
    with open(flask_app.config['CSV_FILENAME'], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Item Name'] in item_name_list:
                list_to_display.append([row['Item Name'],row['Item Type'],row['Location'],row['Detailed Info'],row['Date Added'],row['Date Updated'],row['Date Recycled']])
    # Sort and remove duplicates from the list
    if len(list_to_display) > 1:
        list_to_display.sort(key=lambda x: x[0])
    return list_to_display

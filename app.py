from flask import Flask, redirect, render_template, request
import csv
import os
import urllib.parse


# Configure app
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Create new empty item database, if one does not exist
if os.path.isfile('item_database.csv') == False:
    database = open('item_database.csv', 'w', newline='')
    database_writer = csv.writer(database)
    # Add the first row as colum labels
    database_writer.writerow(['Item Name', 'Item Type', 'Location', 'Detailed Info'])
    database.close()
# Create new empty recycle database, if one does not exist
if os.path.isfile('recycle_database.csv') == False:
    database = open('recycle_database.csv', 'w', newline='')
    database_writer = csv.writer(database)
    # Add the first row as colum labels
    database_writer.writerow(['Item Name', 'Item Type', 'Location', 'Detailed Info'])
    database.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get item details from form
        item_name = request.form.get("name").capitalize()
        item_type = request.form.get("type").title()
        item_location = request.form.get("location").title()
        item_description = request.form.get("description").capitalize()
        # Check if form entries were left blank
        if not item_name:
            return apology("You must enter an item name", 400)
        elif item_name in get_item_name_list():
            return apology("Sorry, that item name is already used (no duplicates)", 400)
        elif not item_type:
            return apology("You must enter an item type", 400)
        elif not item_location:
            return apology("You must enter an item location", 400)
        elif not item_description:
            return apology("You must enter an item description", 400)
        # Create new item to add to database
        new_item = [item_name,item_type,item_location,item_description]
        # Add new item to database
        with open('item_database.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_item)
        return render_template("item_details.html", reason="Newly Added Item", item=new_item)
    else:
        return render_template("add.html")


@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":
        ...
    else:
        return render_template("remove.html")


@app.route("/update_item", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        # Get item details from form
        item_name = request.form["name"]
        item_type = request.form.get("type")
        item_location = request.form.get("location")
        item_description = request.form.get("description")
        # Check if form entries were left blank
        if not item_name:
            return apology("You must enter an item name", 400)
        elif item_name in get_item_name_list():
            return apology("Sorry, that item name is already used (no duplicates)", 400)
        elif not item_type:
            return apology("You must enter an item type", 400)
        elif not item_location:
            return apology("You must enter an item location", 400)
        elif not item_description:
            return apology("You must enter an item description", 400)
        # Create new item to add to database
        updated_item = [item_name,item_type,item_location,item_description]
        # Add new item to database
        with open('item_database.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(updated_item)
        return render_template("item_details.html", reason="Updated Item", item=updated_item)
    else:
        item_list = get_item_name_list()
        return render_template("update_item.html", item_list=item_list)


@app.route("/list_request", methods=["GET", "POST"])
def list_request():
    if request.method == "POST":
        location_name = request.form["location_list"]
        type_name = request.form["type_list"]
        item_name_list = get_item_name_list(location_name, type_name)
        display_list = build_list_to_display(item_name_list)
        return render_template('list_results.html', display_list=display_list)
    else:
        location_list = get_location_name_list()
        type_list = get_item_type_list()
        return render_template('list_request.html', location_list=location_list, type_list=type_list)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        ...
    else:
        return render_template("search.html")


@app.route('/item_details', methods=["GET", "POST"])
def items():
    if request.method == "POST":
        ...
    else:
        html_item_name = request.args.get('name')
        print("html_item_name:")
        print(html_item_name)
        item_name = urllib.parse.unquote(html_item_name)
        print(item_name)
        with open('item_database.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Item Name'] == item_name:
                    item = [row['Item Name'],row['Item Type'],row['Location'],row['Detailed Info']]
        # item = ['Test Name','Test Type','Test Location','Test Info']
        return render_template("item_details.html", reason="Details Requested", item=item)


@app.route("/recycle", methods=["GET", "POST"])
def recycle():
    if request.method == "POST":
        location_name = request.form["location_list"]
        type_name = request.form["type_list"]
        item_name_list = get_item_name_list(location_name, type_name)
        display_list = build_list_to_display(item_name_list)
        return render_template('recycle.html', display_list=display_list)
    else:
        location_list = get_location_name_list()
        type_list = get_item_type_list()
        return render_template('recycle.html', location_list=location_list, type_list=type_list)


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


def get_item_name_list(location_name=None, type_name=None):
    item_name_list = []
    with open('item_database.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (location_name == 'None') and (type_name == 'None'):
                item_name_list.append(row['Item Name'])
            elif (location_name != 'None') and (type_name == 'None'):
                if row['Location'] == location_name:
                    item_name_list.append(row['Item Name'])
            elif (location_name == 'None') and (type_name != 'None'):
                if row['Item Type'] == type_name:
                    item_name_list.append(row['Item Name'])
            elif (location_name != 'None') and (type_name != 'None'):
                if (row['Location'] == location_name) and (row['Item Type'] == type_name):
                    item_name_list.append(row['Item Name'])
    if len(item_name_list) > 1:
        item_name_list = sorted(set(item_name_list))
    # print(item_name_list)
    return item_name_list


def get_item_type_list():
    item_type_list = []
    with open('item_database.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_type_list.append(row['Item Type'])
    if len(item_type_list) > 1:
        item_type_list.sort()
        item_type_list = sorted(set(item_type_list))
    # print(item_type_list)
    return item_type_list


def get_location_name_list():
    location_name_list = []
    with open('item_database.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            location_name_list.append(row['Location'])
    if len(location_name_list) > 1:
        location_name_list = sorted(set(location_name_list))
    # print(location_name_list)
    return location_name_list


def build_list_to_display(item_names):
    list_to_display = []
    with open('item_database.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Item Name'] in item_names:
                list_to_display.append([row['Item Name'],row['Item Type'],row['Location'],row['Detailed Info']])
    if len(list_to_display) > 1:
        list_to_display.sort(key=lambda x: x[0])
    # print(list_to_display)
    return list_to_display


def add_to_recycle(item_name):
    ...


def remove_from_recycle(item_name):
    ...

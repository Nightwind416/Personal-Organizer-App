from flask import Flask, redirect, render_template, request
import csv
import os


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


# Create new empty location database, if one does not exist
if os.path.isfile('location_database.csv') == False:
    database = open('location_database.csv', 'w', newline='')
    database_writer = csv.writer(database)
    # Add the first row as colum labels
    database_writer.writerow(['Location Name','Location Type','Detailed Info'])
    database.close()
# Create new empty item database, if one does not exist
if os.path.isfile('item_database.csv') == False:
    database = open('item_database.csv', 'w', newline='')
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
        item_name = request.form.get("name")
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
        new_item = [item_name,item_type,item_location,item_description]
        # Add new item to database
        with open('item_database.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_item)
        return render_template("index.html")
    else:
        return render_template("add.html")


@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":
        ...
    else:
        return render_template("remove.html")


@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        database_writer.writerow([item, specific_location, item_type, room_location, detailed_info])
        organizer_database.flush()
    else:
        return render_template("update.html")


@app.route("/list", methods=["GET", "POST"])
def list():
    if request.method == "POST":
        organizer_database.seek(0)
        reader = csv.reader(organizer_database)
        for row in reader:
            if row[1] == location or row[3] == location:
                print(row[0])
        organizer_database.flush()
    else:
        return render_template("list.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        organizer_database.seek(0)
        database_reader = csv.reader(organizer_database)
        for row in database_reader:
            if query in row:
                print(row)
        organizer_database.flush()
    else:
        return render_template("search.html")


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


def get_item_name_list():
    item_names = set()
    with open('item_database.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            item_names.add(row[0])
    return item_names


def get_item_type_list():
    item_types = set()
    with open('item_database.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            item_types.add(row[1])
    return item_types


def get_location_list():
    location_names = set()
    with open('location_database.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            location_names.add(row[2])
    return location_names


def get_location_type_list():
    location_types = set()
    with open('location_database.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            location_types.add(row[1])
    return location_types

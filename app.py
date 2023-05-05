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
    organizer_database = open('location_database.csv', 'w', newline='')
    database_writer = csv.writer(organizer_database)
    # Add the first row as colum labels
    database_writer.writerow(['Location Name','Location Type','Detailed Info'])
    organizer_database.close()
# Create new empty item database, if one does not exist
if os.path.isfile('item_database.csv') == False:
    organizer_database = open('item_database.csv', 'w', newline='')
    database_writer = csv.writer(organizer_database)
    # Add the first row as colum labels
    database_writer.writerow(['Item Name', 'Item Type', 'Location', 'Detailed Info'])
    organizer_database.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        item = input("What is the item you are saving? ")
        detailed = input("Do you want to enter detailed info for this item, or just the location? ")
        if detailed == 'yes':
            item_type = input("What type of itme is " + item + " ?")
            room_location = input("What room is " + item + " stored in?")
            specific_location = input("Where is the item currently stored? ")
            detailed_info = input("What is the detailed info for " + item + " ?")
            save_item(item, specific_location, item_type=item_type, room_location=room_location, detailed_info=detailed_info)
        else:
            specific_location = input("Where is the item currently stored? ")
            save_item(item, specific_location)
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

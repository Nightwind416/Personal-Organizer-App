import pytest
import os
import csv
from app import flask_app as app


# Set flask app test environment
app.config.from_object("app_config.TestEnv")


# Create new empty test item database, if one does not exist
if os.path.isfile(app.config['CSV_FILENAME']) == False:
    database = open(app.config['CSV_FILENAME'], 'w', newline='')
    database_writer = csv.writer(database)
    # Add the first row as colum labels
    database_writer.writerow(['Item Name', 'Item Type', 'Location', 'Detailed Info', 'Date Added', 'Date Updated', 'Date Recycled'])
    database.close()


# create a function to count database entries
def count_entries():
    with open(app.config['CSV_FILENAME'], 'r') as file:
        reader = csv.reader(file)
        # subtract 1 to exclude the header row
        entry_count = sum(1 for row in reader) - 1
        return entry_count


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# test index route
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to your Personal Organizer" in response.data


# test for empty starting database
def test_empty_database():
    expected_entries = 0
    actual_entries = count_entries()
    assert actual_entries == expected_entries


# test /add route
def test_add(client):
    # test empty name, error response
    response = client.post("/add", data={"name": "", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-name" in response.data
    # test empty type, error response
    response = client.post("/add", data={"name": "UnitTest_Empty_Type", "type": "", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-type" in response.data
    # test empty location, error response
    response = client.post("/add", data={"name": "UnitTest_Empty_Location", "type": "UnitTest_Type", "location": "", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-location" in response.data
    # test adding 10 new items, correct responses
    for i in range(10):
        response = client.post("/add", data={"name": f"UnitTest_New_Item{i}", "type": "c", "location": "UnitTest_Location", "details": "UnitTest_Details"})
        assert response.status_code == 200
        assert b"New item added" in response.data
    # test adding 3 additional items with no details, correct responses
    for i in range(3):
        response = client.post("/add", data={"name": f"UnitTest_New_Item_No_Details{i}", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": ""})
        assert response.status_code == 200
        assert b"*No details provided" in response.data
    # test adding a duplicate item, error response
    response = client.post("/add", data={"name": "UnitTest_New_Item1", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"Sorry%2C-that-item-name-is-already-used-%28no-duplicates%29" in response.data
    # test current database total is accurate
    expected_entries = 13
    actual_entries = count_entries()
    assert actual_entries == expected_entries



# test /list_request route
def test_list_request(client):
    # test GET request
    response = client.get("/list_request")
    assert response.status_code == 200
    assert b"List Request" in response.data
    # test POST request with type selected
    response = client.post("/list_request", data={"location_list": "None", "type_list": "UnitTest_Type"})
    assert response.status_code == 200
    assert b"List Results" in response.data
    # test POST request with location selected
    response = client.post("/list_request", data={"location_list": "UnitTest_Location", "type_list": "None"})
    assert response.status_code == 200
    assert b"List Results" in response.data
    # test POST request with type and location selected
    response = client.post("/list_request", data={"location_list": "UnitTest_Location", "type_list": "UnitTest_Type"})
    assert response.status_code == 200
    assert b"List Results" in response.data


# test /item_details route
def test_item_details(client):
    # test item not found
    response = client.get("/item_details?item_name=Nonexistent_Item")
    assert response.status_code == 400
    assert b"Sorry%2C-that-item-does-not-exist" in response.data
    # test item found
    response = client.get("/item_details?item_name=UnitTest_New_Item4")
    assert response.status_code == 200
    assert b"Detailed Item View" in response.data
    # test item found
    response = client.get("/item_details?item_name=UnitTest_New_Item_No_Details1")
    assert response.status_code == 200
    assert b"Detailed Item View" in response.data


# test /search route
def test_search(client):
    # test GET request
    response = client.get("/search")
    assert response.status_code == 200
    assert b"Which fields would you like to search" in response.data
    # test POST request with no results
    response = client.post("/search", data={"query": "Nonexistent_Item"})
    assert response.status_code == 400
    assert b"No-items-matched-your-search" in response.data
    # test POST request with search query (no options)
    response = client.post("/search", data={"query": "Unittest"})
    assert response.status_code == 200
    assert b"Search Query: Unittest" in response.data
    # test POST request with search query (name option)

    # test POST request with search query (type option)

    # test POST request with search query (location option)

    # test POST request with search query (detail option)

    # test POST request with search query (date added)

    # test POST request with search query (date updated)

    # test POST request with search query (date recycled)


# test update route
def test_update(client):
    # test GET request
    response = client.get("/update_item?item_name=Unittest_new_item0")
    assert response.status_code == 200
    assert b"Updating information for:" in response.data
    # test POST request to update item details
    response = client.post("/update_item", data={"name": "Updated_UnitTest_New_Item1", "type": "Updated_Type", "location": "Updated_Location", "details": "Updated_Details"})
    assert response.status_code == 200
    assert b"Item updated" in response.data


# test /recycle route (view empty recycle bin)
def test_recycle_view(client):
    # test GET request
    response = client.get("/recycle")
    assert response.status_code == 400
    assert b"Recycle Bin" in response.data
    assert b"Recycle-bin-is-empty" in response.data


# test /move_to_recycle route
def test_move_to_recycle(client):
    # test POST request to move an item to the recycle bin
    for i in range(5):
        response = client.post("/move_to_recycle", data={"item_name": f"UnitTest_New_Item{i}"})
        assert response.status_code == 302
        assert b"Redirecting" in response.data


# test /remove_from_recycle route
def test_remove_from_recycle(client):
    # test POST request to remove an item from the recycle bin
    for i in range(3):
        response = client.post("/remove_from_recycle", data={"item_name": "UnitTest_New_Item{i}"})
        assert response.status_code == 302
        assert b"Redirecting" in response.data


# test /recycle route (empty recycle bin)
def test_recycle_empty(client):
    # test POST request to empty bin
    response = client.post("/recycle")
    assert response.status_code == 302
    assert b"Recycle Bin" in response.data
    assert b"Recycle-bin-is-empty" in response.data


# Delete test item database csv, after all tests are run
def test_delete_csv():
    os.remove(app.config['CSV_FILENAME'])

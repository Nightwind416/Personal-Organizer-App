import pytest
from flask import session
import app
import os
import csv



# Create test flask client
@pytest.fixture
def client():
    # Set flask app test environment
    app.flask_app.config.from_object("app_config.TestEnv")
    # Create new empty test item database
    with open(app.flask_app.config['CSV_FILENAME'], 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Item Name', 'Item Type', 'Location', 'Detailed Info', 'Date Added', 'Date Updated', 'Date Recycled'])
    with app.flask_app.test_client() as client:
        yield client


# test index route
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to your Personal Organizer" in response.data


# test /add route
def test_add(client):
    # test empty name error response
    response = client.post("/add", data={"name": "", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-name" in response.data
    # test empty type error response
    response = client.post("/add", data={"name": "UnitTest_Empty_Type", "type": "", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-type" in response.data
    # test empty location error response
    response = client.post("/add", data={"name": "UnitTest_Empty_Location", "type": "UnitTest_Type", "location": "", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-location" in response.data
    # test adding 10 new items correct responses
    for i in range(10):
        response = client.post("/add", data={"name": f"UnitTest_New_Item{i}", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
        assert response.status_code == 200
        assert b"New item added" in response.data
    # test adding 3 new items with no details correct responses
    for i in range(3):
        response = client.post("/add", data={"name": f"UnitTest_New_Item_No_Details{i}", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": ""})
        assert response.status_code == 200
        assert b"*No details provided" in response.data
    # test adding a duplicate item error response
    response = client.post("/add", data={"name": "UnitTest_New_Item1", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"Sorry%2C-that-item-name-is-already-used-%28no-duplicates%29" in response.data



# test list_request route
def test_list_request(client):
    # test GET request
    response = client.get("/list_request")
    assert response.status_code == 200
    assert b"List Request" in response.data
    # # test POST request with type selected
    # response = client.post("/list_request", data={"type": "UnitTest_Type"})
    # assert response.status_code == 200
    # assert b"List Results" in response.data
    # # test POST request with location selected
    # response = client.post("/list_request", data={"location": "UnitTest_Location"})
    # assert response.status_code == 200
    # assert b"List Results" in response.data
    # # test POST request with type and location selected
    # response = client.post("/list_request", data={"type": "UnitTest_Type", "location": "UnitTest_Location"})
    # assert response.status_code == 200
    # assert b"List Results" in response.data


# test item route
def test_item(client):
    # test item not found
    response = client.get("/item_details?item_name=Nonexistent_Item")
    assert response.status_code == 400
    assert b"Sorry%2C-that-item-does-not-exist" in response.data
    # test item found
    response = client.get("/item_details?item_name=Unittest_new_item0")
    assert response.status_code == 200
    assert b"Detailed Item View" in response.data


# test search route
def test_search(client):
    # test GET request
    response = client.get("/search")
    assert response.status_code == 200
    assert b"Which fields would you like to search" in response.data
    # test POST request with search query
    response = client.post("/search", data={"query": "Unittest"})
    assert response.status_code == 200
    assert b"Search Results" in response.data

# # test recycle route
# def test_recycle(client):
#     # test GET request
#     response = client.get("/recycle")
#     assert response.status_code == 200
#     assert b"Recycle Bin" in response.data
#     # test POST request to recycle an item
#     response = client.post("/move_to_recycle", data={"name": "UnitTest_New_Item"})
#     assert response.status_code == 302
#     assert b"Redirecting" in response.data

# # test move_to_recycle route
# def test_move_to_recycle(client):
#     # test POST request to move an item to the recycle bin
#     response = client.post("/move_to_recycle", data={"name": "UnitTest_New_Item"})
#     assert response.status_code == 302
#     assert b"Redirecting" in response.data

# # test remove_from_recycle route
# def test_remove_from_recycle(client):
#     # test POST request to remove an item from the recycle bin
#     response = client.post("/remove_from_recycle", data={"name": "UnitTest_New_Item"})
#     assert response.status_code == 302
#     assert b"Redirecting" in response.data

# # test empty_recycle route
# def test_empty_recycle(client):
#     # test POST request to empty the recycle bin
#     response = client.post("/empty_recycle")
#     assert response.status_code == 302
#     assert b"Redirecting" in response.data

# # test update route
# def test_update(client):
#     # test GET request
#     response = client.get("/update?name=UnitTest_New_Item")
#     assert response.status_code == 200
#     assert b"Update Item Details" in response.data
#     # test POST request to update item details
#     response = client.post("/update", data={"name": "UnitTest_New_Item", "type": "Updated_Type", "location": "Updated_Location", "details": "Updated_Details"})
#     assert response.status_code == 302
#     assert b"Redirecting" in response.data

# Delete test item database csv, after all tests are run
def test_delete_csv():
    os.remove(app.flask_app.config['CSV_FILENAME'])

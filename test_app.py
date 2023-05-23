import pytest
import app
import os
import csv


@pytest.fixture
def client(monkeypatch):
    # enable Flask testing mode
    app.app.config["TESTING"] = True
    # Monkeypatch creating a test database
    def mock_initialize_database(database_file):
        if os.path.isfile(database_file) == False:
            with open(database_file, 'w', newline='') as database:
                database_writer = csv.writer(database)
                database_writer.writerow(['Item Name', 'Item Type', 'Location', 'Detailed Info', 'Date Added', 'Date Updated', 'Date Recycled'])
    # Apply the monkeypatch to the initialize_database function
    monkeypatch.setattr(app, "initialize_database", mock_initialize_database)
    # setup test client
    with app.app.test_client() as client:
        yield client


# test index route
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to your Personal Organizer" in response.data

# test /add route
def test_add(client):
    # test for empty name
    response = client.post("/add", data={"name": "", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-name" in response.data
    # test for empty type
    response = client.post("/add", data={"name": "UnitTest_Empty_Type", "type": "", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-type" in response.data
    # test for empty location
    response = client.post("/add", data={"name": "UnitTest_Empty_Location", "type": "UnitTest_Type", "location": "", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"You-must-enter-an-item-location" in response.data
    # test correctly adding new item
    response = client.post("/add", data={"name": "UnitTest_New_Item", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 200
    assert b"New item added" in response.data
    # test for trying to add a duplicate item
    response = client.post("/add", data={"name": "UnitTest_New_Item", "type": "UnitTest_Type", "location": "UnitTest_Location", "details": "UnitTest_Details"})
    assert response.status_code == 400
    assert b"Sorry%2C-that-item-name-is-already-used-%28no-duplicates%29" in response.data








def test_list_request(client):
    response = client.post("/list_request", data={"location_list": "Location 1", "type_list": "Type 1"})
    assert response.status_code == 200
    response = client.post("/list_request", data={"location_list": "Location 1"})
    assert response.status_code == 200
    response = client.post("/list_request", data={"type_list": "Type 1"})
    assert response.status_code == 200
    response = client.post("/list_request")
    assert response.status_code == 200
    # Add assertions for the expected output on the list_results.html template

def test_search(client):
    response = client.post("/search", data={"search_query": "item", "option1": True})
    assert response.status_code == 200
    # Add assertions for the expected output on the search_results.html template

def test_recycle(client):
    response = client.get("/recycle")
    assert response.status_code == 200
    # Add assertions for the expected output on the recycle.html template

def test_move_to_recycle(client):
    response = client.post("/move_to_recycle", data={"item_name": "Item 1"})
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/recycle"  # Assuming redirect to /recycle

def test_remove_from_recycle(client):
    response = client.post("/remove_from_recycle", data={"item_name": "Item 1"})
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/recycle"  # Assuming redirect to /recycle

def test_empty_recycle(client):
    response = client.post("/empty_recycle")
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/recycle"  # Assuming redirect to /recycle

def test_update_item(client):
    response = client.post("/update_item", data={"name": "Item 1", "type": "Type 2", "location": "Location 2", "details": "Details 2"})
    assert response.status_code == 200
    assert b"Item updated" in response.data
def test_create_board_list(client, board_data):
    board_list_data = {
        "board_id": board_data.id,
        "title": "Title For List",
        "order": 1  # Include order property
    }

    # Send a POST request to the board_list creation endpoint
    response = client.post("/board_list", json=board_list_data)
    print(response.json())
    # Assertions to ensure the board list was created successfully
    assert response.status_code == 200
    assert response.json()["title"] == board_list_data["title"]
    assert response.json()["board_id"] == board_list_data["board_id"]
    assert response.json()["order"] == board_list_data["order"]  # Checking order property
    assert "id" in response.json()

def test_get_board_lists_by_board_id(client, board_data, board_list_data):
    # Test the get_board_lists_by_board_id endpoint
    response = client.get(f"/board_list/{board_data.id}")
    board_lists = response.json()

    # Assertions to ensure the board lists are retrieved successfully
    assert response.status_code == 200
    assert isinstance(board_lists, list)
    assert len(board_lists) == len(board_list_data)
    for i, board_list in enumerate(board_lists):
        assert board_list["title"] == board_list_data[i].title
        assert board_list["board_id"] == board_list_data[i].board_id
        assert board_list["order"] == board_list_data[i].order  # Checking order property


def test_delete_board_list_by_board_id(client, board_list_data_single):
    # Test the deletion
    delete_response = client.delete(f"/board_list/{board_list_data_single.id}")
    assert delete_response.status_code == 200

    # check if the deleted board still exists
    get_response = client.get(f"/board_list/{board_list_data_single.id}")
    assert get_response.status_code == 404


def test_board_list_update(client, board_data, board_list_data_single):
    update_data = {
        "title": "Updated List Title",
        "order": 1  # Include order property
    }

    response = client.put(f"/board_list/{board_list_data_single.id}", json=update_data)

    data = response.json()

    # Check if the response is received correctly
    assert response.status_code == 200

    # Check if the data is updated
    assert data["title"] == update_data["title"]
    assert data["order"] == update_data["order"]  # Checking order property

    # Update only the title
    update_data_title = {
        "title": "Updating the title Only"
    }

    response = client.put(f"/board_list/{board_list_data_single.id}", json=update_data_title)

    data = response.json()

    # Check if the response is received correctly
    assert response.status_code == 200

    # Check if the data is updated
    assert data["title"] == update_data_title["title"]

    # Updating non-existent data
    response = client.put(f"/board_list/{9999}", json=update_data_title)

    assert response.status_code == 404
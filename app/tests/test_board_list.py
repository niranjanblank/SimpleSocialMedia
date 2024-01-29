
def test_create_board_list(client, board_data):
    board_list_data = {
        "board_id": board_data.id,
        "title": "Title For List",
        "description": "desc for the title of list in board"
    }

    # Send a POST request to the board_list creation endpoint
    response = client.post("/board_list", json=board_list_data)
    print(response.json())
    # Assertions to ensure the board list was created successfully
    assert response.status_code == 200
    assert response.json()["title"] == board_list_data["title"]
    assert response.json()["description"] == board_list_data["description"]
    assert response.json()["board_id"] == board_list_data["board_id"]
    assert "id" in response.json()

def test_get_board_lists_by_board_id(client, board_data, board_list_data):
    # Test the get_board_lists_by_board_id endpoint
    response = client.get(f"/board_list/{board_data.id}")
    board_lists = response.json()

    # Assertions to ensure the board lists are retrieved successfully
    assert response.status_code == 200
    assert isinstance(board_lists, list)
    assert len(board_lists) == len(board_list_data)


def test_delete_board_list_by_board_id(client, board_list_data_single):

    # Test the deletion
    delete_response = client.delete(f"/board_list/{board_list_data_single.id}")
    assert delete_response.status_code == 200

    # check if the deleted board still exist
    get_response = client.get(f"/board_list/{board_list_data_single.id}")
    assert get_response.status_code == 404

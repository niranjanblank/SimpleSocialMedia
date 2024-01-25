
def test_create_board_list(client, board_data):
    board_list_data = {
        "board_id": board_data.id,
        "title": "Title For List",
        "description": "desc for the title of list in board"
    }

    # Send a POST request to the user creation endpoint
    response = client.post("/board_list", json=board_list_data)
    print(response.json())
    # Assertions to ensure the user was created successfully
    assert response.status_code == 200
    assert response.json()["title"] == board_list_data["title"]
    assert response.json()["description"] == board_list_data["description"]
    assert response.json()["board_id"] == board_list_data["board_id"]
    assert "id" in response.json()

def test_create_board(client, user_data):
    board_data = {
        "title": "Board Title",
        "description": "Board Description",
        "owner_id": user_data.id
    }

    response = client.post("/boards", json=board_data)

    assert response.status_code == 200
    assert response.json()["title"] == board_data["title"]
    assert response.json()["description"] == board_data["description"]
    assert response.json()["owner_id"] == board_data["owner_id"]
    assert "id" in response.json()


def test_read_board_by_id(client, board_data):
    board_id = board_data.id
    response = client.get(f"/boards/{board_id}")

    board = response.json()

    assert response.status_code == 200
    assert board["id"] == board_id
    assert board["title"] == board_data.title
    assert board["description"] == board_data.description
    # Ensure that the owner information is included
    assert "owner" in board
    assert board["owner"] is not None
    assert "username" in board["owner"]


def test_update_board(client, board_data):
    board_id = board_data.id
    update_data = {
        "title": "Updated Board Title",
        "description": "Updated Board title"
    }

    response = client.put(f"/boards/{board_id}", json=update_data)
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_delete_board(client, board_data):
    board_id = board_data.id

    delete_response = client.delete(f"/boards/{board_id}")
    assert delete_response.status_code == 200

    # verify that the data is no longer available
    get_response = client.get(f"/boards/{board_id}")
    assert get_response.status_code == 404

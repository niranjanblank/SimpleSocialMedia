from unittest.mock import patch


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


def test_create_board_with_nonexistent_user(client):
    # Using a random or non-existent user ID
    nonexistent_user_id = 99999  # This should be an ID that doesn't exist in your user table

    # Board data with the non-existent user ID
    board_data = {
        "title": "Board Title",
        "description": "Board Description",
        "owner_id": nonexistent_user_id
    }

    response = client.post("/boards", json=board_data)

    # Assert that the board creation fails due to non-existent user
    assert response.status_code != 200


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


def test_get_boards_pagination(client, create_test_boards):
    # Test fetching the first few boards
    response = client.get("/boards/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  # Expecting 5 boards due to limit=5

    # Test another page of boards
    response = client.get("/boards/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  # Expecting the next 5 boards due to skip=5

    # Test edge case: Requesting more boards than exist
    response = client.get("/boards/?skip=0&limit=50")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(create_test_boards)  # Expecting the total number of boards created, as it's less than limit

    # Test edge case: Requesting with high skip
    response = client.get("/boards/?skip=30&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Expecting no boards as skip is beyond the total number of boards


def test_get_boards_by_owner_id(client, user_data, create_board_data_single_owner):
    # testing fetching
    response = client.get(f"/boards/owner/{user_data.id}")
    assert response.status_code == 200
    data = response.json()

    # checking if the data returned is equal to the data created in the db
    assert len(data) == 20

    # checking for non-existent user
    response = client.get(f"/boards/owner/{999999}")
    assert response.status_code == 404


# Mock data to simulate S3 response
MOCK_S3_RESPONSE = [
    "https://ticketingsystemdata.s3.ap-southeast-2.amazonaws.com/boards/template_images/image1.jpg",
    "https://ticketingsystemdata.s3.ap-southeast-2.amazonaws.com/boards/template_images/image2.jpg",
    "https://ticketingsystemdata.s3.ap-southeast-2.amazonaws.com/boards/template_images/image3.jpg",
]


# Mock function to replace `list_template_images` in your application
def mock_list_template_images(prefix):
    return MOCK_S3_RESPONSE


# Test for the /boards/template-images endpoint
@patch('app.routers.board_router.list_template_images', side_effect=mock_list_template_images)
def test_get_template_images(mock_list_template_images, client):
    response = client.get("/boards/images/template-images")

    print(response.status_code)  # Check status code
    print(response.json())

    # Check that the response is successful
    assert response.status_code == 200

    # Check that the response data matches the mock S3 data
    assert response.json() == MOCK_S3_RESPONSE

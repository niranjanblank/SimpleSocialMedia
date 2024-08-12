def test_create_list_card(client, board_list_data_single):
    """ Test for creating card in a list """
    list_card_data = {
        "title": "Test Card",
        "desc": "Test Description",
        "list_id": board_list_data_single.id,
        "order": 1  # Include order property
    }
    response = client.post("/list_card", json=list_card_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == list_card_data["title"]
    assert data["desc"] == list_card_data["desc"]
    assert data["list_id"] == list_card_data["list_id"]
    assert data["order"] == list_card_data["order"]  # Checking order property

    # Create another card to ensure order increments
    list_card_data_2 = {
        "title": "Test Card 2",
        "desc": "Test Description 2",
        "list_id": board_list_data_single.id,
        "order": 2  # Explicitly set order for the test
    }
    response_2 = client.post("/list_card", json=list_card_data_2)
    assert response_2.status_code == 200
    data_2 = response_2.json()
    assert data_2["order"] == list_card_data_2["order"]  # Order should match provided value

def test_get_list_card_by_list_id_endpoint_success(client, list_card_data):
    list_id = list_card_data[0].list_id
    response = client.get(f"/list_card/list/{list_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(list_card_data)
    for i, card in enumerate(data):
        assert card["title"] == list_card_data[i].title
        assert card["desc"] == list_card_data[i].desc
        assert card["list_id"] == list_card_data[i].list_id
        assert card["order"] == list_card_data[i].order  # Checking order property


def test_update_list_card(client, list_card_data, board_list_data):
    """ Test for updating a card in a list """
    # Use the first card from the fixture
    card_to_update = list_card_data[0]

    # Prepare the update payload
    update_payload = {
        "title": "Updated Card Title",
        "desc": "Updated description for card",
        "list_id": board_list_data[1].id,  # Moving the card to another list
        "order": 2
    }

    # Perform the PUT request to update the card
    response = client.put(f"/list_card/{card_to_update.id}", json=update_payload)

    # Ensure the request was successful
    assert response.status_code == 200

    # Parse the response
    data = response.json()

    # Verify the card was updated correctly
    assert data["id"] == card_to_update.id
    assert data["title"] == update_payload["title"]
    assert data["desc"] == update_payload["desc"]
    assert data["list_id"] == update_payload["list_id"]
    assert data["order"] == update_payload["order"]


def test_update_nonexistent_card(client):
    """ Test for updating a non-existent card """
    # Prepare an update payload
    update_payload = {
        "title": "Nonexistent Card Title",
        "desc": "This card does not exist",
        "list_id": 1,
        "order": 1
    }

    # Attempt to update a card with an ID that doesn't exist
    response = client.put("/list_card/9999", json=update_payload)  # Assuming 9999 is a non-existent ID

    # Ensure the request fails with a 404
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Card not found"

def test_delete_list_card(client, list_card_data):
    """ Test for deleting a card from a list """
    # Use the first card from the fixture to delete
    card_to_delete = list_card_data[0]

    # Perform the DELETE request to delete the card
    response = client.delete(f"/list_card/{card_to_delete.id}")

    # Ensure the request was successful
    assert response.status_code == 200

    # Check the response to ensure the card was deleted
    data = response.json()
    assert data == {"deleted": True}

    # Attempt to retrieve the deleted card to ensure it no longer exists
    response = client.get(f"/list_card/{card_to_delete.id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"No cards with id {card_to_delete.id}"


def test_delete_nonexistent_card(client):
    """ Test for deleting a non-existent card """
    # Attempt to delete a card with an ID that doesn't exist
    response = client.delete("/list_card/9999")  # Assuming 9999 is a non-existent ID

    # Ensure the request fails with a 404
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Card not found"


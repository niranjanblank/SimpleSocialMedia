def test_create_card_label_relationship(client, list_card_data, label_data):
    # Prepare the payload
    payload = {
        "card_id": list_card_data[0].id,
        "label_id": label_data.id
    }

    # Make the request to create the card-label relationship
    response = client.post("/card-labels", json=payload)

    # Assert the response status code
    assert response.status_code == 200

    # Assert that the response contains the correct card_id and label_id
    response_data = response.json()
    assert response_data["card_id"] == payload["card_id"]
    assert response_data["label_id"] == payload["label_id"]

def test_create_card_label_relationship_card_not_found(client, label_data):
    # Prepare the payload with a non-existent card_id
    payload = {
        "card_id": 9999,  # Assuming this ID does not exist
        "label_id": label_data.id
    }

    # Make the request to create the card-label relationship
    response = client.post("/card-labels", json=payload)

    # Assert the response status code
    assert response.status_code == 400

    # Assert the error message
    assert response.json() == {"detail": "Card with id 9999 not found"}

def test_create_card_label_relationship_label_not_found(client, list_card_data):
    # Prepare the payload with a non-existent label_id
    payload = {
        "card_id": list_card_data[0].id,
        "label_id": 9999  # Assuming this ID does not exist
    }

    # Make the request to create the card-label relationship
    response = client.post("/card-labels", json=payload)

    # Assert the response status code
    assert response.status_code == 400

    # Assert the error message
    assert response.json() == {"detail": "Label with id 9999 not found"}

def test_create_card_label_relationship_conflict(client, card_label_data):
    # Prepare the payload with an existing card-label relationship
    payload = {
        "card_id": card_label_data.card_id,
        "label_id": card_label_data.label_id
    }

    # Make the request to create the card-label relationship again
    response = client.post("/card-labels", json=payload)

    # Assert the response status code
    assert response.status_code == 400

def test_delete_card_label_relationship(client, list_card_data, label_data):
    # Create a relationship to delete
    card_id = list_card_data[0].id
    label_id = label_data.id

    # Create the card-label relationship
    response = client.post("/card-labels", json={"card_id": card_id, "label_id": label_id})
    assert response.status_code == 200

    # Now delete the relationship
    delete_response = client.delete(f"/card-labels/{card_id}/{label_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"deleted": True}

    # Ensure the relationship no longer exists
    double_delete_response = client.delete(f"/card-labels/{card_id}/{label_id}")
    assert double_delete_response.status_code == 404
    assert double_delete_response.json() == {"detail": "Card-label relationship not found."}
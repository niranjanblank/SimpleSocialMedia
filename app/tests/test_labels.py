def test_create_label(client, board_data):
    label_data = {
        "title": "Label 1",
        "color": "#ff3344",
        "board_id": board_data.id
    }

    response = client.post("/labels", json=label_data)

    assert response.status_code == 200
    assert response.json()["title"] == label_data["title"]
    assert response.json()["color"] == label_data["color"]
    assert response.json()["board_id"] == label_data["board_id"]
    assert "id" in response.json()


def test_get_labels_by_board_id(client, board_data, labels_data):
    response = client.get(f"/boards/{board_data.id}/labels")
    labels = response.json()

    assert response.status_code == 200
    assert isinstance(labels, list)
    assert len(labels_data) == len(labels)

    for i, label in enumerate(labels):
        assert label["title"] == labels_data[i].title
        assert label["color"] == labels_data[i].color
        assert label["board_id"] == labels_data[i].board_id


def test_delete_label(client, label_data):
    response = client.delete(f"/labels/{label_data.id}")

    assert response.status_code == 200
    assert response.json() == {"deleted": True}

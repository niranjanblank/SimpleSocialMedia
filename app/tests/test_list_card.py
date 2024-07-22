
def test_create_list_card(client, board_list_data_single):
    """ Test for creating card in a list """
    list_card_data = {
        "title": "Test Card",
        "desc": "Test Description",
        "list_id": board_list_data_single.id
    }
    response = client.post("/list_card", json=list_card_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == list_card_data["title"]
    assert data["desc"] == list_card_data["desc"]
    assert data["list_id"] == list_card_data["list_id"]

def
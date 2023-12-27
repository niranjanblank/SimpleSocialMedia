def test_create_user(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "a-very-secure-password"
    }

    # Send a POST request to the user creation endpoint
    response = client.post("/users/", json=user_data)

    # Assertions to ensure the user was created successfully
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]
    assert response.json()["email"] == user_data["email"]
    assert "id" in response.json()


def test_get_user_by_id(client, user_data):
    user_id = user_data.id

    # send a get request to retrieve the user
    response = client.get(f"/users/{user_id}")
    print(response.text)
    # assertions to ensure the user is retrieved successfully
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == user_id
    assert "username" in user  # Ensure the username is present
    assert "email" in user  # Ensure the email is present

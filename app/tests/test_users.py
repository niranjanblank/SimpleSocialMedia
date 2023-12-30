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


def test_user_pagination(client, create_test_users):
    # fetch the data
    response = client.get("/users/?skip=0&limit=5")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 5

    # Test another page of users
    response = client.get("/users/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  # Expecting the next 5 users

    # Test edge case: Requesting more users than exist
    response = client.get("/users/?skip=0&limit=20")
    assert response.status_code == 200
    data = response.json()
    total_users = len(create_test_users)
    assert len(data) == total_users  # Expecting the total number of users created, as it's less than limit

    # Test edge case: Requesting with high skip
    response = client.get("/users/?skip=15&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Expecting no users as skip is beyond the total number of users

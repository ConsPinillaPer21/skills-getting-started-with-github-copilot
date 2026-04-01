def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert "location" in response.headers


def test_get_activities_returns_200_and_activity_dict(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_get_activities_item_contains_key_fields(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    activity = response.json()["Chess Club"]

    # Assert
    assert response.status_code == 200
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_signup_success_returns_200_and_message(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    params = {"email": "new.student@mergington.edu"}

    # Act
    response = client.post(endpoint, params=params)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "message" in data


def test_signup_unknown_activity_returns_404_and_detail(client):
    # Arrange
    endpoint = "/activities/Unknown%20Activity/signup"
    params = {"email": "new.student@mergington.edu"}

    # Act
    response = client.post(endpoint, params=params)
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert "detail" in data


def test_signup_duplicate_returns_400_and_detail(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    params = {"email": "michael@mergington.edu"}

    # Act
    response = client.post(endpoint, params=params)
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert "detail" in data


def test_unregister_success_returns_200_and_message(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    params = {"email": "michael@mergington.edu"}

    # Act
    response = client.delete(endpoint, params=params)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "message" in data


def test_unregister_unknown_activity_returns_404_and_detail(client):
    # Arrange
    endpoint = "/activities/Unknown%20Activity/signup"
    params = {"email": "new.student@mergington.edu"}

    # Act
    response = client.delete(endpoint, params=params)
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert "detail" in data


def test_unregister_not_signed_up_returns_404_and_detail(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    params = {"email": "not.registered@mergington.edu"}

    # Act
    response = client.delete(endpoint, params=params)
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert "detail" in data

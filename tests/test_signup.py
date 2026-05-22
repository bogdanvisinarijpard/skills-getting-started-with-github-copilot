from urllib.parse import quote


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{encoded_activity}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_fails_when_activity_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity = quote(activity_name, safe="")
    email = "student@mergington.edu"
    endpoint = f"/activities/{encoded_activity}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_when_already_registered(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    email = "michael@mergington.edu"
    endpoint = f"/activities/{encoded_activity}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

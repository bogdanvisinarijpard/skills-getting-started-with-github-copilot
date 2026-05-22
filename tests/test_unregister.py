from urllib.parse import quote


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    email = "michael@mergington.edu"
    endpoint = f"/activities/{encoded_activity}/participants?email={quote(email, safe='')}"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_fails_when_activity_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity = quote(activity_name, safe="")
    email = "student@mergington.edu"
    endpoint = f"/activities/{encoded_activity}/participants?email={quote(email, safe='')}"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_when_participant_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    email = "absent@mergington.edu"
    endpoint = f"/activities/{encoded_activity}/participants?email={quote(email, safe='')}"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"

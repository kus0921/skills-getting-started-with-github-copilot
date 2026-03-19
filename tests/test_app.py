import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_and_unregister():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act: sign up
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert signup_response.status_code == 200
    assert email in signup_response.json()["message"]

    # Act: try duplicate signup
    duplicate_response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"]

    # Act: unregister
    unregister_response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert unregister_response.status_code == 200
    assert email in unregister_response.json()["message"]

    # Act: try duplicate unregister
    duplicate_unreg_response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert duplicate_unreg_response.status_code == 400
    assert "not registered" in duplicate_unreg_response.json()["detail"]

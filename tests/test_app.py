import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

ACTIVITY = "Chess Club"
EMAIL = "testuser@mergington.edu"


def test_list_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert ACTIVITY in data

def test_signup_activity():
    response = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Confirm participant is added
    response = client.get("/activities")
    participants = response.json()[ACTIVITY]["participants"]
    assert EMAIL in participants

def test_unregister_activity():
    response = client.post(f"/activities/{ACTIVITY}/unregister?email={EMAIL}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Confirm participant is removed
    response = client.get("/activities")
    participants = response.json()[ACTIVITY]["participants"]
    assert EMAIL not in participants

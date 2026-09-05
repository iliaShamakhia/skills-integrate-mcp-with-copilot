from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_activities_are_public():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data


def test_signup_requires_teacher_auth():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 401


def test_teacher_auth_allows_signup_and_unregister():
    username = "teacher"
    password = "m3rg1ngton"
    email = "teacher-test@mergington.edu"

    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
        auth=(username, password),
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
        auth=(username, password),
    )
    assert unregister_response.status_code == 200

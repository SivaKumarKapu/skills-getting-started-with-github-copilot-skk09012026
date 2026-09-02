from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert delete_response.status_code == 200
    payload = delete_response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_signup_updates_activity_state_immediately():
    activity_name = "Chess Club"
    email = "newstudent@example.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_delete_participant_returns_404_for_unknown_activity():
    response = client.delete("/activities/Unknown Activity/participants/student@example.edu")
    assert response.status_code == 404

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_existing_activity():
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_for_nonexistent_activity_returns_404():
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404


def test_unregister_from_activity():
    email = "tempstudent@mergington.edu"

    # sign up first so the student exists in the activity
    signup_response = client.post("/activities/Tennis Club/signup", params={"email": email})
    assert signup_response.status_code == 200

    response = client.delete("/activities/Tennis Club/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Tennis Club"}


def test_unregister_nonexistent_student_returns_400():
    response = client.delete("/activities/Chess Club/signup", params={"email": "missing@mergington.edu"})
    assert response.status_code == 400

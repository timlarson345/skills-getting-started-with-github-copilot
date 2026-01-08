import os
import sys
import urllib.parse

# Make src/ importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@example.com"

    # sign up
    r = client.post(f"/activities/{urllib.parse.quote(activity, safe='')}/signup?email={email}")
    assert r.status_code == 200

    # verify added
    r2 = client.get("/activities")
    participants = r2.json()[activity]["participants"]
    assert email in participants

    # unregister
    r3 = client.delete(f"/activities/{urllib.parse.quote(activity, safe='')}/unregister?email={email}")
    assert r3.status_code == 200

    r4 = client.get("/activities")
    participants2 = r4.json()[activity]["participants"]
    assert email not in participants2

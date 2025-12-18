from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_and_get_topic():
    create_resp = client.post(
        "/topics",
        json={"name": "Docker", "description": "Learn Docker"},
    )
    assert create_resp.status_code == 201
    topic = create_resp.json()

    get_resp = client.get(f"/topics/{topic['id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["name"] == "Docker"


def test_create_session_for_existing_topic():
    # create topic
    topic_resp = client.post(
        "/topics",
        json={"name": "Postgres", "description": "Learn SQL"},
    )
    topic = topic_resp.json()

    # create session
    session_resp = client.post(
        "/sessions",
        json={
            "topic_id": topic["id"],
            "study_date": "2025-01-01",
            "duration_minutes": 60,
            "notes": "Intro session",
        },
    )
    assert session_resp.status_code == 201


def test_create_session_for_unknown_topic_fails():
    resp = client.post(
        "/sessions",
        json={
            "topic_id": 9999,
            "study_date": "2025-01-01",
            "duration_minutes": 30,
            "notes": "Should fail",
        },
    )
    assert resp.status_code in (400, 404)

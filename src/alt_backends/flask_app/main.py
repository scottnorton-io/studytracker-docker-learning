from datetime import date, datetime

from flask import Flask, jsonify, request, abort


app = Flask(__name__)


_topics = []
_sessions = []
_topic_id = 0
_session_id = 0


@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "ok", "service": "studytracker-web-flask"})


@app.route("/topics", methods=["GET"])
def list_topics():
    return jsonify(_topics)


@app.route("/topics", methods=["POST"])
def create_topic():
    global _topic_id
    data = request.get_json(force=True) or {}
    name = data.get("name")
    if not name:
        abort(400, description="name is required")

    _topic_id += 1
    topic = {
        "id": _topic_id,
        "name": name,
        "description": data.get("description"),
        "created_at": datetime.utcnow().isoformat(),
    }
    _topics.append(topic)
    return jsonify(topic), 201


@app.route("/topics/<int:topic_id>", methods=["GET"])
def get_topic(topic_id: int):
    for t in _topics:
        if t["id"] == topic_id:
            return jsonify(t)
    abort(404, description="Topic not found")


@app.route("/sessions", methods=["POST"])
def create_session():
    global _session_id
    data = request.get_json(force=True) or {}

    topic_id = data.get("topic_id")
    if not any(t["id"] == topic_id for t in _topics):
        abort(400, description="Unknown topic_id")

    _session_id += 1
    session = {
        "id": _session_id,
        "topic_id": topic_id,
        "study_date": data.get("study_date", date.today().isoformat()),
        "duration_minutes": data.get("duration_minutes", 60),
        "notes": data.get("notes"),
        "created_at": datetime.utcnow().isoformat(),
    }
    _sessions.append(session)
    return jsonify(session), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)

# 📋 StudyTracker – Alternate Backends (Flask & Express)

Minimal alternate implementations of the StudyTracker API using **Flask** and **Express**, matching the same surface area as the FastAPI service.

> **Scope:** v0.1.0 parity on core routes (`/healthz`, `/topics`, `/topics/{id}`, `/sessions`) using in-memory storage. Later iterations can refactor to share the same database layer.
> 

---

## src/alt_backends/flask_app/[main.py](http://main.py)

```python
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
        "study_date": data.get("study_date", [date.today](http://date.today)().isoformat()),
        "duration_minutes": data.get("duration_minutes", 60),
        "notes": data.get("notes"),
        "created_at": datetime.utcnow().isoformat(),
    }
    _sessions.append(session)
    return jsonify(session), 201

if __name__ == "__main__":
    [app.run](http://app.run)(host="0.0.0.0", port=8001)
```

---

## src/alt_backends/express_app/index.js

```jsx
import express from "express";

const app = express();
app.use(express.json());

let topics = [];
let sessions = [];
let topicId = 0;
let sessionId = 0;

app.get("/healthz", (req, res) => {
  res.json({ status: "ok", service: "studytracker-web-express" });
});

app.get("/topics", (req, res) => {
  res.json(topics);
});

[app.post](http://app.post)("/topics", (req, res) => {
  const { name, description } = req.body || {};
  if (!name) {
    return res.status(400).json({ error: { code: "INVALID_INPUT", message: "name is required" } });
  }

  topicId += 1;
  const topic = {
    id: topicId,
    name,
    description: description || null,
    created_at: new Date().toISOString(),
  };
  topics.push(topic);
  res.status(201).json(topic);
});

app.get("/topics/:id", (req, res) => {
  const id = parseInt([req.params.id](http://req.params.id), 10);
  const topic = topics.find((t) => [t.id](http://t.id) === id);
  if (!topic) {
    return res.status(404).json({ error: { code: "TOPIC_NOT_FOUND", message: "Topic not found" } });
  }
  res.json(topic);
});

[app.post](http://app.post)("/sessions", (req, res) => {
  const { topic_id, study_date, duration_minutes, notes } = req.body || {};
  if (!topics.find((t) => [t.id](http://t.id) === topic_id)) {
    return res.status(400).json({ error: { code: "UNKNOWN_TOPIC", message: "Unknown topic_id" } });
  }

  sessionId += 1;
  const session = {
    id: sessionId,
    topic_id,
    study_date: study_date || new Date().toISOString().slice(0, 10),
    duration_minutes: duration_minutes || 60,
    notes: notes || null,
    created_at: new Date().toISOString(),
  };
  sessions.push(session);
  res.status(201).json(session);
});

const port = process.env.PORT || 8002;
app.listen(port, () => {
  console.log(`StudyTracker Express app listening on port ${port}`);
});
```

These alternates can be wired into additional Docker services (`web-flask`, `web-express`) using patterns similar to `web-fastapi` in the Docker & Compose page.
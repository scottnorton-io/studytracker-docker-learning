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

app.post("/topics", (req, res) => {
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
  const id = parseInt(req.params.id, 10);
  const topic = topics.find((t) => t.id === id);
  if (!topic) {
    return res.status(404).json({ error: { code: "TOPIC_NOT_FOUND", message: "Topic not found" } });
  }
  res.json(topic);
});

app.post("/sessions", (req, res) => {
  const { topic_id, study_date, duration_minutes, notes } = req.body || {};
  if (!topics.find((t) => t.id === topic_id)) {
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

CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    cwd TEXT,
    repository TEXT,
    host_type TEXT,
    branch TEXT,
    summary TEXT,
    agent_name TEXT,
    agent_description TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE turns (
    id INTEGER PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id),
    turn_index INTEGER,
    user_message TEXT,
    assistant_response TEXT,
    timestamp TEXT
);

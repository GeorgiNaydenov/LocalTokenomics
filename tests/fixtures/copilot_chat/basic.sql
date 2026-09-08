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

INSERT INTO sessions VALUES
    ('sess-alpha', '/home/user/alpha', 'user/alpha', 'local', 'main', 'a summary', NULL, NULL, '2026-08-20T10:00:00Z', '2026-08-20T10:05:00Z'),
    ('sess-null-cwd', NULL, NULL, 'local', NULL, NULL, NULL, NULL, '2026-08-20T11:00:00Z', '2026-08-20T11:01:00Z');

INSERT INTO turns VALUES
    (1, 'sess-alpha', 0, 'hello', 'hi there', '2026-08-20T10:00:05Z'),
    (2, 'sess-alpha', 1, 'do a thing', 'done', '2026-08-20T10:01:00Z'),
    (3, 'sess-null-cwd', 0, 'hello', 'hi', '2026-08-20T11:00:30Z');

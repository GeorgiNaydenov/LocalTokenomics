CREATE TABLE apps (
    id INTEGER PRIMARY KEY,
    name TEXT,
    path TEXT,
    created_at INTEGER,
    updated_at INTEGER,
    github_org TEXT,
    github_repo TEXT,
    chat_context TEXT,
    github_branch TEXT,
    vercel_project_id TEXT,
    vercel_project_name TEXT,
    vercel_team_id TEXT,
    vercel_deployment_url TEXT,
    neon_project_id TEXT,
    neon_development_branch_id TEXT,
    neon_preview_branch_id TEXT
);

CREATE TABLE chats (
    id INTEGER PRIMARY KEY,
    app_id INTEGER,
    title TEXT,
    created_at INTEGER,
    initial_commit_hash TEXT
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER,
    role TEXT,
    content TEXT,
    created_at INTEGER,
    approval_state TEXT,
    commit_hash TEXT
);

INSERT INTO apps VALUES
    (1, 'gamma', '/home/user/gamma', 1755680000, 1755680000, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

INSERT INTO chats VALUES
    (1, 1, NULL, 1755680100, NULL);

INSERT INTO messages VALUES
    (1, 1, 'assistant', 'done', 1755680210, NULL, NULL);

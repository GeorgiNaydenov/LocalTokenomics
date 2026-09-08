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
    (1, 'alpha', '/home/user/alpha', 1755680000, 1755680000, 'acme', 'alpha-app', NULL, 'main', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'beta', '/home/user/beta', 1755690000, 1755690000, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

INSERT INTO chats VALUES
    (1, 1, 'first chat', 1755680100, NULL),
    (2, 2, 'second chat', 1755690100, NULL);

INSERT INTO messages VALUES
    (1, 1, 'user', 'build me a login page', 1755680200, NULL, NULL),
    (2, 1, 'assistant', 'sure, here is the login page', 1755680210, NULL, NULL),
    (3, 2, 'assistant', 'done', 1755690210, NULL, NULL);

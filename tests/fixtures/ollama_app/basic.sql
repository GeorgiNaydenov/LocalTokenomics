CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    chat_id TEXT,
    role TEXT,
    content TEXT,
    thinking TEXT,
    stream INTEGER,
    model_name TEXT,
    model_cloud INTEGER,
    model_ollama_host TEXT,
    created_at TEXT,
    updated_at TEXT,
    thinking_time_start TEXT,
    thinking_time_end TEXT,
    tool_result TEXT
);

INSERT INTO messages VALUES
    (1, 'chat-1', 'user', 'hello', NULL, 0, NULL, NULL, NULL, '2025-08-26 11:00:40.0000000+03:00', '2025-08-26 11:00:40.0000000+03:00', NULL, NULL, NULL),
    (2, 'chat-1', 'assistant', 'hi there', NULL, 0, 'llama3.1:8b', 0, NULL, '2025-08-26 11:00:43.9084354+03:00', '2025-08-26 11:00:43.9084354+03:00', NULL, NULL, NULL),
    (3, 'chat-2', 'assistant', 'from the cloud', NULL, 0, 'gpt-oss:120b-cloud', 1, NULL, '2025-08-26 11:05:12.1234567+03:00', '2025-08-26 11:05:12.1234567+03:00', NULL, NULL, NULL);

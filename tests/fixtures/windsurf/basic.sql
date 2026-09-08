CREATE TABLE ItemTable (key TEXT UNIQUE, value TEXT);

INSERT INTO ItemTable (key, value) VALUES
    ('cascade.chatdata', '{"tabs": [
        {"tabId": "tab-1", "chatTitle": "Add tests", "lastSendTime": 1755680000000, "bubbles": [
            {"type": "user", "text": "add tests please"},
            {"type": "assistant", "text": "done, tests added"}
        ]},
        {"tabId": "tab-2", "chatTitle": "Empty tab", "bubbles": []}
    ]}');

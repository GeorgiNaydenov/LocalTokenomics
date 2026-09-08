CREATE TABLE cursorDiskKV (key TEXT UNIQUE, value BLOB);

INSERT INTO cursorDiskKV (key, value) VALUES
    ('composerData:11111111-1111-1111-1111-111111111111', '{"composerId": "11111111-1111-1111-1111-111111111111", "name": "Fix login bug", "createdAt": 1755680000000}'),
    ('composerData:22222222-2222-2222-2222-222222222222', '{"composerId": "22222222-2222-2222-2222-222222222222", "name": "Refactor auth", "createdAt": 1755683600000}'),
    ('bubbleId:11111111-1111-1111-1111-111111111111:aaa', '{"type": 1, "text": "hello"}');

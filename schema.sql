CREATE TABLE IF NOT EXISTS locations(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS grades(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    label       TEXT NOT NULL,
    sort_order  INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT NOT NULL DEFAULT (date('now')),
    location_id     INTEGER NOT NULL REFERENCES locations(id),
    duration_min    INTEGER,
    feel            INTEGER CHECK(feel BETWEEN 1 AND 5),
    notes           TEXT
);

CREATE TABLE IF NOT EXISTS climbs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL REFERENCES sessions(id),
    grade_id    INTEGER NOT NULL REFERENCES grades(id),
    tries       INTEGER NOT NULL DEFAULT 1,
    sent        INTEGER NOT NULL DEFAULT 0 CHECK(sent IN (0, 1)),
    notes       TEXT
);
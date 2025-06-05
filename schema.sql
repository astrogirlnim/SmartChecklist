DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS checklists;
DROP TABLE IF EXISTS items;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE checklists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checklist_id INTEGER NOT NULL,
    parent_item_id INTEGER,
    content TEXT NOT NULL,
    url TEXT,
    checked INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (checklist_id) REFERENCES checklists (id),
    FOREIGN KEY (parent_item_id) REFERENCES items (id)
); 
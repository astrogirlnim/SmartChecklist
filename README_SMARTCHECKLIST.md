# 📝 SmartChecklist - MVP

SmartChecklist is a web-based to-do application that allows users to create **smart checklists** with subnotes, links, and other contextual data to guide them through daily tasks. The MVP provides user registration, login, and authenticated management of personalized checklists.

---

## 🚀 Features (MVP)

- User registration and login
- Secure user sessions (Flask Sessions)
- Create/edit/delete checklists
- Create/edit/delete checklist items
- Support for:
  - Rich item text (subnotes, URLs)
  - Check/uncheck items
- SQLite database for lightweight storage
- Clean UI with raw JavaScript for interactivity

---

## 🛠️ Tech Stack

- Backend: Python (Flask)
- Frontend: HTML, CSS, Vanilla JavaScript
- Database: SQLite
- Auth: Flask-Login + sessions

---

## 📂 Project Structure

```
smartchecklist/
├── app.py
├── schema.sql
├── static/
│   ├── styles.css
│   └── script.js
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── instance/
│   └── smartchecklist.sqlite
├── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/smartchecklist.git
cd smartchecklist
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install Flask Flask-Login
```

### 4. Initialize the Database

```bash
flask shell < schema.sql
```

### 5. Run the App

```bash
export FLASK_APP=app.py  # on Windows use `set FLASK_APP=app.py`
export FLASK_ENV=development
flask run
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 🧱 Database Schema (`schema.sql`)

```sql
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
    content TEXT NOT NULL,
    checked INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (checklist_id) REFERENCES checklists (id)
);
```

---

## ✨ Core Pages

### `/register`
- Register new users.
- Stores hashed passwords.

### `/login`
- User login and session handling.

### `/dashboard`
- Shows all checklists for the logged-in user.
- Interface to create new checklists.

### `/checklist/<id>`
- View and manage a single checklist.
- Add/edit/delete checklist items.
- Mark items as done/undone.

---

## 🧠 JavaScript Interactivity (Minimal)

- **script.js** handles:
  - Checkbox toggling via AJAX (`fetch`)
  - Dynamic addition/removal of items

```js
function toggleItem(itemId) {
  fetch(`/toggle_item/${itemId}`, { method: 'POST' })
    .then(() => document.location.reload());
}
```

---

## 🔒 Auth & Security

- Passwords stored with hashing using `werkzeug.security`.
- Auth routes protected with `@login_required`.
- Flask session to store current user.

---

## ✍️ Notes

- MVP will not include advanced filtering, notifications, or sharing.
- Future improvements:
  - Due dates and reminders
  - Drag-and-drop UI
  - Markdown support
  - Mobile-friendly UI

---

## 📌 Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📄 License

MIT License

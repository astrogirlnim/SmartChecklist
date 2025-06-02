# 📝 SmartChecklist

A web-based to-do application that allows users to create smart checklists with subnotes, links, and other contextual data to guide them through daily tasks.

## Features

- User registration and login
- Create and manage multiple checklists
- Add/edit/delete checklist items
- Mark items as complete/incomplete
- Clean, modern UI
- Secure user authentication

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smartchecklist.git
cd smartchecklist
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask shell < schema.sql
```

5. Run the application:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Visit `http://127.0.0.1:5000` in your web browser to use the application.

## Usage

1. Register a new account or login with existing credentials
2. Create a new checklist from the dashboard
3. Add items to your checklist
4. Mark items as complete by clicking the checkbox
5. Navigate between different checklists from the dashboard

## Security

- Passwords are securely hashed using Werkzeug's security functions
- User sessions are managed securely using Flask-Login
- SQLite database with proper SQL injection prevention

## License

MIT License 
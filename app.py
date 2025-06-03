from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key
app.config['DATABASE'] = os.path.join(app.instance_path, 'smartchecklist.sqlite')

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    print('Initialized the database.')

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return User(user['id'], user['username'])
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('splash.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        
        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('register'))
            
        try:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
            
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    checklists = db.execute(
        'SELECT * FROM checklists WHERE user_id = ?',
        (current_user.id,)
    ).fetchall()
    return render_template('dashboard.html', checklists=checklists)

@app.route('/checklist/<int:id>')
@login_required
def checklist(id):
    db = get_db()
    checklist = db.execute(
        'SELECT * FROM checklists WHERE id = ? AND user_id = ?',
        (id, current_user.id)
    ).fetchone()
    if checklist:
        items = db.execute(
            'SELECT * FROM items WHERE checklist_id = ?',
            (id,)
        ).fetchall()
        return render_template('checklist.html', checklist=checklist, items=items)
    return redirect(url_for('dashboard'))

@app.route('/create_checklist', methods=['POST'])
@login_required
def create_checklist():
    title = request.form['title']
    if not title:
        flash('Title is required')
        return redirect(url_for('dashboard'))
        
    db = get_db()
    db.execute(
        'INSERT INTO checklists (user_id, title) VALUES (?, ?)',
        (current_user.id, title)
    )
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_item/<int:checklist_id>', methods=['POST'])
@login_required
def add_item(checklist_id):
    content = request.form['content']
    if not content:
        flash('Content is required')
        return redirect(url_for('checklist', id=checklist_id))
        
    db = get_db()
    db.execute(
        'INSERT INTO items (checklist_id, content, checked) VALUES (?, ?, 0)',
        (checklist_id, content)
    )
    db.commit()
    return redirect(url_for('checklist', id=checklist_id))

@app.route('/toggle_item/<int:item_id>', methods=['POST'])
@login_required
def toggle_item(item_id):
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if item:
        new_state = 1 if item['checked'] == 0 else 0
        db.execute(
            'UPDATE items SET checked = ? WHERE id = ?',
            (new_state, item_id)
        )
        db.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    db = get_db()
    # First check if the item exists and belongs to a checklist owned by the current user
    item = db.execute('''
        SELECT i.*, c.user_id 
        FROM items i 
        JOIN checklists c ON i.checklist_id = c.id 
        WHERE i.id = ? AND c.user_id = ?
    ''', (item_id, current_user.id)).fetchone()
    
    if item:
        db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        db.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/delete_checklist/<int:checklist_id>', methods=['POST'])
@login_required
def delete_checklist(checklist_id):
    db = get_db()
    # Check if the checklist belongs to the current user
    checklist = db.execute(
        'SELECT * FROM checklists WHERE id = ? AND user_id = ?',
        (checklist_id, current_user.id)
    ).fetchone()
    
    if checklist:
        # Delete all items in the checklist first (due to foreign key constraint)
        db.execute('DELETE FROM items WHERE checklist_id = ?', (checklist_id,))
        # Then delete the checklist itself
        db.execute('DELETE FROM checklists WHERE id = ?', (checklist_id,))
        db.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    app.run(debug=True) 
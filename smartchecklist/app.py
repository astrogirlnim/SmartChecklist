from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

def get_db_connection(db_path):
    """Get database connection for a given database path"""
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db

def database_exists_and_initialized(db_path):
    """Check if database exists and has the required tables"""
    if not os.path.exists(db_path):
        return False
    
    try:
        db = get_db_connection(db_path)
        # Check if all required tables exist
        required_tables = ['users', 'checklists', 'items']
        for table in required_tables:
            result = db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,)
            ).fetchone()
            if not result:
                return False
        
        # Check if tables have the expected structure
        # Check users table
        users_schema = db.execute("PRAGMA table_info(users)").fetchall()
        if len(users_schema) < 3:  # Should have id, username, password columns
            return False
        
        # Check checklists table  
        checklists_schema = db.execute("PRAGMA table_info(checklists)").fetchall()
        if len(checklists_schema) < 3:  # Should have id, user_id, title columns
            return False
        
        # Check items table
        items_schema = db.execute("PRAGMA table_info(items)").fetchall()
        if len(items_schema) < 4:  # Should have at least id, checklist_id, content, checked columns
            return False
        
        # Check if new columns exist (for schema updates)
        column_names = [col[1] for col in items_schema]
        if 'parent_item_id' not in column_names or 'url' not in column_names:
            return False
        
        return True
        
    except sqlite3.Error:
        return False
    finally:
        if 'db' in locals():
            db.close()

def init_db(app_instance=None, db_path=None):
    """Initialize database only if it doesn't exist or is not properly set up"""
    if app_instance:
        db_path = app_instance.config['DATABASE']
    
    if not db_path:
        raise ValueError("Either app_instance or db_path must be provided")
    
    if database_exists_and_initialized(db_path):
        print("Database already exists and is properly initialized.")
        return
        
    print("Initializing database...")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    if app_instance:
        # Use Flask app context for schema loading
        with app_instance.app_context():
            db = get_db_connection(db_path)
            with app_instance.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
            db.close()
    else:
        # Direct schema loading for standalone use
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        db = get_db_connection(db_path)
        with open(schema_path, 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()
    
    print("Database initialized successfully.")

def ensure_db_initialized(app_instance=None, db_path=None):
    """Ensure database is initialized - safe to call multiple times"""
    if app_instance:
        db_path = app_instance.config['DATABASE']
    
    if not database_exists_and_initialized(db_path):
        init_db(app_instance, db_path)

def organize_items_hierarchically(all_items):
    """Organize items into a hierarchical structure"""
    items_dict = {}
    root_items = []
    
    # First pass: create dictionary of all items
    for item in all_items:
        item_dict = dict(item)
        item_dict['subitems'] = []
        items_dict[item['id']] = item_dict
    
    # Second pass: organize hierarchy
    for item in all_items:
        if item['parent_item_id'] is None:
            # Root item
            root_items.append(items_dict[item['id']])
        else:
            # Subitem - add to parent's subitems list
            if item['parent_item_id'] in items_dict:
                items_dict[item['parent_item_id']]['subitems'].append(items_dict[item['id']])
    
    return root_items

def delete_item_and_subitems(db, item_id):
    """Recursively delete an item and all its subitems"""
    # Find all subitems of this item
    subitems = db.execute('SELECT id FROM items WHERE parent_item_id = ?', (item_id,)).fetchall()
    
    # Recursively delete subitems
    for subitem in subitems:
        delete_item_and_subitems(db, subitem['id'])
    
    # Delete the item itself
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))

def create_app(config=None):
    """Application factory function"""
    app = Flask(__name__)
    
    # Default configuration
    app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key
    app.config['DATABASE'] = os.path.join(app.instance_path, 'smartchecklist.sqlite')
    
    # Load additional configuration if provided
    if config:
        app.config.update(config)
    
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize Flask-Login
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
            # Get all items for this checklist
            all_items = db.execute(
                'SELECT * FROM items WHERE checklist_id = ? ORDER BY id',
                (id,)
            ).fetchall()
            
            # Organize items hierarchically
            items = organize_items_hierarchically(all_items)
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
        url = request.form.get('url', '').strip()
        parent_item_id = request.form.get('parent_item_id')
        
        if not content:
            flash('Content is required')
            return redirect(url_for('checklist', id=checklist_id))
        
        # Validate URL if provided
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
            
        # Convert empty string to None for parent_item_id
        if parent_item_id == '':
            parent_item_id = None
        elif parent_item_id:
            parent_item_id = int(parent_item_id)
            
        db = get_db()
        db.execute(
            'INSERT INTO items (checklist_id, parent_item_id, content, url, checked) VALUES (?, ?, ?, ?, 0)',
            (checklist_id, parent_item_id, content, url)
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

    @app.route('/edit_item/<int:item_id>', methods=['POST'])
    @login_required
    def edit_item(item_id):
        content = request.form.get('content', '').strip()
        url = request.form.get('url', '').strip()
        
        if not content:
            return jsonify({'success': False, 'error': 'Content is required'}), 400
        
        # Validate URL if provided
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        db = get_db()
        # Verify item exists and belongs to user's checklist
        item = db.execute('''
            SELECT i.*, c.user_id 
            FROM items i 
            JOIN checklists c ON i.checklist_id = c.id 
            WHERE i.id = ? AND c.user_id = ?
        ''', (item_id, current_user.id)).fetchone()
        
        if item:
            db.execute(
                'UPDATE items SET content = ?, url = ? WHERE id = ?',
                (content, url, item_id)
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
            # Delete all subitems first (cascade deletion)
            delete_item_and_subitems(db, item_id)
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
    
    @app.cli.command('init-db')
    def init_db_command():
        """Clear existing data and create new tables."""
        init_db(app_instance=app)
        print('Initialized the database.')
    
    # Ensure database is initialized on app startup
    with app.app_context():
        ensure_db_initialized(app_instance=app)
    
    return app

# Create a global app instance for development
app = create_app()

def main():
    """Entry point for the command line script"""
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main() 
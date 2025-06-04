#!/usr/bin/env python3
"""
Database initialization script for Smart Checklist App

This script safely initializes the database without overwriting existing data.
It can be run multiple times and will only initialize if the database doesn't exist
or is not properly set up.

Usage:
    python init_database.py
"""

import os
import sqlite3
from app import create_app, database_exists_and_initialized, init_db

def main():
    """Initialize the database safely"""
    print("Smart Checklist Database Initialization")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        # Check current database status
        db_path = app.config['DATABASE']
        print(f"Database path: {db_path}")
        
        if os.path.exists(db_path):
            print("✓ Database file exists")
            
            # Test database connection and structure
            try:
                if database_exists_and_initialized(db_path):
                    print("✓ Database is properly initialized with all required tables")
                    print("✓ Database structure is valid")
                    print("\n✅ Database is ready for use!")
                    
                    # Show database statistics
                    db = sqlite3.connect(db_path)
                    db.row_factory = sqlite3.Row
                    
                    user_count = db.execute("SELECT COUNT(*) as count FROM users").fetchone()['count']
                    checklist_count = db.execute("SELECT COUNT(*) as count FROM checklists").fetchone()['count']
                    item_count = db.execute("SELECT COUNT(*) as count FROM items").fetchone()['count']
                    
                    print(f"\n📊 Database Statistics:")
                    print(f"   Users: {user_count}")
                    print(f"   Checklists: {checklist_count}")
                    print(f"   Items: {item_count}")
                    
                    db.close()
                    
                else:
                    print("⚠ Database exists but is not properly initialized")
                    print("🔧 Initializing database structure...")
                    
                    init_db(app_instance=app)
                    
                    print("✅ Database initialized successfully!")
                    
            except Exception as e:
                print(f"❌ Error checking database: {e}")
                print("🔧 Attempting to initialize database...")
                
                init_db(app_instance=app)
                
                print("✅ Database initialized successfully!")
        else:
            print("ℹ Database file does not exist")
            print("🔧 Creating and initializing database...")
            
            # Ensure instance directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            init_db(app_instance=app)
            
            print("✅ Database created and initialized successfully!")
    
    print("\n🎉 Database initialization complete!")

if __name__ == '__main__':
    main() 
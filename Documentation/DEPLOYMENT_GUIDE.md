# Smart Checklist App - Database Persistence Deployment Guide

This guide explains how to deploy the Smart Checklist Flask application with proper database persistence, ensuring that your user data is preserved across deployments and updates.

## 🎯 Problem Solved

The deployment system now:
- ✅ Checks if database exists before initialization
- ✅ Preserves existing user data during updates
- ✅ Automatically initializes database on first deployment
- ✅ Validates database structure and repairs if needed
- ✅ Uses Docker volumes for data persistence

## 🏗️ Architecture Overview

### Database Persistence Strategy
- **Location**: `/app/instance/smartchecklist.sqlite` (inside container)
- **Persistence**: Docker volume mounted to `/app/instance`
- **Initialization**: Automatic on app startup + manual script available
- **Safety**: Non-destructive initialization (checks before creating)

### Key Components
1. **Enhanced `init_db()`**: Non-destructive database initialization
2. **`database_exists_and_initialized()`**: Validates database structure
3. **`ensure_db_initialized()`**: Safe initialization wrapper
4. **`init_database.py`**: Standalone initialization script
5. **Docker Volume**: Persistent storage for database

## 🚀 Deployment Options

### Option 1: Docker with Named Volume (Recommended)

```bash
# Create a named volume for database persistence
docker volume create smartchecklist_data

# Build the image
docker build -t smartchecklist .

# Run with persistent volume
docker run -d \
  --name smartchecklist_app \
  -p 5000:5000 \
  -v smartchecklist_data:/app/instance \
  smartchecklist

# Check database status
docker exec smartchecklist_app python init_database.py
```

### Option 2: Docker with Host Directory Binding

```bash
# Create host directory for database
mkdir -p ./data/instance

# Build and run with host directory binding
docker build -t smartchecklist .

docker run -d \
  --name smartchecklist_app \
  -p 5000:5000 \
  -v $(pwd)/data/instance:/app/instance \
  smartchecklist
```

### Option 3: Docker Compose (Production Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  smartchecklist:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - smartchecklist_data:/app/instance
    restart: unless-stopped
    environment:
      - FLASK_ENV=production

volumes:
  smartchecklist_data:
```

Deploy with:
```bash
docker-compose up -d
```

## 🔄 Update Deployment Process

### Safe Update Steps
1. **Stop the current container** (data persists in volume)
2. **Build new image** with updates
3. **Start new container** with same volume
4. **Database auto-checks** and initializes if needed

```bash
# Update deployment
docker stop smartchecklist_app
docker rm smartchecklist_app

# Rebuild with updates
docker build -t smartchecklist:latest .

# Start with same persistent volume
docker run -d \
  --name smartchecklist_app \
  -p 5000:5000 \
  -v smartchecklist_data:/app/instance \
  smartchecklist:latest
```

## 🛠️ Manual Database Management

### Check Database Status
```bash
# From host
docker exec smartchecklist_app python init_database.py

# Or from inside container
docker exec -it smartchecklist_app /bin/sh
python init_database.py
```

### Force Database Reinitialization (⚠️ Destructive)
```bash
# Only if you want to start fresh (loses all data)
docker exec smartchecklist_app rm -f /app/instance/smartchecklist.sqlite
docker restart smartchecklist_app
```

### Backup Database
```bash
# Copy database out of container
docker cp smartchecklist_app:/app/instance/smartchecklist.sqlite ./backup_$(date +%Y%m%d_%H%M%S).sqlite
```

### Restore Database
```bash
# Copy database into container
docker cp ./backup_file.sqlite smartchecklist_app:/app/instance/smartchecklist.sqlite
docker restart smartchecklist_app
```

## 🧪 Testing the Deployment

### 1. Test Database Persistence
```bash
# Create some test data in the app
# Stop and restart container
docker restart smartchecklist_app
# Verify data still exists
```

### 2. Test Update Deployment
```bash
# Make a small change to the app
# Follow update deployment process
# Verify data persists and app works
```

### 3. Verify Database Structure
```bash
docker exec smartchecklist_app python init_database.py
# Should show ✓ for all checks
```

## 🔍 Troubleshooting

### Database Not Initializing
```bash
# Check logs
docker logs smartchecklist_app

# Manual initialization
docker exec smartchecklist_app python init_database.py
```

### Permission Issues
```bash
# Fix permissions
docker exec smartchecklist_app chmod 755 /app/instance
docker exec smartchecklist_app chown -R root:root /app/instance
```

### Database Corruption
```bash
# Check database file
docker exec smartchecklist_app ls -la /app/instance/

# Test database connection
docker exec smartchecklist_app python -c "
import sqlite3
db = sqlite3.connect('/app/instance/smartchecklist.sqlite')
print('Database connection successful')
db.close()
"
```

## 📋 Production Checklist

- [ ] Database volume is properly mounted
- [ ] Database initializes automatically on first run
- [ ] Existing data persists after updates
- [ ] Database structure validation works
- [ ] Backup strategy is in place
- [ ] Monitoring and logging configured
- [ ] Security best practices applied (secrets, user permissions)

## 🔐 Security Notes

- Database is stored in container volume (not in image layers)
- Use proper secrets management for production SECRET_KEY
- Consider using environment variables for sensitive configuration
- Regular database backups are recommended
- Monitor database file permissions

## 📊 Monitoring

Monitor these aspects in production:
- Database file size growth
- Container restarts and their impact on data
- Database initialization logs
- Application startup time
- Volume usage and disk space 
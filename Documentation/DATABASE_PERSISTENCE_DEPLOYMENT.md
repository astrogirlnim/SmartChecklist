# Database Persistence and Deployment Guide

## Smart Checklist Flask Application

This document provides comprehensive instructions for deploying the Smart Checklist Flask application with robust database persistence, ensuring user data is preserved across deployments and updates.

---

## 🎯 Overview

### Problem Addressed
The Smart Checklist application uses SQLite for data storage. Previously, each deployment would reinitialize the database, potentially causing data loss. This solution implements a safe database persistence system that:

- ✅ Preserves existing user data during updates
- ✅ Automatically initializes database on first deployment  
- ✅ Validates database structure and repairs if needed
- ✅ Uses Docker volumes for reliable data persistence
- ✅ Provides manual tools for database management

### Solution Architecture
- **Database Location**: `/app/instance/smartchecklist.sqlite` (inside container)
- **Persistence Method**: Docker volumes mounted to `/app/instance`
- **Initialization**: Automatic on app startup + manual script available
- **Safety**: Non-destructive initialization with structure validation

---

## 🏗️ Technical Implementation

### Core Components

#### 1. Database Functions (Module Level)
Located in `app.py`:

```python
def database_exists_and_initialized(db_path)
```
- Checks if database file exists
- Validates all required tables are present
- Verifies table structure integrity
- Returns `True` if database is ready for use

```python
def init_db(app_instance=None, db_path=None)
```
- Non-destructive database initialization
- Only creates database if missing or invalid
- Supports both Flask app context and standalone use
- Preserves existing data

```python
def ensure_db_initialized(app_instance=None, db_path=None)
```
- Safe wrapper for database initialization
- Can be called multiple times without side effects
- Used during Flask app startup

#### 2. Automatic Initialization
The Flask application automatically ensures database initialization during startup:

```python
# In create_app() function
with app.app_context():
    ensure_db_initialized(app_instance=app)
```

#### 3. Docker Volume Configuration
Enhanced `Dockerfile` with persistence support:

```dockerfile
# Create volume for database persistence
VOLUME ["/app/instance"]

# Ensure the instance directory exists with proper permissions
RUN mkdir -p /app/instance && chmod 755 /app/instance
```

#### 4. Standalone Initialization Script
`init_database.py` provides manual database management:
- Detailed status reporting
- Database statistics
- Error handling and recovery
- Safe for repeated execution

---

## 🚀 Deployment Options

### Option 1: Docker Compose (Recommended for Production)

**Setup:**
1. Ensure `docker-compose.yml` is configured:
```yaml
version: '3.8'
services:
  smartchecklist:
    build: .
    container_name: smartchecklist_app
    ports:
      - "5000:5000"
    volumes:
      - smartchecklist_data:/app/instance
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:5000/')"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  smartchecklist_data:
```

**Deployment Commands:**
```bash
# Initial deployment
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f

# Verify database
docker exec smartchecklist_app python init_database.py
```

**Update Deployment:**
```bash
# Safe update process
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify data persistence
docker exec smartchecklist_app python init_database.py
```

### Option 2: Docker with Named Volumes

**Setup:**
```bash
# Create persistent volume
docker volume create smartchecklist_data

# Build application image
docker build -t smartchecklist .
```

**Initial Deployment:**
```bash
docker run -d \
  --name smartchecklist_app \
  -p 5000:5000 \
  -v smartchecklist_data:/app/instance \
  --restart unless-stopped \
  smartchecklist
```

**Update Process:**
```bash
# Stop and remove container (data persists in volume)
docker stop smartchecklist_app
docker rm smartchecklist_app

# Rebuild with updates
docker build -t smartchecklist:latest .

# Deploy with same volume
docker run -d \
  --name smartchecklist_app \
  -p 5000:5000 \
  -v smartchecklist_data:/app/instance \
  --restart unless-stopped \
  smartchecklist:latest
```

### Option 3: Docker with Host Directory Binding

**Setup:**
```bash
# Create host directory
mkdir -p ./data/instance
chmod 755 ./data/instance
```

**Deployment:**
```bash
docker build -t smartchecklist .

docker run -d \
  --name smartchecklist_app \
  -p 5000:5000 \
  -v $(pwd)/data/instance:/app/instance \
  --restart unless-stopped \
  smartchecklist
```

**Benefits:**
- Direct access to database file from host
- Easy backup and migration
- Simple file-based persistence

---

## 🛠️ Database Management

### Manual Database Operations

#### Check Database Status
```bash
# From host system
docker exec smartchecklist_app python init_database.py

# From inside container
docker exec -it smartchecklist_app /bin/sh
cd /app
python init_database.py
```

**Expected Output:**
```
Smart Checklist Database Initialization
========================================
Database path: /app/instance/smartchecklist.sqlite
✓ Database file exists
✓ Database is properly initialized with all required tables
✓ Database structure is valid

✅ Database is ready for use!

📊 Database Statistics:
   Users: X
   Checklists: Y
   Items: Z
```

#### Force Database Reset (⚠️ Data Loss)
```bash
# Only if you need to start completely fresh
docker exec smartchecklist_app rm -f /app/instance/smartchecklist.sqlite
docker restart smartchecklist_app

# Verify new database
docker exec smartchecklist_app python init_database.py
```

#### Database Backup
```bash
# Create timestamped backup
docker cp smartchecklist_app:/app/instance/smartchecklist.sqlite \
  ./backup_smartchecklist_$(date +%Y%m%d_%H%M%S).sqlite

# Verify backup
ls -la backup_smartchecklist_*.sqlite
```

#### Database Restore
```bash
# Stop application
docker stop smartchecklist_app

# Restore from backup
docker cp ./backup_smartchecklist_YYYYMMDD_HHMMSS.sqlite \
  smartchecklist_app:/app/instance/smartchecklist.sqlite

# Restart and verify
docker start smartchecklist_app
docker exec smartchecklist_app python init_database.py
```

### CLI Commands (Flask)

The application includes Flask CLI commands for database management:

```bash
# Initialize database (safe, preserves data)
docker exec smartchecklist_app flask init-db

# Check if command is available
docker exec smartchecklist_app flask --help
```

---

## 🧪 Testing and Validation

### Deployment Testing Checklist

#### 1. Fresh Deployment Test
```bash
# Clean environment
docker volume rm smartchecklist_data 2>/dev/null || true
docker rm -f smartchecklist_app 2>/dev/null || true

# Deploy fresh
docker-compose up -d

# Verify auto-initialization
docker exec smartchecklist_app python init_database.py
# Should show: Database created and initialized successfully

# Test application
curl http://localhost:5000/
```

#### 2. Data Persistence Test
```bash
# Create some test data via the web interface
# ... (register user, create checklists, add items)

# Simulate update deployment
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify data still exists
docker exec smartchecklist_app python init_database.py
# Should show: Database is ready for use with existing data
```

#### 3. Database Recovery Test
```bash
# Simulate corrupted database
docker exec smartchecklist_app rm -f /app/instance/smartchecklist.sqlite

# Restart application
docker restart smartchecklist_app

# Verify auto-recovery
docker exec smartchecklist_app python init_database.py
# Should show: Database created and initialized successfully
```

### Database Structure Validation

The system validates these components:
- **Users table**: `id`, `username`, `password` columns
- **Checklists table**: `id`, `user_id`, `title` columns  
- **Items table**: `id`, `checklist_id`, `content`, `checked` columns
- **Foreign key relationships**: Proper table constraints
- **File permissions**: Database file accessibility

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Database Not Initializing
**Symptoms:**
- Application fails to start
- Database connection errors
- Missing tables

**Diagnosis:**
```bash
# Check container logs
docker logs smartchecklist_app

# Check database file
docker exec smartchecklist_app ls -la /app/instance/

# Manual initialization
docker exec smartchecklist_app python init_database.py
```

**Solutions:**
1. Verify volume mount is correct
2. Check file permissions
3. Run manual initialization
4. Rebuild container if persistent issues

#### Permission Denied Errors
**Symptoms:**
- Cannot create database file
- SQLite permission errors

**Solution:**
```bash
# Fix container permissions
docker exec smartchecklist_app chmod 755 /app/instance
docker exec smartchecklist_app chown -R root:root /app/instance

# Restart application
docker restart smartchecklist_app
```

#### Database Corruption
**Symptoms:**
- SQLite error messages
- Inconsistent data
- Application crashes

**Recovery:**
```bash
# Check database integrity
docker exec smartchecklist_app python -c "
import sqlite3
db = sqlite3.connect('/app/instance/smartchecklist.sqlite')
result = db.execute('PRAGMA integrity_check').fetchone()
print('Database integrity:', result[0])
db.close()
"

# If corrupted, restore from backup
# (See Database Restore section above)
```

#### Volume Mount Issues
**Symptoms:**
- Data disappears after restart
- Multiple database instances

**Verification:**
```bash
# Check volume mounts
docker inspect smartchecklist_app | grep -A 10 "Mounts"

# Verify volume existence
docker volume ls | grep smartchecklist

# Check volume data
docker run --rm -v smartchecklist_data:/data alpine ls -la /data
```

### Monitoring and Logs

#### Application Logs
```bash
# Real-time logs
docker-compose logs -f

# Specific time range
docker-compose logs --since 2h

# Filter for database messages
docker-compose logs | grep -i database
```

#### Database Monitoring
```bash
# Database size monitoring
docker exec smartchecklist_app du -h /app/instance/smartchecklist.sqlite

# Table row counts
docker exec smartchecklist_app python -c "
import sqlite3
db = sqlite3.connect('/app/instance/smartchecklist.sqlite')
print('Users:', db.execute('SELECT COUNT(*) FROM users').fetchone()[0])
print('Checklists:', db.execute('SELECT COUNT(*) FROM checklists').fetchone()[0])
print('Items:', db.execute('SELECT COUNT(*) FROM items').fetchone()[0])
db.close()
"
```

---

## 🔐 Security and Best Practices

### Production Security

#### Environment Variables
```bash
# Set secure secret key
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Use in docker-compose.yml
environment:
  - FLASK_ENV=production
  - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
```

#### Database Security
- Database file stored in Docker volume (not in image)
- No database credentials needed (SQLite)
- File permissions properly set
- Regular backup strategy implemented

#### Network Security
```yaml
# docker-compose.yml additions
services:
  smartchecklist:
    networks:
      - app-network
    # Only expose necessary ports

networks:
  app-network:
    driver: bridge
```

### Backup Strategy

#### Automated Backups
```bash
#!/bin/bash
# backup_script.sh
BACKUP_DIR="/backups/smartchecklist"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Create backup
docker cp smartchecklist_app:/app/instance/smartchecklist.sqlite \
  $BACKUP_DIR/smartchecklist_$TIMESTAMP.sqlite

# Keep only last 30 days
find $BACKUP_DIR -name "smartchecklist_*.sqlite" -mtime +30 -delete

echo "Backup completed: smartchecklist_$TIMESTAMP.sqlite"
```

#### Backup Verification
```bash
# Test backup integrity
sqlite3 backup_file.sqlite "PRAGMA integrity_check;"

# Verify table structure
sqlite3 backup_file.sqlite ".schema" | grep "CREATE TABLE"
```

---

## 📋 Production Deployment Checklist

### Pre-Deployment
- [ ] **Environment Setup**
  - [ ] Docker and Docker Compose installed
  - [ ] Required ports (5000) available
  - [ ] Sufficient disk space for database growth
  - [ ] Backup storage configured

- [ ] **Configuration Review**
  - [ ] `docker-compose.yml` configured for production
  - [ ] Environment variables set
  - [ ] Volume mounts properly configured
  - [ ] Health checks enabled

- [ ] **Security**
  - [ ] Secure secret key generated
  - [ ] Network access properly restricted
  - [ ] File permissions reviewed

### Deployment Process
- [ ] **Initial Deployment**
  - [ ] Build application image successfully
  - [ ] Deploy with Docker Compose
  - [ ] Verify database initialization
  - [ ] Test application functionality
  - [ ] Confirm health checks passing

- [ ] **Post-Deployment**
  - [ ] Database backup strategy active
  - [ ] Monitoring and logging configured
  - [ ] Documentation updated
  - [ ] Team trained on management procedures

### Update Process
- [ ] **Pre-Update**
  - [ ] Create database backup
  - [ ] Test update in staging environment
  - [ ] Plan rollback procedure

- [ ] **Update Execution**
  - [ ] Follow safe update process
  - [ ] Verify data persistence
  - [ ] Test application functionality
  - [ ] Monitor for issues

- [ ] **Post-Update**
  - [ ] Verify all features working
  - [ ] Check database integrity
  - [ ] Update documentation if needed

---

## 📊 Monitoring and Maintenance

### Regular Maintenance Tasks

#### Weekly
- [ ] Review application logs
- [ ] Check database file size growth
- [ ] Verify backup integrity
- [ ] Test database connection

#### Monthly  
- [ ] Full database backup
- [ ] Review disk usage
- [ ] Update container images
- [ ] Security review

#### Quarterly
- [ ] Disaster recovery test
- [ ] Performance review
- [ ] Documentation update
- [ ] Team training refresh

### Performance Monitoring
```bash
# Database performance
docker exec smartchecklist_app python -c "
import sqlite3, time
start = time.time()
db = sqlite3.connect('/app/instance/smartchecklist.sqlite')
db.execute('SELECT COUNT(*) FROM users').fetchone()
db.close()
print(f'Query time: {time.time() - start:.3f}s')
"

# Container resource usage
docker stats smartchecklist_app --no-stream
```

---

## 🚀 Advanced Configuration

### Environment-Specific Configurations

#### Development
```yaml
# docker-compose.dev.yml
services:
  smartchecklist:
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    volumes:
      - .:/app:ro  # Read-only code mount for development
      - dev_data:/app/instance
```

#### Staging
```yaml
# docker-compose.staging.yml
services:
  smartchecklist:
    environment:
      - FLASK_ENV=staging
    volumes:
      - staging_data:/app/instance
    deploy:
      resources:
        limits:
          memory: 256M
```

#### Production
```yaml
# docker-compose.prod.yml
services:
  smartchecklist:
    environment:
      - FLASK_ENV=production
    volumes:
      - prod_data:/app/instance
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
    healthcheck:
      interval: 30s
      timeout: 10s
      retries: 5
```

### Database Migration Support

For future schema changes, the framework supports migration scripts:

```python
# Example migration function
def migrate_database_v2(db_path):
    """Migrate database to version 2 schema"""
    if not database_exists_and_initialized(db_path):
        return False
    
    db = get_db_connection(db_path)
    try:
        # Check if migration needed
        result = db.execute("PRAGMA user_version").fetchone()
        current_version = result[0] if result else 0
        
        if current_version < 2:
            # Perform migration
            db.execute("ALTER TABLE users ADD COLUMN email TEXT")
            db.execute("PRAGMA user_version = 2")
            db.commit()
            print("Database migrated to version 2")
        
        return True
    except Exception as e:
        print(f"Migration failed: {e}")
        return False
    finally:
        db.close()
```

---

## 📞 Support and Resources

### Getting Help
- **Application Issues**: Check container logs and database status
- **Database Problems**: Use `init_database.py` for diagnosis
- **Deployment Issues**: Verify Docker volume configuration
- **Performance**: Monitor resource usage and database size

### Additional Resources
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Docker Volumes**: https://docs.docker.com/storage/volumes/
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **Docker Compose**: https://docs.docker.com/compose/

### Emergency Procedures
1. **Application Down**: Check container status and restart if needed
2. **Database Corruption**: Restore from most recent backup
3. **Data Loss**: Review backup files and restore procedure
4. **Performance Issues**: Check resource usage and database size

---

*This documentation is maintained as part of the Smart Checklist application. Last updated: $(date)* 
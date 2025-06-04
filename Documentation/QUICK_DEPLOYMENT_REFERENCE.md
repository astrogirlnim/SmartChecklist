# Quick Deployment Reference

## Smart Checklist - Database Persistence Commands

> **Quick reference for common deployment and database management operations**

---

## 🚀 Quick Deploy Commands

### New Deployment (Docker Compose)
```bash
# Deploy application with persistent database
docker-compose up -d

# Verify database is ready
docker exec smartchecklist_app python init_database.py
```

### Update Deployment
```bash
# Safe update process - preserves all data
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify data persistence
docker exec smartchecklist_app python init_database.py
```

### Manual Docker Deployment
```bash
# Create volume and deploy
docker volume create smartchecklist_data
docker build -t smartchecklist .
docker run -d --name smartchecklist_app -p 5000:5000 \
  -v smartchecklist_data:/app/instance smartchecklist
```

---

## 🛠️ Database Management

### Check Database Status
```bash
# Detailed database status and statistics
docker exec smartchecklist_app python init_database.py

# Quick table counts
docker exec smartchecklist_app python -c "
import sqlite3
db = sqlite3.connect('/app/instance/smartchecklist.sqlite')
print('Users:', db.execute('SELECT COUNT(*) FROM users').fetchone()[0])
print('Checklists:', db.execute('SELECT COUNT(*) FROM checklists').fetchone()[0])
print('Items:', db.execute('SELECT COUNT(*) FROM items').fetchone()[0])
db.close()
"
```

### Backup Database
```bash
# Create timestamped backup
docker cp smartchecklist_app:/app/instance/smartchecklist.sqlite \
  ./backup_$(date +%Y%m%d_%H%M%S).sqlite
```

### Restore Database
```bash
# Stop app, restore, restart
docker stop smartchecklist_app
docker cp ./backup_file.sqlite smartchecklist_app:/app/instance/smartchecklist.sqlite
docker start smartchecklist_app
```

---

## 🔍 Quick Troubleshooting

### App Won't Start
```bash
# Check logs
docker logs smartchecklist_app

# Check database file exists
docker exec smartchecklist_app ls -la /app/instance/

# Force database initialization
docker exec smartchecklist_app python init_database.py
```

### Database Issues
```bash
# Check database integrity
docker exec smartchecklist_app python -c "
import sqlite3
db = sqlite3.connect('/app/instance/smartchecklist.sqlite')
print(db.execute('PRAGMA integrity_check').fetchone()[0])
db.close()
"

# Reset database (⚠️ DATA LOSS)
docker exec smartchecklist_app rm -f /app/instance/smartchecklist.sqlite
docker restart smartchecklist_app
```

### Permission Problems
```bash
# Fix file permissions
docker exec smartchecklist_app chmod 755 /app/instance
docker exec smartchecklist_app chown -R root:root /app/instance
docker restart smartchecklist_app
```

---

## 📊 Monitoring

### Container Status
```bash
# Check if running
docker-compose ps

# Resource usage
docker stats smartchecklist_app --no-stream

# Live logs
docker-compose logs -f
```

### Database Monitoring
```bash
# Database file size
docker exec smartchecklist_app du -h /app/instance/smartchecklist.sqlite

# Connection test
docker exec smartchecklist_app python -c "
import sqlite3
db = sqlite3.connect('/app/instance/smartchecklist.sqlite')
print('✅ Database connection successful')
db.close()
"
```

---

## 🔐 Production Commands

### Secure Deployment
```bash
# Generate secure secret key
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Deploy with production settings
docker-compose -f docker-compose.yml up -d
```

### Backup Script
```bash
#!/bin/bash
# Daily backup script
BACKUP_DIR="/backups/smartchecklist"
mkdir -p $BACKUP_DIR
docker cp smartchecklist_app:/app/instance/smartchecklist.sqlite \
  $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sqlite
```

---

## ⚠️ Emergency Procedures

### Application Down
1. `docker-compose ps` - Check container status
2. `docker-compose logs` - Check error logs  
3. `docker-compose restart` - Restart if needed
4. `docker exec smartchecklist_app python init_database.py` - Verify database

### Data Recovery
1. Stop application: `docker stop smartchecklist_app`
2. List backups: `ls -la backup_*.sqlite`
3. Restore: `docker cp backup_file.sqlite smartchecklist_app:/app/instance/smartchecklist.sqlite`
4. Restart: `docker start smartchecklist_app`
5. Verify: `docker exec smartchecklist_app python init_database.py`

### Complete Reset (⚠️ All Data Lost)
```bash
docker-compose down
docker volume rm smartchecklist_data
docker-compose up -d
```

---

## 📋 Health Checks

### Pre-Deployment Checklist
- [ ] Docker and Docker Compose installed
- [ ] Port 5000 available
- [ ] Sufficient disk space
- [ ] Previous database backed up

### Post-Deployment Verification
- [ ] `docker-compose ps` shows healthy status
- [ ] `curl http://localhost:5000/` returns HTML
- [ ] `docker exec smartchecklist_app python init_database.py` shows ✅
- [ ] Application accessible in browser

### Update Verification
- [ ] Previous data still visible in application
- [ ] All features working correctly
- [ ] Database statistics match expectations
- [ ] No error logs in `docker-compose logs`

---

*For detailed information, see [DATABASE_PERSISTENCE_DEPLOYMENT.md](./DATABASE_PERSISTENCE_DEPLOYMENT.md)* 
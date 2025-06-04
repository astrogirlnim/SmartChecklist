# 🌿 SmartChecklist

> *Where productivity meets organic simplicity*

SmartChecklist is a mindfully designed task management application that embraces the philosophy of digital minimalism. Built with muted earth tones and organic design elements, it provides a peaceful environment for organizing your daily tasks and long-term goals. Like leaves on a tree or stones in a riverbed, every task finds its perfect place in the natural rhythm of your day.

## ✨ Philosophy & Design

SmartChecklist strips away the chaos of overwhelming productivity apps, leaving only what matters: your tasks, your progress, and your peace of mind. The interface draws inspiration from natural materials—clay, sage, warm wood—creating a tactile, organic experience that feels as natural as breathing.

## 🎯 Key Features

### 🌱 **Naturally Organized**
- Create checklists that grow organically with your needs
- Intuitive task organization without rigid structures
- Seamless workflow adaptation

### 🏞️ **Mindful Design**
- Calming earth-tone palette (browns, sage greens, clay reds)
- Organic textures and subtle animations
- Typography inspired by natural materials

### ⚡ **Effortless Flow**
- Add tasks, check them off, create new lists
- No complicated features to learn
- Essential tools for staying organized

### 🔐 **Secure & Private**
- User registration and authentication
- Secure password hashing with Werkzeug
- Personal sanctuary for your thoughts and plans

### 📱 **Responsive Experience**
- Beautiful on desktop, tablet, and mobile
- Organic animations and hover effects
- Staggered loading for natural feel

## 🛠️ Technical Specifications

### **Backend Stack**
- **Framework**: Flask 3.0.2 (Python web framework)
- **Authentication**: Flask-Login 0.6.3 (session management)
- **Database**: SQLite 3 (embedded database)
- **Security**: Werkzeug 3.0.1 (password hashing, security utilities)
- **ORM**: Raw SQL with sqlite3 (lightweight approach)

### **Frontend Stack**
- **Templates**: Jinja2 (Flask's template engine)
- **Styling**: Custom CSS3 with CSS Variables
- **Icons**: Font Awesome 6.5.1
- **Typography**: Charter, Georgia, Playfair Display (serif fonts)
- **Animations**: CSS3 keyframes and transitions

### **Design System**
- **Color Palette**: Muted earth tones
  - Primary: `#8b7355` (warm brown)
  - Sage Green: `#9caf88` 
  - Clay Red: `#c49484`
  - Warm Accent: `#b5956b`
- **Typography**: Serif-based for organic feel
- **Animations**: Organic floating, rustle effects, clay pulse
- **Textures**: SVG noise patterns for natural texture

### **Architecture Patterns**
- **MVC Pattern**: Model-View-Controller separation
- **Template Inheritance**: DRY principle with base templates
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Core functionality works without JavaScript

### **Development Tools**
- **Version Control**: Git
- **Environment**: Python virtual environment (venv)
- **Development Server**: Flask built-in development server
- **Debugging**: Flask debugger with PIN protection

## 📋 Requirements

### **System Requirements**
- Python 3.8+ (tested with Python 3.11.3)
- SQLite 3 (usually included with Python)
- Modern web browser with CSS3 support

### **Dependencies**
```txt
Flask==3.0.2
Flask-Login==0.6.3
Werkzeug==3.0.1
```

## 🚀 Setup Instructions

### **1. Clone the Repository**
```bash
git clone <your-repository-url>
cd SimpleToDoApp
```

### **2. Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Initialize Database**
```bash
# Using Flask CLI (recommended)
flask --app app init-db

# Alternative method if the above doesn't work
python -c "from app import init_db; init_db()"
```

### **5. Run the Application**
```bash
# Method 1: Direct Python execution
python app.py

# Method 2: Using Flask CLI
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
flask run
```

### **6. Access the Application**
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## 🐳 Production Deployment

### **Database Persistence**
SmartChecklist includes a robust database persistence system that ensures your data is preserved across deployments and updates. The system automatically:

- ✅ **Preserves existing user data** during application updates
- ✅ **Automatically initializes database** on first deployment
- ✅ **Validates database structure** and repairs if needed
- ✅ **Uses Docker volumes** for reliable data persistence

### **Quick Deployment (Docker)**
```bash
# Deploy with persistent database
docker-compose up -d

# Verify database status
docker exec smartchecklist_app python init_database.py
```

### **Update Deployment**
```bash
# Safe update process - preserves all user data
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### **📖 Complete Documentation**
For comprehensive deployment instructions, database management, troubleshooting, and production best practices, see:

- **[Database Persistence & Deployment Guide](./Documentation/DATABASE_PERSISTENCE_DEPLOYMENT.md)** - Complete implementation details and deployment options
- **[Quick Reference](./Documentation/QUICK_DEPLOYMENT_REFERENCE.md)** - Common commands and troubleshooting steps

## 🎮 Usage Guide

### **Getting Started**
1. **Welcome**: Visit the organic splash page with nature-inspired descriptions
2. **Register**: Create your account with username and password
3. **Dashboard**: View your personal collection of checklists
4. **Create**: Add new checklists that grow with your needs
5. **Organize**: Add tasks and check them off as you complete them

### **Navigation Flow**
```
Splash Page → Sign Up/Sign In → Dashboard → Checklist View → Task Management
```

### **Core Workflows**
- **Account Management**: Register → Login → Use App → Logout
- **List Management**: Create Checklist → Add Items → Check Off Tasks
- **Organization**: Multiple Lists → Switch Between Lists → Track Progress

## 🗂️ Project Structure

```
SimpleToDoApp/
├── app.py                 # Main Flask application
├── schema.sql            # Database schema
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── static/
│   ├── styles.css       # Organic design CSS
│   └── script.js        # Frontend JavaScript
├── templates/
│   ├── base.html        # Base template with navigation
│   ├── splash.html      # Landing page with features
│   ├── login.html       # Authentication form
│   ├── register.html    # User registration
│   ├── dashboard.html   # Checklist overview
│   └── checklist.html   # Individual checklist view
├── instance/            # Instance-specific files (gitignored)
│   └── smartchecklist.sqlite  # SQLite database
└── venv/               # Virtual environment (gitignored)
```

## 🔒 Security Features

- **Password Security**: Werkzeug PBKDF2 password hashing
- **Session Management**: Flask-Login secure session handling
- **SQL Injection Prevention**: Parameterized queries
- **CSRF Protection**: Built-in Flask security features
- **Secure Secrets**: Random secret key generation

## 🎨 Design Principles

### **Digital Minimalism**
- Essential features only
- No overwhelming productivity bloat
- Focus on what matters most

### **Organic Aesthetics**
- Earth-tone color palette
- Natural texture overlays
- Organic animation patterns
- Serif typography for warmth

### **Mindful UX**
- Calming visual hierarchy
- Intuitive navigation flow
- Peaceful interaction patterns
- Stress-free task management

## 🧪 Development & Testing

### **Local Development**
```bash
# Run in debug mode
python app.py  # Debug mode enabled by default

# Check application status
curl -s http://127.0.0.1:5000/
```

### **Code Quality**
- Clean, readable Python code
- Consistent naming conventions
- Modular template structure
- Responsive CSS architecture

## 🚀 Deployment Considerations

### **Production Setup**
- Use production WSGI server (Gunicorn, uWSGI)
- Set `FLASK_ENV=production`
- Use PostgreSQL for production database
- Configure proper secret key management
- Enable HTTPS with SSL certificates

### **Environment Variables**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with organic design principles
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for your own mindful productivity needs.

## 🌱 Future Enhancements

- **Drag & Drop**: Organic task reordering
- **Categories**: Natural grouping with earth-tone tags
- **Collaboration**: Peaceful shared checklists
- **Mobile App**: Native organic mobile experience
- **Sync**: Cross-device harmony
- **Themes**: Additional nature-inspired palettes

---

*"Like placing stones on a cairn, every completed task is a step forward on your personal journey of growth and achievement."* 
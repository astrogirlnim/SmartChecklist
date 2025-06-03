# SmartChecklist Build Process

## Problem Statement

The SmartChecklist project has a **dual directory structure** that can cause confusion during builds:

```
SimpleToDoApp/
├── static/           # ← Root level files (where you make changes)
├── templates/        # ← Root level files (where you make changes)  
├── app.py           # ← Root level files (where you make changes)
├── smartchecklist/  # ← Package directory (what gets built into wheel)
│   ├── static/      # ← Package level files (can become outdated)
│   ├── templates/   # ← Package level files (can become outdated)
│   └── app.py       # ← Package level files (can become outdated)
└── pyproject.toml   # ← Build config points to smartchecklist/ directory
```

**The Issue**: When you add new functionality (like delete buttons) to the root-level files, the wheel build uses the `smartchecklist/` directory files, which may be outdated. This results in wheels missing your latest features.

## Solution: Automated Sync Script

The `sync_and_build.sh` script solves this by:

1. **Syncing files** from root level → package level
2. **Cleaning** old build artifacts  
3. **Building** a fresh wheel
4. **Verifying** the wheel contains your latest changes

## Usage

### Quick Start
```bash
# Make the script executable (first time only)
chmod +x sync_and_build.sh

# Run the script
./sync_and_build.sh
```

### When to Use
Run this script whenever you:
- Add new features to root-level files
- Modify CSS, JavaScript, or templates
- Update Python routes in `app.py`
- Want to ensure your wheel has the latest changes

### Script Output
The script provides detailed feedback:
```
🔄 Starting smartchecklist wheel build process...

📁 Syncing static files...
   • Copying static/script.js → smartchecklist/static/script.js
   ✅ Static files synced

📄 Syncing template files...
   • Copying templates/checklist.html → smartchecklist/templates/checklist.html
   ✅ Template files synced

🧹 Cleaning old build artifacts...
   ✅ Build artifacts cleaned

🔨 Building new wheel...
   ✅ Build completed successfully!

🔍 Quick verification:
   ✅ Delete functions found in script.js
   ✅ Delete buttons found in checklist.html
   
🚀 Your wheel is ready for deployment!
```

## Files Synced

The script automatically syncs these files from root → package:

### Static Files
- `static/script.js` → `smartchecklist/static/script.js`
- `static/styles.css` → `smartchecklist/static/styles.css`

### Template Files  
- `templates/base.html` → `smartchecklist/templates/base.html`
- `templates/checklist.html` → `smartchecklist/templates/checklist.html`
- `templates/dashboard.html` → `smartchecklist/templates/dashboard.html`
- `templates/login.html` → `smartchecklist/templates/login.html`
- `templates/register.html` → `smartchecklist/templates/register.html`
- `templates/splash.html` → `smartchecklist/templates/splash.html`

### Other Files
- `app.py` → `smartchecklist/app.py` 
- `schema.sql` → `smartchecklist/schema.sql`

## Verification

The script automatically verifies that your wheel contains:
- ✅ Delete functions in JavaScript
- ✅ Delete buttons in templates
- ✅ All latest functionality

## Deployment

After running the script, install the wheel:
```bash
pip install dist/smartchecklist-1.0.0-py3-none-any.whl --force-reinstall
```

## Alternative: Manual Process

If you prefer manual control, you can run these steps individually:

```bash
# 1. Sync files manually
cp static/script.js smartchecklist/static/script.js
cp static/styles.css smartchecklist/static/styles.css
cp templates/*.html smartchecklist/templates/
cp app.py smartchecklist/app.py
cp schema.sql smartchecklist/schema.sql

# 2. Clean build artifacts
rm -rf dist/ build/ *.egg-info/

# 3. Build wheel
python -m build --wheel

# 4. Verify (optional)
python -m zipfile -l dist/smartchecklist-1.0.0-py3-none-any.whl
```

## Troubleshooting

### Script Fails
- Ensure you're in the project root directory
- Check that both root and package directories exist
- Verify Python build tools are installed: `pip install build`

### Missing Features in Wheel
- Run the script again to ensure all files are synced
- Check the verification output for any ❌ indicators
- Manually inspect the wheel contents if needed

### Build Warnings
The build process may show warnings about missing image files - these are safe to ignore if you're not using images in your static directory.

---

**💡 Pro Tip**: Add this script to your development workflow and run it before every deployment to ensure consistency! 
#!/bin/sh

# sync_and_build.sh - Automated script to sync files and rebuild the smartchecklist wheel
# 
# This script solves the issue where new functionality is added to root-level files 
# (static/, templates/) but the wheel is built from the smartchecklist/ package 
# directory, which contains older versions.

set -e  # Exit on any error

echo "🔄 Starting smartchecklist wheel build process..."
echo ""

# Step 1: Sync static files from root to package directory
echo "📁 Syncing static files..."
if [ -d "static" ] && [ -d "smartchecklist/static" ]; then
    echo "   • Copying static/script.js → smartchecklist/static/script.js"
    cp static/script.js smartchecklist/static/script.js
    
    echo "   • Copying static/styles.css → smartchecklist/static/styles.css"
    cp static/styles.css smartchecklist/static/styles.css
    
    echo "   ✅ Static files synced"
else
    echo "   ⚠️  Warning: static directories not found, skipping..."
fi

echo ""

# Step 2: Sync template files from root to package directory  
echo "📄 Syncing template files..."
if [ -d "templates" ] && [ -d "smartchecklist/templates" ]; then
    echo "   • Copying templates/checklist.html → smartchecklist/templates/checklist.html"
    cp templates/checklist.html smartchecklist/templates/checklist.html
    
    echo "   • Copying templates/dashboard.html → smartchecklist/templates/dashboard.html"
    cp templates/dashboard.html smartchecklist/templates/dashboard.html
    
    echo "   • Copying templates/base.html → smartchecklist/templates/base.html"
    cp templates/base.html smartchecklist/templates/base.html
    
    echo "   • Copying templates/login.html → smartchecklist/templates/login.html"
    cp templates/login.html smartchecklist/templates/login.html
    
    echo "   • Copying templates/register.html → smartchecklist/templates/register.html"
    cp templates/register.html smartchecklist/templates/register.html
    
    echo "   • Copying templates/splash.html → smartchecklist/templates/splash.html"
    cp templates/splash.html smartchecklist/templates/splash.html
    
    echo "   ✅ Template files synced"
else
    echo "   ⚠️  Warning: template directories not found, skipping..."
fi

echo ""

# Step 3: Sync other important files
echo "🗄️  Syncing other files..."
if [ -f "schema.sql" ]; then
    echo "   • Copying schema.sql → smartchecklist/schema.sql"
    cp schema.sql smartchecklist/schema.sql
    echo "   ✅ Schema file synced"
fi

if [ -f "app.py" ] && [ -f "smartchecklist/app.py" ]; then
    echo "   • Copying app.py → smartchecklist/app.py"
    cp app.py smartchecklist/app.py
    echo "   ✅ App file synced"
fi

echo ""

# Step 4: Clean old build artifacts
echo "🧹 Cleaning old build artifacts..."
echo "   • Removing dist/ directory..."
rm -rf dist/

echo "   • Removing build/ directory..."
rm -rf build/

echo "   • Removing *.egg-info directories..."
rm -rf *.egg-info/

echo "   ✅ Build artifacts cleaned"
echo ""

# Step 5: Build new wheel
echo "🔨 Building new wheel..."
echo "   • Running: python -m build --wheel"
python -m build --wheel

echo ""
echo "🎉 Build completed successfully!"
echo ""

# Step 6: Show build results
if [ -f "dist/smartchecklist-1.0.0-py3-none-any.whl" ]; then
    echo "📦 New wheel created: dist/smartchecklist-1.0.0-py3-none-any.whl"
    wheel_size=$(ls -lh dist/smartchecklist-1.0.0-py3-none-any.whl | awk '{print $5}')
    echo "   • Size: $wheel_size"
    echo ""
    
    echo "🚀 Your wheel is ready for deployment!"
    echo "   Run: pip install dist/smartchecklist-1.0.0-py3-none-any.whl --force-reinstall"
else
    echo "❌ Error: Wheel file not found after build"
    exit 1
fi

echo ""
echo "💡 Tip: Run this script whenever you update files in the root directory"
echo "    to ensure your wheel includes all the latest changes." 
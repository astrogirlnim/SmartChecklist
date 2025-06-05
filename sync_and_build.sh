#!/bin/sh

# sync_and_build.sh - Automated script to sync files and rebuild the smartchecklist wheel
# 
# This script solves the issue where new functionality is added to root-level files 
# (static/, templates/) but the wheel is built from the smartchecklist/ package 
# directory, which contains older versions.

set -e  # Exit on any error

echo "🔄 Starting smartchecklist wheel build process..."
echo ""

# Step 1: Sync static files from package to root (package is the source of truth)
echo "📁 Syncing static files..."
if [ -d "smartchecklist/static" ]; then
    mkdir -p static
    echo "   • Copying smartchecklist/static/* → static/"
    cp smartchecklist/static/* static/
    echo "   ✅ Static files synced from package to root"
else
    echo "   ⚠️  Warning: smartchecklist/static directory not found, skipping..."
fi

echo ""

# Step 2: Sync template files from package to root (package is the source of truth)
echo "📄 Syncing template files..."
if [ -d "smartchecklist/templates" ]; then
    mkdir -p templates
    echo "   • Copying smartchecklist/templates/* → templates/"
    cp smartchecklist/templates/*.html templates/
    echo "   ✅ Template files synced from package to root"
else
    echo "   ⚠️  Warning: smartchecklist/templates directory not found, skipping..."
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
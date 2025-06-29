#!/bin/bash

echo "🎬 Framepack Generator Pro"
echo "========================"
echo ""
echo "Starting application..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run install.sh first to set up the application."
    echo ""
    read -p "Press any key to continue..."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    echo ""
    read -p "Press any key to continue..."
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Start the application
echo "🚀 Launching Framepack Generator Pro..."
echo ""
echo "The application will be available at:"
echo "http://127.0.0.1:7861"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

python app.py

# If we get here, the application has stopped
echo ""
echo "🛑 Application stopped"
echo ""
read -p "Press any key to continue..."
#!/bin/bash

# Investor-Entrepreneur Chatbot Setup Script
echo "🚀 Setting up Investor-Entrepreneur Chatbot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

VENV_DIR=".venv"

# Check if venv is available
if ! python3 -m venv --help &> /dev/null; then
    echo "❌ python3-venv is required but not installed."
    echo "Please install it using your system's package manager (e.g., 'sudo apt-get install python3-venv')."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creating Python virtual environment in '$VENV_DIR'..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        exit 1
    fi
    echo "✅ Virtual environment created."
else
    echo "🐍 Virtual environment already exists."
fi

# Activate virtual environment to install packages
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    deactivate
    exit 1
fi

# Deactivate the environment after installation
deactivate

# Create activation script
echo "📝 Creating activation script (env.sh)..."
cat > env.sh << EOL
#!/bin/bash
# This script activates the Python virtual environment.
# Run it with 'source env.sh' before starting the server.

source .venv/bin/activate
echo "✅ Chatbot environment activated. You can now run 'python3 chatbot.py'"
EOL
chmod +x env.sh
echo "✅ Activation script created."

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 To start the chatbot server:"
echo "   1. Activate the environment: source env.sh"
echo "   2. Start the server: python3 chatbot.py"
echo ""
echo "📡 The server will run at: http://localhost:8080"
echo ""
echo "📖 See INTEGRATION_GUIDE.md for detailed integration examples."

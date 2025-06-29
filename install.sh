#!/bin/bash

# Framepack Generator Pro - Linux/macOS Installation Script
# Bash script for automated setup

echo "🎬 Framepack Generator Pro - Installation Script"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✅ Found: $(python3 --version)${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}✅ Found: $(python --version)${NC}"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo -e "${RED}❌ Python 3.8+ required. Current version: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python version check passed${NC}"

# Check if pip is installed
echo -e "${YELLOW}Checking pip installation...${NC}"
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}❌ pip not found. Please install pip${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip found${NC}"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Removing old one...${NC}"
    rm -rf venv
fi

$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment created${NC}"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Check for CUDA availability
echo -e "${YELLOW}Checking for CUDA support...${NC}"
CUDA_AVAILABLE=false
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        echo -e "${GREEN}✅ NVIDIA GPU detected${NC}"
        CUDA_AVAILABLE=true
    fi
else
    echo -e "${YELLOW}⚠️  No NVIDIA GPU detected, using CPU mode${NC}"
fi

# Install PyTorch with CUDA 12.8 support if available
if [ "$CUDA_AVAILABLE" = true ]; then
    echo -e "${YELLOW}Installing PyTorch with CUDA 12.8 support...${NC}"
    pip install --pre torch==2.8.0.dev20250324+cu128 torchvision==0.22.0.dev20250325+cu128 torchaudio==2.6.0.dev20250325+cu128 --index-url https://download.pytorch.org/whl/nightly/cu128
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  CUDA installation failed, falling back to CPU version...${NC}"
        pip install torch torchvision torchaudio
    else
        echo -e "${GREEN}✅ PyTorch with CUDA 12.8 installed${NC}"
    fi
else
    echo -e "${YELLOW}Installing PyTorch (CPU version)...${NC}"
    pip install torch torchvision torchaudio
fi

# Install other requirements
echo -e "${YELLOW}Installing application dependencies...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies installed successfully${NC}"

# Create necessary directories
echo -e "${YELLOW}Creating application directories...${NC}"
directories=("generated_prompts" "history" "uploads" "exports")
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✅ Created directory: $dir${NC}"
    fi
done

# Test installation
echo -e "${YELLOW}Testing installation...${NC}"
python -c "import torch, transformers, gradio, PIL, cv2, numpy, pandas; print('✅ All imports successful')"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi

# Create run script
echo -e "${YELLOW}Creating run script...${NC}"
cat > run.sh << 'EOF'
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
EOF

chmod +x run.sh
echo -e "${GREEN}✅ Run script created: run.sh${NC}"

# Installation complete
echo ""
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo -e "${CYAN}=================================================${NC}"
echo ""
echo -e "${NC}To start the application:${NC}"
echo -e "${YELLOW}1. Run: ./run.sh OR${NC}"
echo -e "${YELLOW}2. Run: source venv/bin/activate && python app.py${NC}"
echo ""
echo -e "${CYAN}The application will be available at: http://127.0.0.1:7861${NC}"
echo ""
echo -e "${NC}For support, visit: https://github.com/Valorking6/framepack-generator-pro${NC}"
echo ""
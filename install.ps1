# Framepack Generator Pro - Windows Installation Script
# PowerShell script for automated setup

Write-Host "🎬 Framepack Generator Pro - Installation Script" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check Python version
$versionString = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$version = [float]$versionString
if ($version -lt 3.8) {
    Write-Host "❌ Python 3.8+ required. Current version: $versionString" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python version check passed" -ForegroundColor Green

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Removing old one..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}

python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Check for CUDA availability
Write-Host "Checking for CUDA support..." -ForegroundColor Yellow
$cudaAvailable = $false
try {
    $nvidiaSmi = nvidia-smi 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ NVIDIA GPU detected" -ForegroundColor Green
        $cudaAvailable = $true
    }
} catch {
    Write-Host "⚠️  No NVIDIA GPU detected, using CPU mode" -ForegroundColor Yellow
}

# Install PyTorch with CUDA 12.8 support if available
if ($cudaAvailable) {
    Write-Host "Installing PyTorch with CUDA 12.8 support..." -ForegroundColor Yellow
    pip install --pre torch==2.8.0.dev20250324+cu128 torchvision==0.22.0.dev20250325+cu128 torchaudio==2.6.0.dev20250325+cu128 --index-url https://download.pytorch.org/whl/nightly/cu128
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  CUDA installation failed, falling back to CPU version..." -ForegroundColor Yellow
        pip install torch torchvision torchaudio
    } else {
        Write-Host "✅ PyTorch with CUDA 12.8 installed" -ForegroundColor Green
    }
} else {
    Write-Host "Installing PyTorch (CPU version)..." -ForegroundColor Yellow
    pip install torch torchvision torchaudio
}

# Install other requirements
Write-Host "Installing application dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green

# Create necessary directories
Write-Host "Creating application directories..." -ForegroundColor Yellow
$directories = @("generated_prompts", "history", "uploads", "exports")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Test installation
Write-Host "Testing installation..." -ForegroundColor Yellow
python -c "import torch, transformers, gradio, PIL, cv2, numpy, pandas; print('✅ All imports successful')"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation test failed" -ForegroundColor Red
    exit 1
}

# Create run script
Write-Host "Creating run script..." -ForegroundColor Yellow
$runScript = @"
@echo off
echo 🎬 Starting Framepack Generator Pro...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python app.py
pause
"@

$runScript | Out-File -FilePath "run.bat" -Encoding ASCII

Write-Host "✅ Run script created: run.bat" -ForegroundColor Green

# Installation complete
Write-Host ""
Write-Host "🎉 Installation completed successfully!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor White
Write-Host "1. Double-click 'run.bat' OR" -ForegroundColor Yellow
Write-Host "2. Run: .\venv\Scripts\Activate.ps1 && python app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "The application will be available at: http://127.0.0.1:7861" -ForegroundColor Cyan
Write-Host ""
Write-Host "For support, visit: https://github.com/Valorking6/framepack-generator-pro" -ForegroundColor White

# Pause to show results
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
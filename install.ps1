# Framepack Generator Pro - Windows Installation Script
# PowerShell script for automated setup

Write-Host "🎬 Framepack Generator Pro - Installation Script" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersionOutput = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed"
    }
    Write-Host "✅ Found: $pythonVersionOutput" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Write-Host "   Make sure Python is added to your PATH environment variable." -ForegroundColor Red
    exit 1
}

# Check Python version using proper version comparison
Write-Host "Verifying Python version compatibility..." -ForegroundColor Yellow
try {
    # Get the full version string (e.g., "3.10.11")
    $fullVersionString = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to get Python version details"
    }
    
    # Parse versions using PowerShell's Version class for proper comparison
    $currentVersion = [System.Version]$fullVersionString
    $requiredVersion = [System.Version]"3.8.0"
    
    Write-Host "   Current Python version: $fullVersionString" -ForegroundColor White
    Write-Host "   Required Python version: 3.8.0 or higher" -ForegroundColor White
    
    if ($currentVersion -lt $requiredVersion) {
        Write-Host "❌ Python 3.8+ required. Current version: $fullVersionString is too old." -ForegroundColor Red
        Write-Host "   Please upgrade Python to version 3.8 or higher from https://python.org" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Python version check passed ($fullVersionString >= 3.8.0)" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to verify Python version: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Please ensure Python is properly installed and accessible." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Removing old one..." -ForegroundColor Yellow
    try {
        Remove-Item -Recurse -Force "venv" -ErrorAction Stop
    } catch {
        Write-Host "❌ Failed to remove existing virtual environment. Please delete the 'venv' folder manually and try again." -ForegroundColor Red
        exit 1
    }
}

python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    Write-Host "   This might be due to insufficient permissions or disk space." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & "venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        throw "Activation script failed"
    }
} catch {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "   You may need to enable script execution: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Failed to upgrade pip, continuing with current version..." -ForegroundColor Yellow
}

# Check for CUDA availability
Write-Host "Checking for CUDA support..." -ForegroundColor Yellow
$cudaAvailable = $false
try {
    $nvidiaSmi = nvidia-smi 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ NVIDIA GPU detected" -ForegroundColor Green
        $cudaAvailable = $true
    } else {
        Write-Host "⚠️  No NVIDIA GPU detected, using CPU mode" -ForegroundColor Yellow
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
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to install PyTorch" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✅ PyTorch with CUDA 12.8 installed" -ForegroundColor Green
    }
} else {
    Write-Host "Installing PyTorch (CPU version)..." -ForegroundColor Yellow
    pip install torch torchvision torchaudio
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install PyTorch" -ForegroundColor Red
        exit 1
    }
}

# Install other requirements
Write-Host "Installing application dependencies..." -ForegroundColor Yellow
if (!(Test-Path "requirements.txt")) {
    Write-Host "❌ requirements.txt file not found" -ForegroundColor Red
    Write-Host "   Please ensure you're running this script from the framepack-generator-pro directory." -ForegroundColor Red
    exit 1
}

pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Write-Host "   Check the error messages above for specific package installation issues." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green

# Create necessary directories
Write-Host "Creating application directories..." -ForegroundColor Yellow
$directories = @("generated_prompts", "history", "uploads", "exports")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        try {
            New-Item -ItemType Directory -Path $dir -ErrorAction Stop | Out-Null
            Write-Host "✅ Created directory: $dir" -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed to create directory: $dir" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✅ Directory already exists: $dir" -ForegroundColor Green
    }
}

# Test installation
Write-Host "Testing installation..." -ForegroundColor Yellow
python -c "import torch, transformers, gradio, PIL, cv2, numpy, pandas; print('✅ All imports successful')"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation test failed" -ForegroundColor Red
    Write-Host "   Some required packages may not have installed correctly." -ForegroundColor Red
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

try {
    $runScript | Out-File -FilePath "run.bat" -Encoding ASCII -ErrorAction Stop
    Write-Host "✅ Run script created: run.bat" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create run script" -ForegroundColor Red
    exit 1
}

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
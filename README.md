
# Framepack Generator Pro

🎬 **AI-Powered Video Prompt Generator with Multi-Provider Support**

Framepack Generator Pro is an intelligent tool designed to analyze uploaded images and generate optimized video prompts specifically tailored for framepack and hunyuan AI video generation tools. Now featuring support for **OpenAI GPT-4 Vision**, **Google Gemini Vision**, and local **BLIP** analysis with automatic fallback capabilities.

## ✨ Features

- **🤖 Multi-Provider AI Analysis**: Choose between OpenAI GPT-4 Vision, Google Gemini Vision, or local BLIP
- **🔄 Automatic Fallback**: Seamlessly switches between providers if one fails
- **🖼️ Advanced Image Analysis**: AI-powered image recognition with detailed scene understanding
- **⏱️ Precise Timing Control**: Generate prompts with exact timestamp markers ([1s: action] format)
- **🎥 Dynamic Camera Work**: Varied shots, movements, and creative effects
- **📝 Dual Output Formats**: Both timestamp and detailed Hunyuan narrative formats
- **⚙️ Customizable Duration**: 5-120 second video sequences with intelligent scaling
- **🔄 Batch Processing**: Handle multiple images simultaneously
- **💾 Export Options**: JSON, TXT, and CSV export formats
- **🎯 Professional Interface**: Clean, intuitive Gradio-based web interface
- **🔐 Secure API Management**: Local storage of API keys with easy setup

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NVIDIA GPU with CUDA support (optional, CPU mode available)
- 4GB+ RAM recommended
- API keys for enhanced analysis (optional):
  - OpenAI API key for GPT-4 Vision
  - Google AI Studio API key for Gemini Vision

### Windows Installation

1. **Download and extract** the project files
2. **Run the installer** (as Administrator):
   ```powershell
   .\install.ps1
   ```
3. **Start the application**:
   ```batch
   run.bat
   ```

### Linux/macOS Installation

1. **Clone or download** the project:
   ```bash
   git clone https://github.com/Valorking6/framepack-generator-pro.git
   cd framepack-generator-pro
   ```

2. **Run the installer**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Start the application**:
   ```bash
   ./run.sh
   ```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 🔑 API Setup

### OpenAI API Key Setup

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with "sk-")
5. Enter it in the Settings tab under "OpenAI API Key"

### Google AI Studio API Key Setup

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Enter it in the Settings tab under "Google AI Studio API Key"

**Note**: API keys are stored locally and used only for image analysis. The application works without API keys using local BLIP analysis.

## 📖 Usage Guide

### 1. Configure AI Provider

1. Go to the **"Settings"** tab
2. Choose your preferred **AI Analysis Provider**:
   - **OpenAI**: Best for detailed, contextual analysis
   - **Google**: Fast processing with good multimodal reasoning
   - **BLIP**: Free local analysis, works offline
3. Enter your API keys if using OpenAI or Google
4. Enable **"API Fallback"** for automatic provider switching
5. Click **"Save API Settings"**

### 2. Basic Prompt Generation

1. **Upload an image** (JPG, PNG, WebP supported)
2. **Adjust duration** using the slider (5-120 seconds)
3. **Add custom actions** (optional) like "waves hello" or "starts dancing"
4. **Choose output format**: Timestamp, Hunyuan, or Both
5. **Click "Generate Video Prompt"**

### 3. Understanding Output Formats

#### Timestamp Format
```
[0s: Wide shot of subject in garden, shallow depth of field]; [2s: Dolly in smoothly as subject raises hand to wave]; [4s: Quick pan right with motion blur as subject walks]; [6s: Pull focus to flowers in foreground while tracking subject]
```

#### Hunyuan Format
```
The camera opens with a brightly lit garden with natural tones, creating an inviting outdoor atmosphere. The subject, wearing casual clothing, is positioned center frame in a medium composition stands gracefully in the frame. The camera smoothly transitions, adopting a medium shot while executing a dolly in, capturing as the subject raises hand to wave with natural grace and authentic expression...
```

### 4. Batch Processing

1. Go to the **"Batch Processing"** tab
2. **Upload multiple images** at once
3. **Click "Process Batch"**
4. **Download results** as CSV file with provider information

### 5. Provider Comparison

| Provider | Pros | Cons | Best For |
|----------|------|------|----------|
| **OpenAI GPT-4 Vision** | Excellent detail, context understanding, creative descriptions | Requires API key, costs per request | Professional content, detailed analysis |
| **Google Gemini Vision** | Fast processing, good multimodal reasoning, cost-effective | Requires API key | Quick analysis, batch processing |
| **BLIP Local** | Free, works offline, no API required, reliable | Basic descriptions, less creative | Offline use, basic analysis |

## 🛠️ Technical Details

### Core Components

- **`app.py`**: Main Gradio interface with multi-provider support
- **`image_analyzer.py`**: Enhanced image analysis with API integration
- **`prompt_generator.py`**: Intelligent prompt generation with timing
- **`utils.py`**: File management, configuration, and utilities
- **`settings.json`**: Configuration including API settings

### AI Models and APIs

- **OpenAI GPT-4 Vision**: Advanced multimodal understanding
- **Google Gemini Vision**: Fast multimodal AI processing
- **BLIP (Salesforce)**: Local image captioning fallback
- **OpenCV**: Computer vision for technical analysis
- **Custom Algorithms**: Camera movement and timing optimization

### Supported Formats

- **Input**: JPG, PNG, WebP, BMP, TIFF
- **Output**: JSON, TXT, CSV
- **Video Duration**: 5-120 seconds
- **Timestamp Precision**: 1-second intervals

## 📁 Project Structure

```
framepack-generator-pro/
├── app.py                 # Main application with multi-provider UI
├── image_analyzer.py      # Enhanced image analysis module
├── prompt_generator.py    # Prompt generation engine
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies (updated)
├── settings.json         # Configuration with API settings
├── install.ps1          # Windows installer
├── install.sh           # Linux/macOS installer
├── run.bat              # Windows launcher
├── run.sh               # Linux/macOS launcher
├── generated_prompts/   # Output directory
├── history/             # Generation history
└── uploads/             # Temporary uploads
```

## 🎯 Use Cases

### Content Creators
- Generate professional video prompts from reference images
- Choose the best AI provider for your workflow
- Create consistent visual narratives with fallback reliability

### Digital Marketers
- Transform product photos into engaging video concepts
- Batch process campaign assets efficiently
- Use cost-effective providers for large-scale processing

### Film & Video Professionals
- Rapid prototyping of video sequences with detailed analysis
- Storyboard development with multiple AI perspectives
- Creative inspiration with provider-specific strengths

## ⚙️ Configuration

### API Settings
```json
{
  "api_settings": {
    "provider": "openai",
    "openai_api_key": "sk-...",
    "google_api_key": "AI...",
    "fallback_enabled": true
  }
}
```

### Model Settings
```json
{
  "model_settings": {
    "blip_model": "Salesforce/blip-image-captioning-base",
    "device": "auto",
    "max_length": 50
  }
}
```

## 🔧 Troubleshooting

### Common Issues

**API Key Errors:**
- Verify API keys are correctly entered in Settings
- Check API key permissions and quotas
- Enable fallback to use alternative providers

**Installation fails on Windows:**
- Run PowerShell as Administrator
- Enable execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Import errors for API clients:**
- Install missing packages: `pip install openai google-generativeai`
- Application will work with BLIP if API packages are missing

**Memory errors:**
- Reduce batch size
- Use smaller images (max 2048x2048 recommended)
- Close other applications

### Performance Optimization

- **API Selection**: OpenAI for quality, Google for speed, BLIP for offline
- **Fallback Strategy**: Enable fallback for reliability
- **Image Size**: Resize large images to 1024x1024 for optimal performance
- **Batch Size**: Process 5-10 images at a time for best results

## 🆕 What's New in v1.1

- ✅ **Multi-Provider Support**: OpenAI GPT-4 Vision and Google Gemini Vision
- ✅ **Automatic Fallback**: Seamless provider switching
- ✅ **Enhanced UI**: API key management and provider selection
- ✅ **Improved Analysis**: More detailed and creative descriptions
- ✅ **Better Error Handling**: Clear error messages and recovery
- ✅ **Provider Tracking**: See which AI analyzed each image
- ✅ **Secure Storage**: Local API key management

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Valorking6/framepack-generator-pro.git
cd framepack-generator-pro

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI**: For GPT-4 Vision API and excellent multimodal capabilities
- **Google**: For Gemini Vision API and AI Studio platform
- **Salesforce BLIP**: For the excellent image captioning model
- **Hugging Face**: For the transformers library and model hosting
- **Gradio**: For the intuitive web interface framework
- **OpenCV**: For computer vision capabilities
- **Content Creator Community**: For inspiration and feedback

## 📞 Support

- **Documentation**: [Wiki](https://github.com/Valorking6/framepack-generator-pro/wiki)
- **Issues**: [GitHub Issues](https://github.com/Valorking6/framepack-generator-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Valorking6/framepack-generator-pro/discussions)

## 🗺️ Roadmap

- [ ] **v1.2**: Video preview generation with selected provider
- [ ] **v1.3**: Custom model training interface
- [ ] **v1.4**: API endpoints for integration
- [ ] **v1.5**: Cloud deployment options
- [ ] **v1.6**: Multi-language support
- [ ] **v1.7**: Advanced prompt templates

---

**Made with ❤️ for content creators worldwide**

*Transform your images into cinematic video prompts with the power of multiple AI providers*

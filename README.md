# 🎬 Framepack Generator Pro

**AI-Powered Video Prompt Generator with Multi-Provider Support**

Transform your images into professional video prompts using cutting-edge AI vision models including OpenAI GPT-4 Vision, Google Gemini Vision, and local BLIP analysis.

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 🤖 Multi-Provider AI Support
- **OpenAI GPT-4 Vision**: Industry-leading image understanding with exceptional detail and context awareness
- **Google Gemini Vision**: Fast, efficient multimodal AI with excellent reasoning capabilities
- **BLIP Local**: Free, offline image captioning that works without API keys
- **Intelligent Fallback**: Automatic provider switching ensures analysis always succeeds

### 🎯 Advanced Video Prompt Generation
- **Dual Output Formats**: Generate both timestamp-based and narrative-style prompts
- **Customizable Duration**: Support for 5-120 second video sequences
- **Custom Actions**: Incorporate specific actions and movements into generated prompts
- **Professional Analysis**: Comprehensive scene, lighting, composition, and color analysis

### 🔄 Batch Processing
- Process multiple images simultaneously
- CSV export for bulk results
- Efficient workflow for content creators

### ⚙️ Professional Interface
- Modern, responsive Gradio web interface
- Real-time provider status and feedback
- Comprehensive settings management
- Built-in help and documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- CUDA-compatible GPU (optional, for faster local processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Valorking6/framepack-generator-pro.git
   cd framepack-generator-pro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://127.0.0.1:7861`

## 🔑 API Setup

### OpenAI API Key
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with "sk-")
5. Enter it in the Settings tab

### Google AI Studio API Key
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Enter it in the Settings tab

**Note**: API keys are stored locally and used only for image analysis. Keep them secure!

## 📖 Usage Guide

### Basic Usage

1. **Setup Provider** (Optional but recommended)
   - Go to Settings tab
   - Choose your preferred AI provider
   - Enter your API key
   - Enable fallback for reliability

2. **Generate Single Prompt**
   - Upload an image (JPG, PNG, WebP)
   - Adjust duration slider (5-120 seconds)
   - Add custom actions if desired
   - Choose output format
   - Click "Generate Video Prompt"

3. **Batch Processing**
   - Go to Batch Processing tab
   - Upload multiple images
   - Click "Process Batch"
   - Download CSV results

### Output Formats

#### Timestamp Format
Precise timing for video editing:
```
[1s: Subject stands confidently in the center]
[3s: Camera slowly zooms in on their face]
[5s: Subject begins to smile warmly]
[8s: Gentle head tilt to the right]
[10s: Eyes look directly at camera]
```

#### Hunyuan Format
Narrative description for fluid motion:
```
A confident person stands in the center of the frame, their posture relaxed yet assured. As the camera slowly draws closer, capturing the subtle details of their expression, a warm smile begins to form. The subject's head tilts gently, creating a more intimate connection with the viewer...
```

## 🎨 AI Provider Comparison

| Provider | Strengths | Best For | Cost |
|----------|-----------|----------|---------|
| **OpenAI GPT-4 Vision** | Exceptional detail, context understanding, creative descriptions | Professional content, detailed analysis | Paid API |
| **Google Gemini Vision** | Fast processing, good multimodal reasoning, reliable | Quick workflows, batch processing | Paid API |
| **BLIP Local** | Free, offline, privacy-focused, reliable | Basic descriptions, no API costs | Free |

## 🛠️ Configuration

### Settings File Structure
```json
{
  "api_settings": {
    "provider": "openai",
    "openai_api_key": "your-key-here",
    "google_api_key": "your-key-here",
    "fallback_enabled": true
  },
  "generation_settings": {
    "default_duration": 30,
    "default_fps": 30,
    "min_duration": 5,
    "max_duration": 120
  }
}
```

### Environment Variables (Optional)
```bash
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-key
```

## 📁 Project Structure

```
framepack-generator-pro/
├── app.py                 # Main Gradio application
├── image_analyzer.py      # Multi-provider image analysis
├── prompt_generator.py    # Video prompt generation logic
├── utils.py              # Utility functions
├── settings.json         # Application configuration
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── generated_prompts/   # Output directory
├── history/            # Generation history
└── uploads/           # Temporary uploads
```

## 🔧 Advanced Features

### Custom Actions
Enhance your prompts with specific actions:
- "waves hello" - Adds greeting gesture
- "starts dancing" - Incorporates dance movements
- "looks around" - Adds environmental awareness
- "adjusts clothing" - Includes wardrobe interactions

### Batch Processing
- Upload multiple images at once
- Consistent settings across all images
- CSV export with all results
- Progress tracking and error handling

### Fallback System
- Automatic provider switching on failure
- Graceful degradation to local models
- Comprehensive error reporting
- Ensures 100% analysis success rate

## 🐛 Troubleshooting

### Common Issues

**API Analysis Fails**
- Check your API keys in Settings
- Verify internet connection
- Ensure API quota is available
- Enable fallback for automatic recovery

**Slow Processing**
- Large images take longer to process
- API providers may have rate limits
- Local BLIP processing depends on hardware

**Installation Issues**
- Ensure Python 3.8+ is installed
- Use virtual environment to avoid conflicts
- Check CUDA installation for GPU acceleration

### Error Messages

| Error | Solution |
|-------|----------|
| "OpenAI API key required" | Add valid API key in Settings |
| "Google AI analysis failed" | Check API key and quota |
| "BLIP model loading failed" | Restart application, check disk space |
| "Image format not supported" | Use JPG, PNG, or WebP formats |

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Salesforce BLIP** - Local image captioning model
- **OpenAI** - GPT-4 Vision API
- **Google** - Gemini Vision API
- **Gradio** - Web interface framework
- **Hugging Face** - Transformers library

## 📞 Support

For support, please:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information
4. Join our community discussions

## 🔮 Roadmap

### Upcoming Features
- [ ] Video analysis support
- [ ] More AI provider integrations
- [ ] Advanced prompt templates
- [ ] API rate limiting management
- [ ] Cloud deployment options
- [ ] Mobile-responsive interface

### Version History

**v1.1.0** (Current)
- ✅ Multi-provider AI support (OpenAI, Google AI)
- ✅ Intelligent fallback system
- ✅ Enhanced UI with provider status
- ✅ Comprehensive settings management
- ✅ Batch processing improvements

**v1.0.0**
- ✅ Initial release with BLIP support
- ✅ Basic prompt generation
- ✅ Gradio web interface

---

**Made with ❤️ for content creators and AI enthusiasts**

*Transform your creative vision into compelling video prompts with the power of AI*
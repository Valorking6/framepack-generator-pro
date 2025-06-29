# 🎬 Framepack Generator Pro

**AI-Powered Video Prompt Generator for Hunyuan Video Creation**

Framepack Generator Pro is a sophisticated AI tool that analyzes uploaded images and generates optimized video prompts specifically designed for framepack and Hunyuan AI video generation platforms. Perfect for content creators, influencers, and digital marketers looking to streamline their video content production workflow with professional-grade prompts.

## ✨ Key Features

### 🧠 Advanced AI Analysis
- **BLIP Model Integration**: State-of-the-art image captioning using Salesforce's BLIP model
- **Computer Vision Processing**: OpenCV-powered scene, lighting, and composition analysis
- **Intelligent Subject Detection**: Automatic identification of poses, clothing, and positioning
- **Color Psychology Analysis**: Mood and atmosphere detection from color palettes

### ⏱️ Precision Timing Control
- **Timestamp Format**: Generate precise `[1s: action] [3s: action]` format prompts
- **Dynamic Duration Scaling**: 5-120 second sequences with intelligent complexity scaling
- **Custom Action Integration**: Seamlessly incorporate user-defined actions into sequences
- **Professional Camera Work**: Varied shots, movements, and cinematic effects

### 🎥 Dual Output Formats
- **Timestamp Format**: Perfect for framepack tools requiring precise timing markers
- **Hunyuan Format**: Detailed narrative descriptions for fluid, natural motion
- **Flexible Export**: Choose individual formats or export both simultaneously

### 🚀 Performance & Efficiency
- **CUDA 12.8 Support**: Optimized for latest NVIDIA GPUs with fallback to CPU
- **Batch Processing**: Handle multiple images simultaneously for workflow efficiency
- **Smart Caching**: Intelligent model loading and memory management
- **Export Options**: JSON, TXT, and CSV formats for various workflows

### 🎨 Professional Interface
- **Gradio Web UI**: Clean, intuitive browser-based interface
- **Real-time Preview**: Instant prompt generation and preview
- **Progress Tracking**: Visual feedback for batch operations
- **Responsive Design**: Works seamlessly across devices

## 🚀 Quick Start Guide

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 4GB+ RAM recommended (8GB+ for batch processing)
- **GPU**: NVIDIA GPU with CUDA 12.8 support (optional, CPU mode available)
- **Storage**: 2GB+ free space for models and dependencies

### Windows Installation

1. **Download** the latest release or clone the repository
2. **Run installer** as Administrator:
   ```powershell
   .\install.ps1
   ```
3. **Launch application**:
   ```batch
   run.bat
   ```

### Linux/macOS Installation

1. **Clone repository**:
   ```bash
   git clone https://github.com/Valorking6/framepack-generator-pro.git
   cd framepack-generator-pro
   ```

2. **Run installer**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Launch application**:
   ```bash
   ./run.sh
   ```

### Manual Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install PyTorch with CUDA 12.8 (if GPU available)
pip install --pre torch==2.8.0.dev20250324+cu128 torchvision==0.22.0.dev20250325+cu128 torchaudio==2.6.0.dev20250325+cu128 --index-url https://download.pytorch.org/whl/nightly/cu128

# Install dependencies
pip install -r requirements.txt

# Launch application
python app.py
```

## 📖 Comprehensive Usage Guide

### 1. Single Image Processing

1. **Upload Image**: Drag and drop or click to upload (JPG, PNG, WebP, BMP, TIFF)
2. **Configure Settings**:
   - **Duration**: Adjust slider from 5-120 seconds
   - **Custom Action**: Add specific actions like "waves hello" or "starts dancing"
   - **Output Format**: Choose Timestamp, Hunyuan, or Both
3. **Generate**: Click "Generate Video Prompt" for instant results
4. **Export**: Download prompts in your preferred format

### 2. Batch Processing Workflow

1. Navigate to **"Batch Processing"** tab
2. **Upload Multiple Images**: Select multiple files simultaneously
3. **Process Batch**: Click to generate prompts for all images
4. **Download Results**: Export comprehensive CSV with all generated prompts

### 3. Understanding Output Formats

#### Timestamp Format Example
```
[0s: Wide shot of subject in garden, shallow depth of field]; 
[2s: Dolly in smoothly as subject raises hand to wave]; 
[4s: Quick pan right with motion blur as subject walks]; 
[6s: Pull focus to flowers in foreground while tracking subject]; 
[8s: Close-up shot with bokeh effect as subject smiles warmly]
```

#### Hunyuan Format Example
```
The camera opens with a brightly lit garden with natural tones, creating an inviting outdoor atmosphere. The subject, wearing casual blue clothing, is positioned center frame in a medium composition stands gracefully in the frame. The camera smoothly transitions, adopting a medium shot while executing a dolly in, capturing as the subject raises hand to wave with natural grace and authentic expression. With fluid movement, the camera shifts to close-up with quick pan right, following the subject's walk in a way that feels organic and unforced...
```

### 4. Advanced Configuration

#### Model Settings
- **BLIP Model**: Choose between base and large models
- **Device Selection**: Auto-detect GPU or force CPU mode
- **Max Length**: Configure caption length limits

#### Generation Settings
- **Default Duration**: Set preferred video length
- **FPS Configuration**: Adjust frame rate (default: 30fps)
- **Quality Presets**: Choose between speed and quality

#### Export Settings
- **Auto-save**: Enable automatic prompt saving
- **Format Preferences**: Set default export formats
- **File Management**: Configure cleanup and organization

## 🛠️ Technical Architecture

### Core Components

- **`app.py`**: Main Gradio interface and application orchestration
- **`image_analyzer.py`**: Advanced image analysis using BLIP and OpenCV
- **`prompt_generator.py`**: Intelligent prompt generation with timing algorithms
- **`utils.py`**: File management, configuration, and utility functions

### AI Models & Technologies

- **BLIP (Salesforce)**: Image captioning and scene understanding
- **OpenCV**: Computer vision for technical analysis
- **scikit-learn**: Color clustering and pattern recognition
- **Custom Algorithms**: Camera movement optimization and timing calculation

### Supported Formats

| Category | Formats |
|----------|----------|
| **Input Images** | JPG, JPEG, PNG, WebP, BMP, TIFF |
| **Output Files** | JSON, TXT, CSV |
| **Video Duration** | 5-120 seconds |
| **Timing Precision** | 1-second intervals |

## 📁 Project Structure

```
framepack-generator-pro/
├── 📄 app.py                 # Main application entry point
├── 🧠 image_analyzer.py      # AI-powered image analysis
├── ✍️ prompt_generator.py     # Intelligent prompt generation
├── 🔧 utils.py              # Utility functions and helpers
├── 📋 requirements.txt      # Python dependencies
├── ⚙️ settings.json         # Application configuration
├── 🪟 install.ps1          # Windows installation script
├── 🐧 install.sh           # Linux/macOS installation script
├── 🪟 run.bat              # Windows launcher
├── 📝 README.md            # This documentation
├── 📂 generated_prompts/   # Output directory for prompts
├── 📂 history/             # Generation history and logs
├── 📂 uploads/             # Temporary file storage
└── 📂 venv/                # Virtual environment (created during install)
```

## 🎯 Use Cases & Applications

### Content Creators
- **Social Media**: Generate engaging video concepts from photos
- **YouTube**: Create professional video sequences for tutorials and vlogs
- **TikTok**: Develop trending video ideas with precise timing
- **Instagram**: Transform static posts into dynamic video content

### Digital Marketing
- **Product Videos**: Convert product photos into compelling video narratives
- **Brand Content**: Maintain consistent visual storytelling across campaigns
- **Advertisement**: Create professional video concepts for marketing materials
- **E-commerce**: Generate product demonstration video prompts

### Film & Video Production
- **Pre-visualization**: Rapid prototyping of video sequences
- **Storyboarding**: AI-assisted storyboard development
- **Creative Direction**: Generate inspiration for camera work and movement
- **Client Presentations**: Quick concept visualization for pitches

### Education & Training
- **Film Studies**: Teach cinematography concepts through AI analysis
- **Content Creation Courses**: Demonstrate professional video planning
- **Marketing Education**: Show video content strategy development

## ⚙️ Configuration & Customization

### Model Configuration
```json
{
  "model_settings": {
    "blip_model": "Salesforce/blip-image-captioning-base",
    "device": "auto",
    "max_length": 50
  }
}
```

### Generation Parameters
```json
{
  "generation_settings": {
    "default_duration": 30,
    "default_fps": 30,
    "min_duration": 5,
    "max_duration": 120
  }
}
```

### Output Preferences
```json
{
  "output_settings": {
    "default_format": "both",
    "export_formats": ["json", "txt", "csv"],
    "auto_save": true
  }
}
```

## 🔧 Troubleshooting & Support

### Common Issues & Solutions

#### Installation Problems

**Windows PowerShell Execution Policy**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Python Version Conflicts**:
- Ensure Python 3.8+ is installed
- Use `python --version` to verify
- Consider using `python3` command on Linux/macOS

**CUDA Installation Issues**:
- Verify NVIDIA drivers: `nvidia-smi`
- Check CUDA compatibility with your GPU
- Application automatically falls back to CPU mode

#### Runtime Issues

**Memory Errors**:
- Reduce batch size for large image sets
- Use smaller images (recommended: 1024x1024 max)
- Close other memory-intensive applications
- Consider upgrading RAM for heavy usage

**Model Loading Failures**:
- Check internet connection for initial model download
- Verify sufficient disk space (2GB+ required)
- Clear cache and restart application

**Import Errors**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify virtual environment activation
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Performance Optimization

#### GPU Optimization
- **CUDA Memory**: Monitor GPU memory usage with `nvidia-smi`
- **Batch Size**: Adjust based on available VRAM
- **Model Selection**: Use base model for faster processing, large for quality

#### CPU Optimization
- **Thread Count**: Application automatically uses available CPU cores
- **Memory Management**: Close unnecessary applications
- **Image Preprocessing**: Resize large images before processing

#### Storage Optimization
- **Cleanup**: Enable auto-cleanup in settings
- **Export Management**: Regularly archive old exports
- **Cache Management**: Clear model cache if disk space is limited

## 🤝 Contributing & Development

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### Development Setup

```bash
# Clone repository
git clone https://github.com/Valorking6/framepack-generator-pro.git
cd framepack-generator-pro

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # Windows: dev-env\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy pre-commit

# Set up pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v
```

### Code Style & Standards

- **Formatting**: Use `black` for code formatting
- **Linting**: Follow `flake8` guidelines
- **Type Hints**: Use `mypy` for type checking
- **Documentation**: Maintain comprehensive docstrings
- **Testing**: Write tests for new features

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Reporting Issues

When reporting issues, please include:
- **System Information**: OS, Python version, GPU details
- **Error Messages**: Complete error logs and stack traces
- **Reproduction Steps**: Clear steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Screenshots**: Visual evidence when applicable

## 📄 License & Legal

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- **BLIP Model**: Salesforce Research License
- **Gradio**: Apache License 2.0
- **OpenCV**: Apache License 2.0
- **PyTorch**: BSD License

## 🙏 Acknowledgments & Credits

### AI Models & Research
- **Salesforce Research**: For the excellent BLIP image captioning model
- **Hugging Face**: For the transformers library and model hosting infrastructure
- **OpenAI**: For inspiration in AI-powered content generation

### Open Source Libraries
- **Gradio Team**: For the intuitive web interface framework
- **OpenCV Contributors**: For comprehensive computer vision capabilities
- **PyTorch Team**: For the robust deep learning framework
- **scikit-learn**: For machine learning utilities

### Community
- **Content Creator Community**: For feedback, testing, and feature requests
- **AI Research Community**: For advancing the field of computer vision
- **Open Source Contributors**: For making this project possible

## 📞 Support & Community

### Documentation & Resources
- **📚 Wiki**: [Comprehensive Documentation](https://github.com/Valorking6/framepack-generator-pro/wiki)
- **🎥 Video Tutorials**: [YouTube Playlist](https://youtube.com/playlist?list=framepack-tutorials)
- **📖 API Documentation**: [API Reference](https://github.com/Valorking6/framepack-generator-pro/docs/api)

### Community Channels
- **💬 Discussions**: [GitHub Discussions](https://github.com/Valorking6/framepack-generator-pro/discussions)
- **🐛 Issues**: [Bug Reports & Feature Requests](https://github.com/Valorking6/framepack-generator-pro/issues)
- **💡 Ideas**: [Feature Suggestions](https://github.com/Valorking6/framepack-generator-pro/discussions/categories/ideas)

### Professional Support
- **📧 Email**: support@framepack-generator-pro.com
- **💼 Enterprise**: enterprise@framepack-generator-pro.com
- **🎓 Education**: education@framepack-generator-pro.com

## 🗺️ Roadmap & Future Development

### Version 1.1 (Q3 2025)
- [ ] **Video Preview Generation**: Real-time video preview from prompts
- [ ] **Advanced Camera Controls**: Manual camera movement customization
- [ ] **Style Transfer**: Apply artistic styles to generated prompts
- [ ] **Prompt Templates**: Pre-built templates for common scenarios

### Version 1.2 (Q4 2025)
- [ ] **Custom Model Training**: Train models on user-specific content
- [ ] **Multi-language Support**: Internationalization for global users
- [ ] **Cloud Integration**: Cloud-based processing and storage
- [ ] **Collaboration Tools**: Team sharing and project management

### Version 1.3 (Q1 2026)
- [ ] **API Endpoints**: RESTful API for integration with other tools
- [ ] **Plugin System**: Extensible architecture for third-party plugins
- [ ] **Mobile App**: Native mobile applications for iOS and Android
- [ ] **Real-time Collaboration**: Live editing and sharing capabilities

### Version 1.4 (Q2 2026)
- [ ] **Advanced AI Models**: Integration with latest vision-language models
- [ ] **3D Scene Understanding**: Support for 3D scene analysis
- [ ] **Voice Integration**: Voice commands and audio prompt generation
- [ ] **AR/VR Support**: Extended reality content creation tools

### Long-term Vision
- **AI Director**: Fully autonomous video direction and editing
- **Industry Integration**: Direct integration with major video platforms
- **Educational Platform**: Comprehensive learning resources and certification
- **Enterprise Solutions**: Large-scale deployment and management tools

---

<div align="center">

**🎬 Transform Your Images Into Cinematic Video Prompts**

*Made with ❤️ for content creators worldwide*

[![GitHub Stars](https://img.shields.io/github/stars/Valorking6/framepack-generator-pro?style=social)](https://github.com/Valorking6/framepack-generator-pro/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Valorking6/framepack-generator-pro?style=social)](https://github.com/Valorking6/framepack-generator-pro/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Valorking6/framepack-generator-pro)](https://github.com/Valorking6/framepack-generator-pro/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[⭐ Star this project](https://github.com/Valorking6/framepack-generator-pro) • [🐛 Report Bug](https://github.com/Valorking6/framepack-generator-pro/issues) • [💡 Request Feature](https://github.com/Valorking6/framepack-generator-pro/discussions)

</div>
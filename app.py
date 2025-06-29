
import gradio as gr
import json
import os
from datetime import datetime
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import cv2
import numpy as np
from image_analyzer import ImageAnalyzer
from prompt_generator import PromptGenerator
import pandas as pd

class FramepackGeneratorPro:
    def __init__(self):
        self.settings = self.load_settings()
        self.image_analyzer = ImageAnalyzer(self.settings)
        self.prompt_generator = PromptGenerator()
        
    def load_settings(self):
        """Load application settings with config.json integration"""
        # First try to load from config.json (new config system)
        config_settings = self.load_config_file()
        
        default_settings = {
            "model_settings": {
                "blip_model": "Salesforce/blip-image-captioning-base",
                "device": "auto",
                "max_length": 50
            },
            "api_settings": {
                "provider": "blip",
                "openai_api_key": "",
                "google_api_key": "",
                "huggingface_api_key": "",
                "fallback_enabled": True
            },
            "generation_settings": {
                "default_duration": 30,
                "default_fps": 30,
                "min_duration": 5,
                "max_duration": 120
            },
            "output_settings": {
                "default_format": "both",
                "export_formats": ["json", "txt", "csv"],
                "auto_save": True
            },
            "ui_settings": {
                "theme": "default",
                "show_advanced": False,
                "auto_analyze": True
            },
            "file_settings": {
                "max_history_files": 100,
                "max_export_files": 50,
                "auto_cleanup": True
            }
        }
        
        # Merge config settings with defaults
        if config_settings:
            # Map config.json structure to app settings
            if "ai_services" in config_settings:
                ai_services = config_settings["ai_services"]
                if "openai" in ai_services:
                    default_settings["api_settings"]["openai_api_key"] = ai_services["openai"].get("api_key", "")
                if "huggingface" in ai_services:
                    default_settings["api_settings"]["huggingface_api_key"] = ai_services["huggingface"].get("api_key", "")
                    default_settings["model_settings"]["blip_model"] = ai_services["huggingface"].get("model", "Salesforce/blip-image-captioning-base")
            
            if "prompt_generation" in config_settings:
                prompt_config = config_settings["prompt_generation"]
                default_settings["generation_settings"]["default_duration"] = prompt_config.get("max_prompt_length", 30) // 10  # rough conversion
            
            if "app" in config_settings:
                app_config = config_settings["app"]
                default_settings["ui_settings"]["debug"] = app_config.get("debug", False)
        
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_settings.items():
                        if key not in loaded_settings:
                            loaded_settings[key] = value
                        elif isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subkey not in loaded_settings[key]:
                                    loaded_settings[key][subkey] = subvalue
                    return loaded_settings
            except Exception as e:
                print(f"Error loading settings: {e}")
        return default_settings
    
    def load_config_file(self):
        """Load configuration from config.json file"""
        config_paths = ["config.json", "config.example.json", "/home/ubuntu/Uploads/config.example.json"]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r") as f:
                        config = json.load(f)
                        print(f"✅ Loaded configuration from {config_path}")
                        return config
                except Exception as e:
                    print(f"❌ Error loading config from {config_path}: {e}")
        
        print("ℹ️ No config file found, using defaults")
        return None
    
    def save_settings(self, settings):
        """Save application settings"""
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=2)
        # Update image analyzer with new settings
        self.settings = settings
        self.image_analyzer.update_settings(settings)
    
    def update_api_settings(self, provider, openai_key, google_key, huggingface_key, fallback_enabled):
        """Update API settings and reinitialize analyzers"""
        self.settings["api_settings"]["provider"] = provider
        self.settings["api_settings"]["openai_api_key"] = openai_key
        self.settings["api_settings"]["google_api_key"] = google_key
        self.settings["api_settings"]["huggingface_api_key"] = huggingface_key
        self.settings["api_settings"]["fallback_enabled"] = fallback_enabled
        
        self.save_settings(self.settings)
        
        # Validate API keys
        status_messages = []
        if provider == "openai" and not openai_key:
            status_messages.append("⚠️ OpenAI API key is required for OpenAI provider")
        elif provider == "google" and not google_key:
            status_messages.append("⚠️ Google AI API key is required for Google AI provider")
        elif provider == "huggingface" and not huggingface_key:
            status_messages.append("⚠️ Hugging Face API key is required for Hugging Face provider")
        
        if not status_messages:
            status_messages.append("✅ API settings updated successfully!")
        
        return "\n".join(status_messages)
    
    def generate_video_prompt(self, image, duration, custom_action, output_format):
        """Main function to generate video prompts from uploaded image"""
        if image is None:
            return "Please upload an image first.", "", None
        
        try:
            # Analyze the uploaded image
            analysis = self.image_analyzer.analyze_image(image)
            
            # Add debugging information
            debug_info = ""
            if self.settings.get("ui_settings", {}).get("debug", False):
                debug_info = f"**🔍 Debug Info:**\n"
                debug_info += f"- Basic Description: {analysis.get('basic_description', 'None')[:100]}...\n"
                debug_info += f"- Scene: {analysis.get('scene_details', {}).get('setting', 'unknown')} ({analysis.get('scene_details', {}).get('environment', 'unknown')})\n"
                debug_info += f"- Subject: {analysis.get('subject_analysis', {}).get('clothing', 'unknown')} at {analysis.get('subject_analysis', {}).get('position', 'unknown')}\n"
                debug_info += f"- Lighting: {analysis.get('lighting_analysis', {}).get('brightness', 'unknown')} with {analysis.get('lighting_analysis', {}).get('color_temperature', 'unknown')} temperature\n\n"
            
            # Generate prompts based on analysis
            timestamp_prompt, hunyuan_prompt = self.prompt_generator.generate_prompts(
                analysis, duration, custom_action
            )
            
            # Add provider info to output
            provider_info = f"**Analysis Provider:** {analysis.get('analysis_provider', 'unknown')}\n\n"
            provider_info += debug_info
            
            # Format output based on user preference
            if output_format == "Timestamp Only":
                display_output = f"{provider_info}**Timestamp Format:**\n{timestamp_prompt}"
                export_data = {"timestamp": timestamp_prompt, "hunyuan": ""}
            elif output_format == "Hunyuan Only":
                display_output = f"{provider_info}**Hunyuan Format:**\n{hunyuan_prompt}"
                export_data = {"timestamp": "", "hunyuan": hunyuan_prompt}
            else:  # Both
                display_output = f"{provider_info}**Timestamp Format:**\n{timestamp_prompt}\n\n**Hunyuan Format:**\n{hunyuan_prompt}"
                export_data = {"timestamp": timestamp_prompt, "hunyuan": hunyuan_prompt}
            
            # Save to history
            self.save_to_history(analysis, timestamp_prompt, hunyuan_prompt, duration, custom_action)
            
            return display_output, self.create_export_file(export_data), "✅ Prompt generated successfully!"
            
        except Exception as e:
            return f"❌ Error generating prompt: {str(e)}", None, "❌ Generation failed"
    
    def create_export_file(self, data):
        """Create export file with generated prompts"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_prompts/framepack_prompt_{timestamp}.json"
        
        os.makedirs("generated_prompts", exist_ok=True)
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "timestamp_prompt": data["timestamp"],
            "hunyuan_prompt": data["hunyuan"],
            "generator": "Framepack Generator Pro v1.1"
        }
        
        with open(filename, "w") as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    def save_to_history(self, analysis, timestamp_prompt, hunyuan_prompt, duration, custom_action):
        """Save generation to history"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "timestamp_prompt": timestamp_prompt,
            "hunyuan_prompt": hunyuan_prompt,
            "duration": duration,
            "custom_action": custom_action
        }
        
        os.makedirs("history", exist_ok=True)
        history_file = "history/generation_history.json"
        
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r") as f:
                    history = json.load(f)
            except:
                history = []
        
        history.append(history_entry)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
    
    def batch_process(self, files):
        """Process multiple images at once"""
        if not files:
            return "Please upload images for batch processing.", None
        
        results = []
        for file_obj in files:
            try:
                image = Image.open(file_obj.name).convert('RGB')
                analysis = self.image_analyzer.analyze_image(image)
                timestamp_prompt, hunyuan_prompt = self.prompt_generator.generate_prompts(
                    analysis, 30, ""  # Default 30s, no custom action
                )
                
                results.append({
                    "filename": os.path.basename(file_obj.name),
                    "analysis_provider": analysis.get('analysis_provider', 'unknown'),
                    "timestamp_prompt": timestamp_prompt,
                    "hunyuan_prompt": hunyuan_prompt
                })
            except Exception as e:
                results.append({
                    "filename": os.path.basename(file_obj.name),
                    "analysis_provider": "error",
                    "timestamp_prompt": f"Error: {str(e)}",
                    "hunyuan_prompt": f"Error: {str(e)}"
                })
        
        # Create CSV export
        df = pd.DataFrame(results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"generated_prompts/batch_results_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        
        summary = f"Processed {len(results)} images successfully.\n\n"
        for result in results[:5]:  # Show first 5 results
            summary += f"**{result['filename']}** ({result['analysis_provider']}): \n{result['timestamp_prompt'][:100]}...\n\n"
        
        if len(results) > 5:
            summary += f"... and {len(results) - 5} more images."
        
        return summary, csv_filename

def create_interface():
    """Create the Gradio interface"""
    app = FramepackGeneratorPro()
    
    # Custom CSS for professional styling
    css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .api-box {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    """
    
    with gr.Blocks(css=css, title="Framepack Generator Pro") as interface:
        gr.HTML("""
        <div class="header">
            <h1>🎬 Framepack Generator Pro</h1>
            <p>AI-Powered Video Prompt Generator with Multi-Provider Support</p>
            <p>Transform your images into professional video prompts using OpenAI GPT-4 Vision, Google Gemini Vision, or local BLIP analysis</p>
        </div>
        """)
        
        with gr.Tabs():
            # Main Generation Tab
            with gr.TabItem("🎯 Generate Prompt"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="feature-box"><h3>📸 Image Upload</h3><p>Upload your image to analyze and generate video prompts</p></div>')
                        image_input = gr.Image(
                            label="Upload Image (JPG, PNG, WebP)",
                            type="pil",
                            height=300
                        )
                        
                        gr.HTML('<div class="feature-box"><h3>⚙️ Settings</h3></div>')
                        duration_slider = gr.Slider(
                            minimum=5,
                            maximum=120,
                            value=30,
                            step=5,
                            label="Video Duration (seconds)",
                            info="Affects prompt complexity and progression"
                        )
                        
                        custom_action = gr.Textbox(
                            label="Custom Action (Optional)",
                            placeholder="e.g., 'waves hello', 'starts dancing', 'looks around'",
                            info="Specific action to incorporate into the video sequence"
                        )
                        
                        output_format = gr.Radio(
                            choices=["Both", "Timestamp Only", "Hunyuan Only"],
                            value="Both",
                            label="Output Format"
                        )
                        
                        generate_btn = gr.Button(
                            "🚀 Generate Video Prompt",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column(scale=2):
                        gr.HTML('<div class="feature-box"><h3>📝 Generated Prompts</h3></div>')
                        output_display = gr.Markdown(
                            label="Generated Prompts",
                            value="Upload an image and click 'Generate Video Prompt' to see results here."
                        )
                        
                        status_display = gr.HTML()
                        
                        export_file = gr.File(
                            label="📥 Download Prompts",
                            visible=False
                        )
                
                generate_btn.click(
                    fn=app.generate_video_prompt,
                    inputs=[image_input, duration_slider, custom_action, output_format],
                    outputs=[output_display, export_file, status_display]
                ).then(
                    lambda: gr.update(visible=True),
                    outputs=[export_file]
                )
            
            # Batch Processing Tab
            with gr.TabItem("📦 Batch Processing"):
                gr.HTML('<div class="feature-box"><h3>🔄 Batch Image Processing</h3><p>Process multiple images simultaneously for efficient workflow</p></div>')
                
                with gr.Row():
                    with gr.Column():
                        batch_files = gr.File(
                            file_count="multiple",
                            file_types=["image"],
                            label="Upload Multiple Images"
                        )
                        
                        batch_btn = gr.Button(
                            "🔄 Process Batch",
                            variant="primary"
                        )
                    
                    with gr.Column():
                        batch_output = gr.Markdown(
                            label="Batch Results",
                            value="Upload multiple images and click 'Process Batch' to see results."
                        )
                        
                        batch_export = gr.File(
                            label="📥 Download Batch Results (CSV)",
                            visible=False
                        )
                
                batch_btn.click(
                    fn=app.batch_process,
                    inputs=[batch_files],
                    outputs=[batch_output, batch_export]
                ).then(
                    lambda: gr.update(visible=True),
                    outputs=[batch_export]
                )
            
            # Settings Tab
            with gr.TabItem("⚙️ Settings"):
                gr.HTML('<div class="feature-box"><h3>🛠️ Application Settings</h3></div>')
                
                with gr.Row():
                    with gr.Column():
                        # API Provider Settings
                        gr.HTML('<div class="api-box"><h4>🤖 AI Provider Settings</h4></div>')
                        
                        api_provider = gr.Radio(
                            choices=["blip", "openai", "google", "huggingface"],
                            value=app.settings["api_settings"]["provider"],
                            label="AI Analysis Provider",
                            info="Choose your preferred AI provider for image analysis"
                        )
                        
                        openai_api_key = gr.Textbox(
                            label="OpenAI API Key",
                            type="password",
                            placeholder="sk-...",
                            value=app.settings["api_settings"]["openai_api_key"],
                            info="Required for OpenAI GPT-4 Vision analysis"
                        )
                        
                        google_api_key = gr.Textbox(
                            label="Google AI Studio API Key",
                            type="password",
                            placeholder="AI...",
                            value=app.settings["api_settings"]["google_api_key"],
                            info="Get your key at: https://aistudio.google.com/apikey"
                        )
                        
                        huggingface_api_key = gr.Textbox(
                            label="Hugging Face API Key",
                            type="password",
                            placeholder="hf_...",
                            value=app.settings["api_settings"]["huggingface_api_key"],
                            info="Get your key at: https://huggingface.co/settings/tokens"
                        )
                        
                        fallback_enabled = gr.Checkbox(
                            label="Enable API Fallback",
                            value=app.settings["api_settings"]["fallback_enabled"],
                            info="Automatically try other providers if the selected one fails"
                        )
                        
                        save_api_btn = gr.Button("💾 Save API Settings", variant="primary")
                        api_status = gr.HTML()
                        
                        # General Settings
                        gr.HTML('<div class="feature-box"><h4>📊 General Settings</h4></div>')
                        
                        settings_duration = gr.Slider(
                            minimum=5,
                            maximum=120,
                            value=app.settings["generation_settings"]["default_duration"],
                            label="Default Duration (seconds)"
                        )
                        
                        settings_fps = gr.Number(
                            value=app.settings["generation_settings"]["default_fps"],
                            label="Default FPS"
                        )
                        
                        settings_model = gr.Dropdown(
                            choices=[
                                "Salesforce/blip-image-captioning-base",
                                "Salesforce/blip-image-captioning-large"
                            ],
                            value=app.settings["model_settings"]["blip_model"],
                            label="BLIP Model (Fallback)"
                        )
                        
                        debug_mode = gr.Checkbox(
                            label="Enable Debug Mode",
                            value=app.settings.get("ui_settings", {}).get("debug", False),
                            info="Show detailed analysis information in prompt output"
                        )
                        
                        save_general_btn = gr.Button("💾 Save General Settings")
                        general_status = gr.HTML()
                    
                    with gr.Column():
                        gr.HTML("""
                        <div class="api-box">
                            <h4>🔑 API Key Setup Instructions</h4>
                            
                            <h5>OpenAI API Key:</h5>
                            <ol>
                                <li>Visit <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI API Keys</a></li>
                                <li>Sign in to your OpenAI account</li>
                                <li>Click "Create new secret key"</li>
                                <li>Copy the key (starts with "sk-")</li>
                                <li>Paste it in the OpenAI API Key field above</li>
                            </ol>
                            
                            <h5>Google AI Studio API Key:</h5>
                            <ol>
                                <li>Visit <a href="https://aistudio.google.com/apikey" target="_blank">Google AI Studio</a></li>
                                <li>Sign in with your Google account</li>
                                <li>Click "Create API Key"</li>
                                <li>Copy the generated key</li>
                                <li>Paste it in the Google AI API Key field above</li>
                            </ol>
                            
                            <h5>Hugging Face API Key:</h5>
                            <ol>
                                <li>Visit <a href="https://huggingface.co/settings/tokens" target="_blank">Hugging Face Tokens</a></li>
                                <li>Sign in to your Hugging Face account</li>
                                <li>Click "New token"</li>
                                <li>Choose "Read" access and create token</li>
                                <li>Copy the token (starts with "hf_")</li>
                                <li>Paste it in the Hugging Face API Key field above</li>
                            </ol>
                            
                            <p><strong>Note:</strong> API keys are stored locally and used only for image analysis. Keep them secure!</p>
                        </div>
                        """)
                        
                        gr.HTML("""
                        <div class="feature-box">
                            <h4>📊 Application Info</h4>
                            <p><strong>Version:</strong> 1.1.0</p>
                            <p><strong>Providers:</strong> OpenAI GPT-4 Vision, Google Gemini Vision, BLIP Local</p>
                            <p><strong>Supported Formats:</strong> JPG, PNG, WebP</p>
                            <p><strong>Max Duration:</strong> 120 seconds</p>
                            <p><strong>Output Formats:</strong> Timestamp, Hunyuan</p>
                            <p><strong>Fallback:</strong> Automatic provider switching</p>
                        </div>
                        """)
                
                # API Settings Save Function
                def save_api_settings_fn(provider, openai_key, google_key, hf_key, fallback):
                    return app.update_api_settings(provider, openai_key, google_key, hf_key, fallback)
                
                save_api_btn.click(
                    fn=save_api_settings_fn,
                    inputs=[api_provider, openai_api_key, google_api_key, huggingface_api_key, fallback_enabled],
                    outputs=[api_status]
                )
                
                # General Settings Save Function
                def save_general_settings_fn(duration, fps, model, debug):
                    app.settings["generation_settings"]["default_duration"] = duration
                    app.settings["generation_settings"]["default_fps"] = fps
                    app.settings["model_settings"]["blip_model"] = model
                    app.settings["ui_settings"]["debug"] = debug
                    app.save_settings(app.settings)
                    return "✅ General settings saved successfully!"
                
                save_general_btn.click(
                    fn=save_general_settings_fn,
                    inputs=[settings_duration, settings_fps, settings_model, debug_mode],
                    outputs=[general_status]
                )
            
            # Help Tab
            with gr.TabItem("❓ Help"):
                gr.HTML("""
                <div class="feature-box">
                    <h3>🎯 How to Use Framepack Generator Pro</h3>
                    
                    <h4>1. Setup API Keys (Recommended):</h4>
                    <ul>
                        <li>Go to the "Settings" tab</li>
                        <li>Choose your preferred AI provider (OpenAI or Google AI)</li>
                        <li>Enter your API key following the setup instructions</li>
                        <li>Enable fallback for automatic provider switching</li>
                    </ul>
                    
                    <h4>2. Generate Single Prompt:</h4>
                    <ul>
                        <li>Upload an image in the "Generate Prompt" tab</li>
                        <li>Adjust duration slider (5-120 seconds)</li>
                        <li>Optionally add custom actions</li>
                        <li>Choose output format and click "Generate Video Prompt"</li>
                    </ul>
                    
                    <h4>3. Batch Processing:</h4>
                    <ul>
                        <li>Go to "Batch Processing" tab</li>
                        <li>Upload multiple images</li>
                        <li>Click "Process Batch" to generate prompts for all images</li>
                        <li>Download results as CSV file</li>
                    </ul>
                    
                    <h4>4. AI Provider Comparison:</h4>
                    <ul>
                        <li><strong>OpenAI GPT-4 Vision:</strong> Excellent detail and context understanding</li>
                        <li><strong>Google Gemini Vision:</strong> Fast processing and good multimodal reasoning</li>
                        <li><strong>Hugging Face BLIP:</strong> Cloud-based BLIP model with better accuracy than local</li>
                        <li><strong>BLIP Local:</strong> Free, works offline, basic but reliable descriptions</li>
                    </ul>
                    
                    <h4>5. Output Formats:</h4>
                    <ul>
                        <li><strong>Timestamp Format:</strong> [1s: action] [3s: action] format for precise timing</li>
                        <li><strong>Hunyuan Format:</strong> Detailed narrative descriptions for fluid motion</li>
                    </ul>
                    
                    <h4>6. Tips for Best Results:</h4>
                    <ul>
                        <li>Use high-quality, well-lit images</li>
                        <li>Clear subject focus works best</li>
                        <li>API providers give more detailed and creative descriptions</li>
                        <li>Longer durations create more complex sequences</li>
                        <li>Custom actions help personalize the video flow</li>
                        <li>Enable fallback to ensure analysis always succeeds</li>
                    </ul>
                    
                    <h4>7. Troubleshooting:</h4>
                    <ul>
                        <li>If API analysis fails, check your API keys in Settings</li>
                        <li>Fallback will automatically use BLIP if APIs are unavailable</li>
                        <li>Large images may take longer to process</li>
                        <li>Check the analysis provider shown in results</li>
                    </ul>
                </div>
                """)
    
    return interface

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("generated_prompts", exist_ok=True)
    os.makedirs("history", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    
    # Launch the application
    interface = create_interface()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7861,
        share=False,
        show_error=True
    )

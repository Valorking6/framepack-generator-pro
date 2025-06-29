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
        self.image_analyzer = ImageAnalyzer()
        self.prompt_generator = PromptGenerator()
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Load application settings"""
        default_settings = {
            "default_duration": 30,
            "default_fps": 30,
            "model_name": "Salesforce/blip-image-captioning-base",
            "output_format": "both"
        }
        
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    return {**default_settings, **settings}
            except:
                pass
        return default_settings
    
    def save_settings(self, settings):
        """Save application settings"""
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=2)
    
    def generate_video_prompt(self, image, duration, custom_action, output_format):
        """Main function to generate video prompts from uploaded image"""
        if image is None:
            return "Please upload an image first.", "", None
        
        try:
            # Analyze the uploaded image
            analysis = self.image_analyzer.analyze_image(image)
            
            # Generate prompts based on analysis
            timestamp_prompt, hunyuan_prompt = self.prompt_generator.generate_prompts(
                analysis, duration, custom_action
            )
            
            # Format output based on user preference
            if output_format == "Timestamp Only":
                display_output = f"**Timestamp Format:**\n{timestamp_prompt}"
                export_data = {"timestamp": timestamp_prompt, "hunyuan": ""}
            elif output_format == "Hunyuan Only":
                display_output = f"**Hunyuan Format:**\n{hunyuan_prompt}"
                export_data = {"timestamp": "", "hunyuan": hunyuan_prompt}
            else:  # Both
                display_output = f"**Timestamp Format:**\n{timestamp_prompt}\n\n**Hunyuan Format:**\n{hunyuan_prompt}"
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
            "generator": "Framepack Generator Pro v1.0"
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
                    "timestamp_prompt": timestamp_prompt,
                    "hunyuan_prompt": hunyuan_prompt
                })
            except Exception as e:
                results.append({
                    "filename": os.path.basename(file_obj.name),
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
            summary += f"**{result['filename']}:**\n{result['timestamp_prompt'][:100]}...\n\n"
        
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
            <p>AI-Powered Video Prompt Generator for Hunyuan Video Creation</p>
            <p>Transform your images into professional video prompts with precise timing and dynamic camera work</p>
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
                        settings_duration = gr.Slider(
                            minimum=5,
                            maximum=120,
                            value=app.settings["default_duration"],
                            label="Default Duration (seconds)"
                        )
                        
                        settings_fps = gr.Number(
                            value=app.settings["default_fps"],
                            label="Default FPS"
                        )
                        
                        settings_model = gr.Dropdown(
                            choices=[
                                "Salesforce/blip-image-captioning-base",
                                "Salesforce/blip-image-captioning-large"
                            ],
                            value=app.settings["model_name"],
                            label="BLIP Model"
                        )
                        
                        save_settings_btn = gr.Button("💾 Save Settings")
                    
                    with gr.Column():
                        gr.HTML("""
                        <div class="feature-box">
                            <h4>📊 Application Info</h4>
                            <p><strong>Version:</strong> 1.0.0</p>
                            <p><strong>Model:</strong> BLIP + Custom Analysis</p>
                            <p><strong>Supported Formats:</strong> JPG, PNG, WebP</p>
                            <p><strong>Max Duration:</strong> 120 seconds</p>
                            <p><strong>Output Formats:</strong> Timestamp, Hunyuan</p>
                        </div>
                        """)
                
                def save_settings_fn(duration, fps, model):
                    new_settings = {
                        "default_duration": duration,
                        "default_fps": fps,
                        "model_name": model,
                        "output_format": "both"
                    }
                    app.save_settings(new_settings)
                    app.settings = new_settings
                    return "✅ Settings saved successfully!"
                
                save_settings_btn.click(
                    fn=save_settings_fn,
                    inputs=[settings_duration, settings_fps, settings_model],
                    outputs=[gr.HTML()]
                )
            
            # Help Tab
            with gr.TabItem("❓ Help"):
                gr.HTML("""
                <div class="feature-box">
                    <h3>🎯 How to Use Framepack Generator Pro</h3>
                    
                    <h4>1. Generate Single Prompt:</h4>
                    <ul>
                        <li>Upload an image in the "Generate Prompt" tab</li>
                        <li>Adjust duration slider (5-120 seconds)</li>
                        <li>Optionally add custom actions</li>
                        <li>Choose output format and click "Generate Video Prompt"</li>
                    </ul>
                    
                    <h4>2. Batch Processing:</h4>
                    <ul>
                        <li>Go to "Batch Processing" tab</li>
                        <li>Upload multiple images</li>
                        <li>Click "Process Batch" to generate prompts for all images</li>
                        <li>Download results as CSV file</li>
                    </ul>
                    
                    <h4>3. Output Formats:</h4>
                    <ul>
                        <li><strong>Timestamp Format:</strong> [1s: action] [3s: action] format for precise timing</li>
                        <li><strong>Hunyuan Format:</strong> Detailed narrative descriptions for fluid motion</li>
                    </ul>
                    
                    <h4>4. Tips for Best Results:</h4>
                    <ul>
                        <li>Use high-quality, well-lit images</li>
                        <li>Clear subject focus works best</li>
                        <li>Longer durations create more complex sequences</li>
                        <li>Custom actions help personalize the video flow</li>
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
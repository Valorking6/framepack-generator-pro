
import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
import shutil

class FileManager:
    """Utility class for file operations"""
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """Ensure directory exists, create if it doesn't"""
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def save_json(data: Dict, filepath: str) -> bool:
        """Save data as JSON file"""
        try:
            FileManager.ensure_directory(os.path.dirname(filepath))
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON file {filepath}: {e}")
            return False
    
    @staticmethod
    def load_json(filepath: str) -> Dict:
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON file {filepath}: {e}")
            return {}
    
    @staticmethod
    def save_csv(data: List[Dict], filepath: str) -> bool:
        """Save data as CSV file"""
        try:
            if not data:
                return False
            
            FileManager.ensure_directory(os.path.dirname(filepath))
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error saving CSV file {filepath}: {e}")
            return False
    
    @staticmethod
    def get_timestamp_filename(prefix: str, extension: str) -> str:
        """Generate timestamped filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    
    @staticmethod
    def cleanup_old_files(directory: str, max_files: int = 50) -> None:
        """Clean up old files, keeping only the most recent ones"""
        try:
            if not os.path.exists(directory):
                return
            
            files = []
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    files.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove old files
            for filepath, _ in files[max_files:]:
                try:
                    os.remove(filepath)
                    print(f"Removed old file: {filepath}")
                except Exception as e:
                    print(f"Error removing file {filepath}: {e}")
                    
        except Exception as e:
            print(f"Error cleaning up directory {directory}: {e}")

class ConfigManager:
    """Configuration management utility"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = {
            "model_settings": {
                "blip_model": "Salesforce/blip-image-captioning-base",
                "device": "auto",
                "max_length": 50
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
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_configs(self.default_config, config)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return self.default_config.copy()
    
    def save_config(self, config: Dict) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result

class PromptExporter:
    """Utility for exporting prompts in various formats"""
    
    @staticmethod
    def export_to_txt(prompt_data: Dict, filepath: str) -> bool:
        """Export prompt to text file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("FRAMEPACK GENERATOR PRO - EXPORTED PROMPT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if prompt_data.get('timestamp_prompt'):
                    f.write("TIMESTAMP FORMAT:\n")
                    f.write("-" * 20 + "\n")
                    f.write(prompt_data['timestamp_prompt'] + "\n\n")
                
                if prompt_data.get('hunyuan_prompt'):
                    f.write("HUNYUAN FORMAT:\n")
                    f.write("-" * 20 + "\n")
                    f.write(prompt_data['hunyuan_prompt'] + "\n\n")
                
                if prompt_data.get('analysis'):
                    f.write("IMAGE ANALYSIS:\n")
                    f.write("-" * 20 + "\n")
                    f.write(json.dumps(prompt_data['analysis'], indent=2) + "\n")
            
            return True
        except Exception as e:
            print(f"Error exporting to TXT: {e}")
            return False
    
    @staticmethod
    def export_to_json(prompt_data: Dict, filepath: str) -> bool:
        """Export prompt to JSON file"""
        try:
            export_data = {
                "metadata": {
                    "generator": "Framepack Generator Pro",
                    "version": "1.0.0",
                    "exported": datetime.now().isoformat()
                },
                "prompts": prompt_data
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    @staticmethod
    def export_batch_to_csv(batch_data: List[Dict], filepath: str) -> bool:
        """Export batch results to CSV"""
        try:
            if not batch_data:
                return False
            
            # Flatten the data for CSV export
            csv_data = []
            for item in batch_data:
                csv_row = {
                    "filename": item.get("filename", ""),
                    "timestamp_prompt": item.get("timestamp_prompt", ""),
                    "hunyuan_prompt": item.get("hunyuan_prompt", ""),
                    "generated_at": datetime.now().isoformat()
                }
                csv_data.append(csv_row)
            
            return FileManager.save_csv(csv_data, filepath)
        except Exception as e:
            print(f"Error exporting batch to CSV: {e}")
            return False

class ValidationUtils:
    """Utility functions for validation"""
    
    @staticmethod
    def validate_image_file(filepath: str) -> bool:
        """Validate if file is a supported image format"""
        if not os.path.exists(filepath):
            return False
        
        supported_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}
        _, ext = os.path.splitext(filepath.lower())
        return ext in supported_extensions
    
    @staticmethod
    def validate_duration(duration: int) -> bool:
        """Validate video duration"""
        return 5 <= duration <= 120
    
    @staticmethod
    def validate_prompt_length(prompt: str, max_length: int = 1000) -> bool:
        """Validate prompt length"""
        return len(prompt) <= max_length
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        import re
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing spaces and dots
        filename = filename.strip(' .')
        # Ensure it's not empty
        if not filename:
            filename = "untitled"
        return filename

class PerformanceMonitor:
    """Monitor application performance"""
    
    def __init__(self):
        self.start_time = None
        self.metrics = {}
    
    def start_timer(self, operation: str) -> None:
        """Start timing an operation"""
        self.start_time = datetime.now()
        self.metrics[operation] = {"start": self.start_time}
    
    def end_timer(self, operation: str) -> float:
        """End timing and return duration"""
        if operation in self.metrics and self.start_time:
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            self.metrics[operation]["end"] = end_time
            self.metrics[operation]["duration"] = duration
            return duration
        return 0.0
    
    def get_metrics(self) -> Dict:
        """Get performance metrics"""
        return self.metrics.copy()
    
    def log_metrics(self, filepath: str = "performance.log") -> None:
        """Log metrics to file"""
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().isoformat()
                f.write(f"\n[{timestamp}] Performance Metrics:\n")
                for operation, data in self.metrics.items():
                    duration = data.get("duration", 0)
                    f.write(f"  {operation}: {duration:.2f}s\n")
        except Exception as e:
            print(f"Error logging metrics: {e}")

# Global instances for easy access
file_manager = FileManager()
config_manager = ConfigManager()
performance_monitor = PerformanceMonitor()

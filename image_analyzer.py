
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
from PIL import Image
import cv2
import numpy as np
import json
import base64
import io
from typing import Dict, List, Tuple, Optional
import os

# Import API clients
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class ImageAnalyzer:
    def __init__(self, settings: Dict = None):
        """Initialize the image analyzer with BLIP and API models"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.settings = settings or {}
        print(f"Using device: {self.device}")
        
        # Load BLIP model for image captioning (fallback)
        try:
            self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            self.blip_model.to(self.device)
            print("✅ BLIP model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading BLIP model: {e}")
            self.blip_processor = None
            self.blip_model = None
        
        # Initialize API clients
        self._init_api_clients()
    
    def _init_api_clients(self):
        """Initialize OpenAI, Google AI, and Hugging Face clients"""
        api_settings = self.settings.get("api_settings", {})
        
        # Initialize OpenAI client
        self.openai_client = None
        if OPENAI_AVAILABLE and api_settings.get("openai_api_key"):
            try:
                self.openai_client = OpenAI(api_key=api_settings["openai_api_key"])
                print("✅ OpenAI client initialized")
            except Exception as e:
                print(f"❌ Error initializing OpenAI client: {e}")
        
        # Initialize Google AI client
        self.google_client = None
        if GOOGLE_AI_AVAILABLE and api_settings.get("google_api_key"):
            try:
                genai.configure(api_key=api_settings["google_api_key"])
                self.google_client = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Google AI client initialized")
            except Exception as e:
                print(f"❌ Error initializing Google AI client: {e}")
        
        # Initialize Hugging Face client
        self.huggingface_api_key = api_settings.get("huggingface_api_key")
        if self.huggingface_api_key and REQUESTS_AVAILABLE:
            print("✅ Hugging Face API key configured")
        elif api_settings.get("huggingface_api_key"):
            print("❌ Requests library not available for Hugging Face API")
    
    def update_settings(self, settings: Dict):
        """Update settings and reinitialize API clients"""
        self.settings = settings
        self._init_api_clients()
    
    def analyze_image(self, image: Image.Image) -> Dict:
        """
        Comprehensive image analysis using selected API provider with fallback
        """
        if image is None:
            raise ValueError("No image provided for analysis")
        
        # Convert PIL image to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        analysis = {
            "basic_description": "",
            "scene_details": {},
            "subject_analysis": {},
            "lighting_analysis": {},
            "composition_analysis": {},
            "color_analysis": {},
            "technical_details": {},
            "analysis_provider": "unknown"
        }
        
        try:
            # Get provider preference
            provider = self.settings.get("api_settings", {}).get("provider", "blip")
            
            # Try selected provider first
            if provider == "openai" and self.openai_client:
                analysis = self._analyze_with_openai(image, analysis)
            elif provider == "google" and self.google_client:
                analysis = self._analyze_with_google(image, analysis)
            elif provider == "huggingface" and self.huggingface_api_key:
                analysis = self._analyze_with_huggingface(image, analysis)
            elif provider == "blip":
                # Use local BLIP model directly
                analysis["basic_description"] = self._get_basic_description(image)
                analysis["analysis_provider"] = "blip_local"
                print("✅ Using BLIP local analysis")
            else:
                # Fallback to BLIP or try other providers
                analysis = self._analyze_with_fallback(image, analysis, provider)
            
            # Always add technical analysis and other computer vision features
            analysis["scene_details"] = self._analyze_scene(image)
            analysis["subject_analysis"] = self._analyze_subject(image)
            analysis["lighting_analysis"] = self._analyze_lighting(image)
            analysis["composition_analysis"] = self._analyze_composition(image)
            analysis["color_analysis"] = self._analyze_colors(image)
            analysis["technical_details"] = self._get_technical_details(image)
            
        except Exception as e:
            print(f"Error in image analysis: {e}")
            analysis["basic_description"] = "A scene with various elements"
            analysis["scene_details"] = {"setting": "unknown", "environment": "indoor"}
            analysis["analysis_provider"] = "error_fallback"
        
        return analysis
    
    def _analyze_with_openai(self, image: Image.Image, analysis: Dict) -> Dict:
        """Analyze image using OpenAI GPT-4 Vision"""
        try:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this image in detail. Provide a comprehensive description including:
                                1. Basic scene description
                                2. Main subjects and their positions
                                3. Lighting conditions and mood
                                4. Composition and framing
                                5. Colors and visual style
                                6. Any notable activities or expressions
                                
                                Format your response as a detailed paragraph."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_str}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            description = response.choices[0].message.content
            analysis["basic_description"] = description
            analysis["analysis_provider"] = "openai_gpt4o_mini"
            print("✅ OpenAI GPT-4o Mini Vision analysis completed")
            
        except Exception as e:
            print(f"❌ OpenAI analysis failed: {e}")
            raise e
        
        return analysis
    
    def _analyze_with_google(self, image: Image.Image, analysis: Dict) -> Dict:
        """Analyze image using Google Gemini Vision"""
        try:
            prompt = """Analyze this image in detail. Provide a comprehensive description including:
            1. Basic scene description
            2. Main subjects and their positions  
            3. Lighting conditions and mood
            4. Composition and framing
            5. Colors and visual style
            6. Any notable activities or expressions
            
            Format your response as a detailed paragraph."""
            
            response = self.google_client.generate_content([prompt, image])
            
            description = response.text
            analysis["basic_description"] = description
            analysis["analysis_provider"] = "google_gemini_vision"
            print("✅ Google Gemini Vision analysis completed")
            
        except Exception as e:
            print(f"❌ Google AI analysis failed: {e}")
            raise e
        
        return analysis
    
    def _analyze_with_huggingface(self, image: Image.Image, analysis: Dict) -> Dict:
        """Analyze image using Hugging Face API"""
        try:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()
            
            # Use the more reliable BLIP base model endpoint
            API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
            headers = {
                "Authorization": f"Bearer {self.huggingface_api_key}",
                "Content-Type": "application/octet-stream",
                "x-wait-for-model": "true"  # Wait for model to load if cold
            }
            
            # Send image data as binary
            response = requests.post(API_URL, headers=headers, data=img_bytes)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    description = result[0].get("generated_text", "A scene with various elements")
                elif isinstance(result, dict) and "generated_text" in result:
                    description = result["generated_text"]
                else:
                    description = "A scene with various elements"
                
                analysis["basic_description"] = description
                analysis["analysis_provider"] = "huggingface_blip_base"
                print("✅ Hugging Face BLIP analysis completed")
            elif response.status_code == 503:
                print("❌ Hugging Face model is loading, retrying...")
                # Wait a moment and try again
                import time
                time.sleep(2)
                response = requests.post(API_URL, headers=headers, data=img_bytes)
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        description = result[0].get("generated_text", "A scene with various elements")
                    else:
                        description = "A scene with various elements"
                    analysis["basic_description"] = description
                    analysis["analysis_provider"] = "huggingface_blip_base"
                    print("✅ Hugging Face BLIP analysis completed after retry")
                else:
                    raise Exception(f"API returned status code {response.status_code} after retry")
            else:
                print(f"❌ Hugging Face API error: {response.status_code}")
                print(f"Response: {response.text}")
                raise Exception(f"API returned status code {response.status_code}")
            
        except Exception as e:
            print(f"❌ Hugging Face analysis failed: {e}")
            raise e
        
        return analysis
    
    def _analyze_with_fallback(self, image: Image.Image, analysis: Dict, preferred_provider: str) -> Dict:
        """Try fallback providers or BLIP if APIs fail"""
        fallback_enabled = self.settings.get("api_settings", {}).get("fallback_enabled", True)
        
        if fallback_enabled:
            # Try other API providers first
            if preferred_provider != "openai" and self.openai_client:
                try:
                    return self._analyze_with_openai(image, analysis)
                except Exception as e:
                    print(f"OpenAI fallback failed: {e}")
            
            if preferred_provider != "google" and self.google_client:
                try:
                    return self._analyze_with_google(image, analysis)
                except Exception as e:
                    print(f"Google AI fallback failed: {e}")
            
            if preferred_provider != "huggingface" and self.huggingface_api_key:
                try:
                    return self._analyze_with_huggingface(image, analysis)
                except Exception as e:
                    print(f"Hugging Face fallback failed: {e}")
        
        # Final fallback to BLIP
        analysis["basic_description"] = self._get_basic_description(image)
        analysis["analysis_provider"] = "blip_local"
        print("✅ Using BLIP local analysis as fallback")
        
        return analysis
    
    def _get_basic_description(self, image: Image.Image) -> str:
        """Generate basic description using BLIP model"""
        if self.blip_model is None or self.blip_processor is None:
            return "A person in a scene"
        
        try:
            inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
            out = self.blip_model.generate(**inputs, max_length=50)
            description = self.blip_processor.decode(out[0], skip_special_tokens=True)
            return description
        except Exception as e:
            print(f"Error generating basic description: {e}")
            return "A person in a scene"
    
    def _analyze_scene(self, image: Image.Image) -> Dict:
        """Analyze scene setting and environment"""
        # Convert to numpy array for OpenCV processing
        img_array = np.array(image)
        
        # Basic scene classification based on colors and features
        scene_analysis = {
            "setting": "unknown",
            "environment": "indoor",
            "background_type": "neutral",
            "depth": "medium",
            "complexity": "moderate"
        }
        
        try:
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Analyze dominant colors to infer setting
            dominant_colors = self._get_dominant_colors(img_array)
            
            # Determine environment based on color patterns
            green_ratio = np.sum((hsv[:,:,1] > 50) & (hsv[:,:,0] > 35) & (hsv[:,:,0] < 85)) / (hsv.shape[0] * hsv.shape[1])
            blue_ratio = np.sum((hsv[:,:,1] > 50) & (hsv[:,:,0] > 100) & (hsv[:,:,0] < 130)) / (hsv.shape[0] * hsv.shape[1])
            
            if green_ratio > 0.3:
                scene_analysis["environment"] = "outdoor"
                scene_analysis["setting"] = "garden" if green_ratio > 0.5 else "park"
            elif blue_ratio > 0.2:
                scene_analysis["environment"] = "outdoor"
                scene_analysis["setting"] = "sky" if blue_ratio > 0.4 else "water"
            else:
                scene_analysis["environment"] = "indoor"
                scene_analysis["setting"] = "room"
            
            # Analyze background complexity
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            if edge_density > 0.1:
                scene_analysis["complexity"] = "complex"
                scene_analysis["background_type"] = "detailed"
            elif edge_density > 0.05:
                scene_analysis["complexity"] = "moderate"
                scene_analysis["background_type"] = "textured"
            else:
                scene_analysis["complexity"] = "simple"
                scene_analysis["background_type"] = "clean"
                
        except Exception as e:
            print(f"Error in scene analysis: {e}")
        
        return scene_analysis
    
    def _analyze_subject(self, image: Image.Image) -> Dict:
        """Analyze the main subject in the image"""
        img_array = np.array(image)
        
        subject_analysis = {
            "position": "center",
            "size": "medium",
            "pose": "standing",
            "clothing": "casual",
            "expression": "neutral",
            "activity": "static"
        }
        
        try:
            # Simple subject position analysis based on center of mass
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Find contours to identify main subject
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find largest contour (likely the main subject)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get bounding box
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Determine position
                center_x = x + w // 2
                center_y = y + h // 2
                img_center_x = img_array.shape[1] // 2
                img_center_y = img_array.shape[0] // 2
                
                if abs(center_x - img_center_x) < img_array.shape[1] * 0.2:
                    subject_analysis["position"] = "center"
                elif center_x < img_center_x:
                    subject_analysis["position"] = "left"
                else:
                    subject_analysis["position"] = "right"
                
                # Determine size
                subject_area = w * h
                total_area = img_array.shape[0] * img_array.shape[1]
                size_ratio = subject_area / total_area
                
                if size_ratio > 0.4:
                    subject_analysis["size"] = "large"
                elif size_ratio > 0.2:
                    subject_analysis["size"] = "medium"
                else:
                    subject_analysis["size"] = "small"
                
                # Analyze aspect ratio for pose estimation
                aspect_ratio = h / w if w > 0 else 1
                if aspect_ratio > 1.5:
                    subject_analysis["pose"] = "standing"
                elif aspect_ratio < 0.8:
                    subject_analysis["pose"] = "sitting"
                else:
                    subject_analysis["pose"] = "neutral"
            
            # Analyze clothing colors
            clothing_colors = self._analyze_clothing_colors(img_array)
            subject_analysis["clothing"] = clothing_colors
            
        except Exception as e:
            print(f"Error in subject analysis: {e}")
        
        return subject_analysis
    
    def _analyze_lighting(self, image: Image.Image) -> Dict:
        """Analyze lighting conditions in the image"""
        img_array = np.array(image)
        
        lighting_analysis = {
            "brightness": "medium",
            "contrast": "normal",
            "direction": "front",
            "quality": "soft",
            "color_temperature": "neutral",
            "shadows": "minimal"
        }
        
        try:
            # Convert to different color spaces for analysis
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Brightness analysis
            mean_brightness = np.mean(gray)
            if mean_brightness > 180:
                lighting_analysis["brightness"] = "bright"
            elif mean_brightness > 120:
                lighting_analysis["brightness"] = "medium"
            else:
                lighting_analysis["brightness"] = "dim"
            
            # Contrast analysis
            contrast = np.std(gray)
            if contrast > 60:
                lighting_analysis["contrast"] = "high"
            elif contrast > 30:
                lighting_analysis["contrast"] = "normal"
            else:
                lighting_analysis["contrast"] = "low"
            
            # Color temperature analysis
            avg_r = np.mean(img_array[:,:,0])
            avg_b = np.mean(img_array[:,:,2])
            
            if avg_r > avg_b + 20:
                lighting_analysis["color_temperature"] = "warm"
            elif avg_b > avg_r + 20:
                lighting_analysis["color_temperature"] = "cool"
            else:
                lighting_analysis["color_temperature"] = "neutral"
            
            # Shadow analysis
            dark_pixels = np.sum(gray < 50) / (gray.shape[0] * gray.shape[1])
            if dark_pixels > 0.3:
                lighting_analysis["shadows"] = "strong"
            elif dark_pixels > 0.1:
                lighting_analysis["shadows"] = "moderate"
            else:
                lighting_analysis["shadows"] = "minimal"
                
        except Exception as e:
            print(f"Error in lighting analysis: {e}")
        
        return lighting_analysis
    
    def _analyze_composition(self, image: Image.Image) -> Dict:
        """Analyze image composition and framing"""
        img_array = np.array(image)
        
        composition = {
            "framing": "medium_shot",
            "rule_of_thirds": False,
            "symmetry": "none",
            "leading_lines": False,
            "depth_of_field": "normal"
        }
        
        try:
            height, width = img_array.shape[:2]
            
            # Analyze framing based on subject size and position
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # Find main subject area
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                subject_height_ratio = h / height
                
                if subject_height_ratio > 0.8:
                    composition["framing"] = "close_up"
                elif subject_height_ratio > 0.5:
                    composition["framing"] = "medium_shot"
                elif subject_height_ratio > 0.3:
                    composition["framing"] = "medium_wide"
                else:
                    composition["framing"] = "wide_shot"
            
            # Check rule of thirds
            third_x = width // 3
            third_y = height // 3
            
            # Simple rule of thirds check based on edge density
            roi_edges = [
                edges[third_y:2*third_y, 0:third_x],
                edges[third_y:2*third_y, third_x:2*third_x],
                edges[third_y:2*third_y, 2*third_x:width],
                edges[0:third_y, third_x:2*third_x],
                edges[2*third_y:height, third_x:2*third_x]
            ]
            
            edge_densities = [np.sum(roi > 0) / (roi.shape[0] * roi.shape[1]) for roi in roi_edges]
            max_density = max(edge_densities)
            
            if max_density > 0.1:
                composition["rule_of_thirds"] = True
            
        except Exception as e:
            print(f"Error in composition analysis: {e}")
        
        return composition
    
    def _analyze_colors(self, image: Image.Image) -> Dict:
        """Analyze color palette and distribution"""
        img_array = np.array(image)
        
        color_analysis = {
            "dominant_colors": [],
            "color_harmony": "complementary",
            "saturation": "medium",
            "color_mood": "neutral"
        }
        
        try:
            # Get dominant colors
            dominant_colors = self._get_dominant_colors(img_array)
            color_analysis["dominant_colors"] = dominant_colors
            
            # Analyze saturation
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            avg_saturation = np.mean(hsv[:,:,1])
            
            if avg_saturation > 150:
                color_analysis["saturation"] = "high"
            elif avg_saturation > 80:
                color_analysis["saturation"] = "medium"
            else:
                color_analysis["saturation"] = "low"
            
            # Determine color mood
            if "red" in dominant_colors or "orange" in dominant_colors:
                color_analysis["color_mood"] = "warm"
            elif "blue" in dominant_colors or "cyan" in dominant_colors:
                color_analysis["color_mood"] = "cool"
            elif "green" in dominant_colors:
                color_analysis["color_mood"] = "natural"
            else:
                color_analysis["color_mood"] = "neutral"
                
        except Exception as e:
            print(f"Error in color analysis: {e}")
        
        return color_analysis
    
    def _get_dominant_colors(self, img_array: np.ndarray, k: int = 5) -> List[str]:
        """Extract dominant colors from image"""
        try:
            # Reshape image to be a list of pixels
            pixels = img_array.reshape(-1, 3)
            
            # Use k-means clustering to find dominant colors
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = kmeans.cluster_centers_
            
            # Convert to color names
            color_names = []
            for color in colors:
                color_name = self._rgb_to_color_name(color)
                if color_name not in color_names:
                    color_names.append(color_name)
            
            return color_names[:3]  # Return top 3 colors
            
        except ImportError:
            # Fallback if sklearn is not available
            return ["red", "blue", "green"]
        except Exception as e:
            print(f"Error extracting dominant colors: {e}")
            return ["neutral"]
    
    def _rgb_to_color_name(self, rgb: np.ndarray) -> str:
        """Convert RGB values to color name"""
        r, g, b = rgb
        
        # Simple color classification
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r > g and r > b:
            if r > 150:
                return "red"
            else:
                return "brown"
        elif g > r and g > b:
            return "green"
        elif b > r and b > g:
            return "blue"
        elif r > 150 and g > 150:
            return "yellow"
        elif r > 150 and b > 150:
            return "magenta"
        elif g > 150 and b > 150:
            return "cyan"
        else:
            return "gray"
    
    def _analyze_clothing_colors(self, img_array: np.ndarray) -> str:
        """Analyze clothing colors in the image"""
        try:
            # Focus on the middle portion of the image where clothing is likely
            height, width = img_array.shape[:2]
            clothing_region = img_array[height//4:3*height//4, width//4:3*width//4]
            
            dominant_colors = self._get_dominant_colors(clothing_region, k=3)
            
            if dominant_colors:
                return f"{dominant_colors[0]} clothing"
            else:
                return "casual clothing"
                
        except Exception as e:
            print(f"Error analyzing clothing colors: {e}")
            return "casual clothing"
    
    def _get_technical_details(self, image: Image.Image) -> Dict:
        """Get technical details about the image"""
        return {
            "width": image.width,
            "height": image.height,
            "aspect_ratio": round(image.width / image.height, 2),
            "format": image.format or "Unknown",
            "mode": image.mode
        }

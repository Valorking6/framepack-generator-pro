
import random
import json
from typing import Dict, List, Tuple
from datetime import datetime

class PromptGenerator:
    def __init__(self):
        """Initialize the prompt generator with templates and motion patterns"""
        self.camera_angles = [
            "wide shot", "medium shot", "close-up", "extreme close-up",
            "aerial shot", "low angle", "high angle", "eye level",
            "bird's eye view", "worm's eye view", "over-the-shoulder"
        ]
        
        self.camera_movements = [
            "dolly in", "dolly out", "pan left", "pan right",
            "tilt up", "tilt down", "zoom in", "zoom out",
            "tracking shot", "crane up", "crane down", "orbit around"
        ]
        
        self.camera_effects = [
            "shallow depth of field", "deep focus", "motion blur",
            "focus pull", "speed ramping", "rack focus",
            "bokeh effect", "lens flare", "vignette"
        ]
        
        self.action_durations = {
            "wave": 2,
            "nod": 1,
            "smile": 1,
            "walk": 3,
            "turn": 2,
            "look": 1,
            "gesture": 2,
            "dance": 4,
            "jump": 1,
            "sit": 2,
            "stand": 2,
            "reach": 2,
            "point": 1,
            "clap": 2,
            "laugh": 2
        }
    
    def generate_prompts(self, analysis: Dict, duration: int, custom_action: str = "") -> Tuple[str, str]:
        """
        Generate both timestamp and Hunyuan format prompts based on image analysis
        """
        # Create the sequence plan
        sequence_plan = self._create_sequence_plan(analysis, duration, custom_action)
        
        # Generate timestamp format
        timestamp_prompt = self._generate_timestamp_format(sequence_plan)
        
        # Generate Hunyuan format
        hunyuan_prompt = self._generate_hunyuan_format(sequence_plan, analysis)
        
        return timestamp_prompt, hunyuan_prompt
    
    def _create_sequence_plan(self, analysis: Dict, duration: int, custom_action: str) -> List[Dict]:
        """Create a detailed sequence plan for the video"""
        sequence = []
        current_time = 0
        
        # Extract key information from analysis
        scene = analysis.get("scene_details", {})
        subject = analysis.get("subject_analysis", {})
        lighting = analysis.get("lighting_analysis", {})
        composition = analysis.get("composition_analysis", {})
        colors = analysis.get("color_analysis", {})
        basic_desc = analysis.get("basic_description", "")
        
        # Use basic description to inform scene understanding
        scene_context = self._extract_scene_context(basic_desc, scene)
        subject_context = self._extract_subject_context(basic_desc, subject)
        
        # Opening shot (0-2 seconds)
        opening_shot = {
            "start_time": 0,
            "duration": 2,
            "camera_angle": self._select_opening_shot(composition),
            "camera_movement": "static",
            "subject_action": "static pose",
            "description": f"Establishing shot revealing {subject_context} in {scene_context}",
            "effects": self._select_effects_for_mood(lighting),
            "scene_context": scene_context,
            "subject_context": subject_context
        }
        sequence.append(opening_shot)
        current_time = 2
        
        # Add custom action if provided
        if custom_action.strip():
            action_duration = self._estimate_action_duration(custom_action)
            custom_shot = {
                "start_time": current_time,
                "duration": action_duration,
                "camera_angle": self._select_action_shot(),
                "camera_movement": self._select_movement_for_action(custom_action),
                "subject_action": custom_action,
                "description": f"Subject {custom_action} with {self._get_movement_description()}",
                "effects": self._select_action_effects()
            }
            sequence.append(custom_shot)
            current_time += action_duration
        
        # Fill remaining time with dynamic shots
        while current_time < duration - 2:
            remaining_time = duration - current_time
            shot_duration = min(random.randint(2, 4), remaining_time)
            
            shot = {
                "start_time": current_time,
                "duration": shot_duration,
                "camera_angle": random.choice(self.camera_angles),
                "camera_movement": random.choice(self.camera_movements),
                "subject_action": self._generate_natural_action(subject),
                "description": self._generate_shot_description(scene, subject, lighting),
                "effects": random.choice(self.camera_effects) if random.random() > 0.5 else None
            }
            sequence.append(shot)
            current_time += shot_duration
        
        # Closing shot
        if current_time < duration:
            closing_shot = {
                "start_time": current_time,
                "duration": duration - current_time,
                "camera_angle": "wide shot",
                "camera_movement": "slow zoom out",
                "subject_action": "final pose",
                "description": f"Final wide shot capturing the complete {scene.get('setting', 'scene')}",
                "effects": "shallow depth of field"
            }
            sequence.append(closing_shot)
        
        return sequence
    
    def _generate_timestamp_format(self, sequence_plan: List[Dict]) -> str:
        """Generate timestamp format prompt: [1s: description] [3s: description]"""
        timestamp_parts = []
        
        for shot in sequence_plan:
            start_time = shot["start_time"]
            
            # Create description
            description_parts = []
            
            # Camera setup
            if shot["camera_movement"] != "static":
                description_parts.append(f"{shot['camera_movement']} to {shot['camera_angle']}")
            else:
                description_parts.append(shot["camera_angle"])
            
            # Subject action
            if shot["subject_action"] != "static pose":
                description_parts.append(f"as subject {shot['subject_action']}")
            
            # Effects
            if shot.get("effects"):
                description_parts.append(f"with {shot['effects']}")
            
            # Additional description
            if shot.get("description"):
                description_parts.append(shot["description"])
            
            full_description = ", ".join(description_parts)
            timestamp_parts.append(f"[{start_time}s: {full_description}]")
        
        return "; ".join(timestamp_parts)
    
    def _generate_hunyuan_format(self, sequence_plan: List[Dict], analysis: Dict) -> str:
        """Generate detailed Hunyuan format with fluid motion descriptions"""
        scene = analysis.get("scene_details", {})
        subject = analysis.get("subject_analysis", {})
        lighting = analysis.get("lighting_analysis", {})
        colors = analysis.get("color_analysis", {})
        
        # Build narrative description
        narrative_parts = []
        
        # Opening description
        setting_desc = self._get_detailed_setting_description(scene, lighting, colors)
        subject_desc = self._get_detailed_subject_description(subject)
        
        narrative_parts.append(f"The camera opens with {setting_desc}. {subject_desc} stands gracefully in the frame.")
        
        # Add sequence descriptions
        for i, shot in enumerate(sequence_plan[1:], 1):  # Skip first shot as it's covered above
            transition = self._get_transition_description(sequence_plan[i-1], shot)
            action_desc = self._get_fluid_action_description(shot)
            
            narrative_parts.append(f"{transition} {action_desc}")
        
        # Add environmental details
        if scene.get("environment") == "outdoor":
            narrative_parts.append("Natural lighting enhances the organic movement and creates dynamic shadows.")
        else:
            narrative_parts.append("The controlled lighting emphasizes the subject's expressions and movements.")
        
        # Add motion flow description
        narrative_parts.append("The sequence flows with natural rhythm, each movement building upon the previous, creating a cohesive visual narrative that captures both the subject's personality and the environment's character.")
        
        return " ".join(narrative_parts)
    
    def _select_opening_shot(self, composition: Dict) -> str:
        """Select appropriate opening shot based on composition"""
        framing = composition.get("framing", "medium_shot")
        
        if framing == "close_up":
            return "medium shot"
        elif framing == "wide_shot":
            return "wide shot"
        else:
            return "medium wide shot"
    
    def _select_effects_for_mood(self, lighting: Dict) -> str:
        """Select camera effects based on lighting mood"""
        brightness = lighting.get("brightness", "medium")
        quality = lighting.get("quality", "soft")
        
        if brightness == "bright" and quality == "soft":
            return "shallow depth of field"
        elif brightness == "dim":
            return "cinematic lighting"
        else:
            return "natural depth of field"
    
    def _select_action_shot(self) -> str:
        """Select camera angle for action shots"""
        return random.choice(["medium shot", "medium close-up", "close-up"])
    
    def _select_movement_for_action(self, action: str) -> str:
        """Select camera movement based on action type"""
        action_lower = action.lower()
        
        if any(word in action_lower for word in ["wave", "gesture", "point"]):
            return "slight zoom in"
        elif any(word in action_lower for word in ["walk", "move", "dance"]):
            return "tracking shot"
        elif any(word in action_lower for word in ["jump", "leap"]):
            return "tilt up"
        else:
            return "dolly in"
    
    def _select_action_effects(self) -> str:
        """Select effects for action shots"""
        return random.choice([
            "motion blur on background",
            "focus pull to subject",
            "shallow depth of field",
            "speed ramping"
        ])
    
    def _estimate_action_duration(self, action: str) -> int:
        """Estimate duration for custom actions"""
        action_lower = action.lower()
        
        for key, duration in self.action_durations.items():
            if key in action_lower:
                return duration
        
        # Default duration based on action complexity
        if len(action.split()) > 3:
            return 4  # Complex actions
        else:
            return 2  # Simple actions
    
    def _generate_natural_action(self, subject: Dict) -> str:
        """Generate natural actions based on subject analysis"""
        pose = subject.get("pose", "standing")
        position = subject.get("position", "center")
        
        actions = [
            "looks around thoughtfully",
            "adjusts posture naturally",
            "shifts weight slightly",
            "turns head to follow something",
            "takes a small step forward",
            "gestures expressively",
            "smiles warmly",
            "looks directly at camera"
        ]
        
        return random.choice(actions)
    
    def _generate_shot_description(self, scene: Dict, subject: Dict, lighting: Dict) -> str:
        """Generate descriptive text for shots"""
        setting = scene.get("setting", "scene")
        environment = scene.get("environment", "space")
        brightness = lighting.get("brightness", "natural")
        
        descriptions = [
            f"capturing the {brightness} ambiance of the {setting}",
            f"revealing details of the {environment} setting",
            f"emphasizing the subject's connection to the {setting}",
            f"showcasing the {brightness} lighting on the subject",
            f"highlighting the texture and depth of the {environment}"
        ]
        
        return random.choice(descriptions)
    
    def _get_movement_description(self) -> str:
        """Get description for camera movement"""
        descriptions = [
            "smooth camera motion",
            "fluid cinematography",
            "dynamic framing",
            "elegant camera work",
            "professional movement"
        ]
        return random.choice(descriptions)
    
    def _get_detailed_setting_description(self, scene: Dict, lighting: Dict, colors: Dict) -> str:
        """Generate detailed setting description for Hunyuan format"""
        setting = scene.get("setting", "scene")
        environment = scene.get("environment", "space")
        brightness = lighting.get("brightness", "natural")
        color_mood = colors.get("color_mood", "neutral")
        
        return f"a {brightness}ly lit {setting} with {color_mood} tones, creating an inviting {environment} atmosphere"
    
    def _get_detailed_subject_description(self, subject: Dict) -> str:
        """Generate detailed subject description"""
        clothing = subject.get("clothing", "casual attire")
        position = subject.get("position", "center")
        size = subject.get("size", "medium")
        
        return f"The subject, wearing {clothing}, is positioned {position} frame in a {size} composition"
    
    def _get_transition_description(self, prev_shot: Dict, current_shot: Dict) -> str:
        """Generate smooth transition descriptions between shots"""
        transitions = [
            "The camera smoothly transitions,",
            "With fluid movement, the camera",
            "Seamlessly, the perspective shifts as",
            "The cinematography flows naturally,",
            "In a graceful motion, the camera"
        ]
        return random.choice(transitions)
    
    def _get_fluid_action_description(self, shot: Dict) -> str:
        """Generate fluid action descriptions for Hunyuan format"""
        camera_angle = shot["camera_angle"]
        movement = shot["camera_movement"]
        action = shot["subject_action"]
        
        descriptions = [
            f"adopting a {camera_angle} while executing a {movement}, capturing as the subject {action} with natural grace and authentic expression.",
            f"shifting to {camera_angle} with {movement}, following the subject's {action} in a way that feels organic and unforced.",
            f"employing {camera_angle} through {movement}, documenting the subject's {action} with cinematic fluidity and emotional resonance."
        ]
        
        return random.choice(descriptions)
    
    def _extract_scene_context(self, basic_desc: str, scene: Dict) -> str:
        """Extract scene context from basic description and analysis"""
        desc_lower = basic_desc.lower()
        
        # Try to extract specific scene elements from description
        if any(word in desc_lower for word in ["outdoor", "outside", "park", "garden", "street", "nature"]):
            return f"outdoor {scene.get('setting', 'environment')}"
        elif any(word in desc_lower for word in ["indoor", "inside", "room", "office", "home", "building"]):
            return f"indoor {scene.get('setting', 'space')}"
        elif any(word in desc_lower for word in ["kitchen", "bedroom", "living room", "bathroom"]):
            room_type = next((word for word in ["kitchen", "bedroom", "living room", "bathroom"] if word in desc_lower), "room")
            return f"{room_type} setting"
        elif any(word in desc_lower for word in ["beach", "ocean", "water", "lake"]):
            return "waterfront location"
        elif any(word in desc_lower for word in ["mountain", "hill", "forest", "tree"]):
            return "natural landscape"
        else:
            # Fallback to analysis or generic
            setting = scene.get("setting", "scene")
            environment = scene.get("environment", "space")
            return f"{environment} {setting}"
    
    def _extract_subject_context(self, basic_desc: str, subject: Dict) -> str:
        """Extract subject context from basic description and analysis"""
        desc_lower = basic_desc.lower()
        
        # Try to extract specific subject details from description
        if any(word in desc_lower for word in ["woman", "girl", "female", "lady"]):
            subject_type = "woman"
        elif any(word in desc_lower for word in ["man", "boy", "male", "guy"]):
            subject_type = "man"
        elif any(word in desc_lower for word in ["child", "kid", "baby"]):
            subject_type = "child"
        elif any(word in desc_lower for word in ["person", "people", "individual"]):
            subject_type = "person"
        else:
            subject_type = "subject"
        
        # Extract clothing or appearance details
        clothing_details = []
        if any(word in desc_lower for word in ["wearing", "dressed", "shirt", "dress", "jacket", "coat"]):
            # Try to extract clothing colors or types
            if "red" in desc_lower:
                clothing_details.append("red clothing")
            elif "blue" in desc_lower:
                clothing_details.append("blue clothing")
            elif "white" in desc_lower:
                clothing_details.append("white clothing")
            elif "black" in desc_lower:
                clothing_details.append("black clothing")
            elif any(word in desc_lower for word in ["shirt", "t-shirt", "blouse"]):
                clothing_details.append("casual shirt")
            elif any(word in desc_lower for word in ["dress", "gown"]):
                clothing_details.append("dress")
            elif any(word in desc_lower for word in ["suit", "formal"]):
                clothing_details.append("formal attire")
        
        # Combine subject type with clothing details
        if clothing_details:
            return f"{subject_type} in {clothing_details[0]}"
        else:
            # Fallback to analysis
            clothing = subject.get("clothing", "casual attire")
            return f"{subject_type} in {clothing}"

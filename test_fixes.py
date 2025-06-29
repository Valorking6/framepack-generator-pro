#!/usr/bin/env python3
"""
Test script to verify the fixes for Framepack Generator Pro
"""

import sys
import os
import json
from PIL import Image
from image_analyzer import ImageAnalyzer
from prompt_generator import PromptGenerator

def test_image_analysis_and_prompts():
    """Test the fixed image analysis and prompt generation"""
    
    # Load settings
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    
    # Test image path
    test_image_path = "/home/ubuntu/Uploads/00005-3655455280.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found at {test_image_path}")
        return False
    
    print("🔍 Testing Framepack Generator Pro fixes...")
    print(f"📸 Using test image: {test_image_path}")
    
    try:
        # Load and analyze image
        image = Image.open(test_image_path)
        print(f"✅ Image loaded successfully: {image.size}")
        
        # Initialize analyzer
        analyzer = ImageAnalyzer(settings)
        print("✅ Image analyzer initialized")
        
        # Analyze image
        print("🔍 Analyzing image...")
        analysis = analyzer.analyze_image(image)
        
        print(f"✅ Image analysis completed using: {analysis.get('analysis_provider', 'unknown')}")
        print(f"📝 Basic description: {analysis.get('basic_description', 'No description')}")
        
        # Initialize prompt generator
        prompt_generator = PromptGenerator()
        print("✅ Prompt generator initialized")
        
        # Generate prompts
        print("🎬 Generating prompts...")
        timestamp_prompt, hunyuan_prompt = prompt_generator.generate_prompts(
            analysis, 
            duration=10, 
            custom_action="waves at the camera"
        )
        
        print("✅ Prompts generated successfully!")
        
        # Display results
        print("\n" + "="*80)
        print("📊 ANALYSIS RESULTS")
        print("="*80)
        print(f"Provider: {analysis.get('analysis_provider', 'unknown')}")
        print(f"Description: {analysis.get('basic_description', 'No description')}")
        print(f"Scene: {analysis.get('scene_details', {})}")
        print(f"Subject: {analysis.get('subject_analysis', {})}")
        print(f"Lighting: {analysis.get('lighting_analysis', {})}")
        
        print("\n" + "="*80)
        print("🎬 TIMESTAMP FORMAT")
        print("="*80)
        print(timestamp_prompt)
        
        print("\n" + "="*80)
        print("🎭 HUNYUAN FORMAT")
        print("="*80)
        print(hunyuan_prompt)
        
        # Save results to file
        results = {
            "analysis": analysis,
            "timestamp_prompt": timestamp_prompt,
            "hunyuan_prompt": hunyuan_prompt,
            "test_image": test_image_path
        }
        
        with open('/home/ubuntu/framepack-generator-pro/test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✅ Results saved to test_results.json")
        
        # Check if results are image-specific
        desc_lower = analysis.get('basic_description', '').lower()
        is_specific = any(word in desc_lower for word in [
            'girl', 'woman', 'blue', 'dress', 'drink', 'car', 'flowers', 'outdoor'
        ])
        
        if is_specific:
            print("✅ SUCCESS: Generated content is image-specific!")
        else:
            print("⚠️  WARNING: Generated content may still be generic")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_image_analysis_and_prompts()
    sys.exit(0 if success else 1)

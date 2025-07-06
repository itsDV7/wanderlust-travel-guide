#!/usr/bin/env python3
"""
Test script for GPT-2 integration with VQA service
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelguide.settings')
django.setup()

from core.gpt2_service import get_gpt2_service
from core.vqa_service import get_vqa_service

def test_gpt2_service():
    """Test the GPT-2 service"""
    print("🧪 Testing GPT-2 Service...")
    
    try:
        # Get GPT-2 service
        gpt2_service = get_gpt2_service()
        
        # Check initial status
        print(f"Initial status: {gpt2_service.get_status()}")
        print(f"Is ready: {gpt2_service.is_ready()}")
        print(f"Is loading: {gpt2_service.is_loading()}")
        
        # Initialize the model
        print("🔄 Initializing GPT-2 model...")
        gpt2_service._initialize_model()
        
        # Check status after initialization
        print(f"Status after init: {gpt2_service.get_status()}")
        print(f"Is ready: {gpt2_service.is_ready()}")
        
        if gpt2_service.is_ready():
            print("✅ GPT-2 model initialized successfully!")
            
            # Test description generation
            test_landmarks = [
                "Eiffel Tower",
                "Taj Mahal", 
                "Pyramids of Giza",
                "Statue of Liberty"
            ]
            
            for landmark in test_landmarks:
                print(f"\n🏛️  Testing description for: {landmark}")
                result = gpt2_service.generate_landmark_description(landmark)
                
                if result['success']:
                    print(f"✅ Success! Description: {result['description'][:100]}...")
                else:
                    print(f"❌ Failed: {result['error']}")
        else:
            print("❌ GPT-2 model failed to initialize")
            
    except Exception as e:
        print(f"❌ Error testing GPT-2 service: {str(e)}")
        import traceback
        traceback.print_exc()

def test_vqa_service():
    """Test the VQA service"""
    print("\n🧪 Testing VQA Service...")
    
    try:
        # Get VQA service
        vqa_service = get_vqa_service()
        
        # Check initial status
        print(f"Initial status: {vqa_service.get_status()}")
        print(f"Is ready: {vqa_service.is_ready()}")
        print(f"Is loading: {vqa_service.is_loading()}")
        
        # Initialize the model
        print("🔄 Initializing VQA model...")
        vqa_service._initialize_model()
        
        # Check status after initialization
        print(f"Status after init: {vqa_service.get_status()}")
        print(f"Is ready: {vqa_service.is_ready()}")
        
        if vqa_service.is_ready():
            print("✅ VQA model initialized successfully!")
        else:
            print("❌ VQA model failed to initialize")
            
    except Exception as e:
        print(f"❌ Error testing VQA service: {str(e)}")
        import traceback
        traceback.print_exc()

def test_integration():
    """Test the integration between VQA and GPT-2"""
    print("\n🧪 Testing VQA + GPT-2 Integration...")
    
    try:
        # Test with a mock landmark name (simulating VQA output)
        mock_landmark_name = "Eiffel Tower"
        
        # Get GPT-2 service
        gpt2_service = get_gpt2_service()
        
        # Initialize if not ready
        if not gpt2_service.is_ready():
            print("🔄 Initializing GPT-2 model for integration test...")
            gpt2_service._initialize_model()
        
        if gpt2_service.is_ready():
            print(f"🏛️  Generating description for: {mock_landmark_name}")
            result = gpt2_service.generate_landmark_description(mock_landmark_name)
            
            if result['success']:
                print("✅ Integration test successful!")
                print(f"Landmark: {mock_landmark_name}")
                print(f"Description: {result['description']}")
            else:
                print(f"❌ Integration test failed: {result['error']}")
        else:
            print("❌ GPT-2 model not ready for integration test")
            
    except Exception as e:
        print(f"❌ Error in integration test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting AI Services Integration Test")
    print("=" * 50)
    
    # Test GPT-2 service
    test_gpt2_service()
    
    # Test VQA service
    test_vqa_service()
    
    # Test integration
    test_integration()
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!") 
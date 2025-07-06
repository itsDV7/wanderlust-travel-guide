#!/usr/bin/env python3
"""
Test script for VQA service
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/Users/divyansh/Travel Guide App/travelguide')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelguide.settings')
django.setup()

from core.vqa_service import get_vqa_service

def test_vqa_service():
    """Test the VQA service"""
    print("Testing VQA service...")
    
    try:
        # Get VQA service
        vqa_service = get_vqa_service()
        
        if vqa_service.is_ready():
            print("✅ VQA service is ready!")
            print(f"Device: {vqa_service.device}")
            print(f"Data type: {vqa_service.dtype}")
        else:
            print("❌ VQA service is not ready")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing VQA service: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    test_vqa_service() 
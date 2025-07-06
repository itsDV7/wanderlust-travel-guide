#!/usr/bin/env python3
"""
Test script to check VQA dependencies
"""

def test_dependencies():
    """Test if all required dependencies are available"""
    print("Testing VQA dependencies...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError as e:
        print(f"❌ PyTorch: {e}")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ Transformers: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✅ Pillow: {Image.__version__}")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False
    
    try:
        import timm
        print(f"✅ Timm: {timm.__version__}")
    except ImportError as e:
        print(f"❌ Timm: {e}")
        return False
    
    try:
        import sentencepiece
        print(f"✅ SentencePiece: {sentencepiece.__version__}")
    except ImportError as e:
        print(f"❌ SentencePiece: {e}")
        return False
    
    try:
        import peft
        print(f"✅ PEFT: {peft.__version__}")
    except ImportError as e:
        print(f"❌ PEFT: {e}")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy: {numpy.__version__}")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False
    
    print("\nTesting device availability...")
    
    try:
        if torch.cuda.is_available():
            print(f"✅ CUDA: Available ({torch.cuda.get_device_name(0)})")
        else:
            print("⚠️ CUDA: Not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")
    
    try:
        if torch.backends.mps.is_available():
            print("✅ MPS: Available")
        else:
            print("⚠️ MPS: Not available")
    except Exception as e:
        print(f"❌ MPS check failed: {e}")
    
    print("✅ CPU: Always available")
    
    return True

if __name__ == "__main__":
    test_dependencies() 
#!/usr/bin/env python3
"""
Simple test for VQA model loading
"""

import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

def test_vqa_loading():
    """Test VQA model loading step by step"""
    print("Testing VQA model loading...")
    
    try:
        import torch
        print(f"✅ PyTorch imported: {torch.__version__}")
    except Exception as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        from transformers import AutoModel, AutoTokenizer
        print("✅ Transformers imported")
    except Exception as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    # Test device selection
    try:
        if torch.cuda.is_available():
            device = 'cuda'
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        elif torch.backends.mps.is_available():
            device = 'mps'
            print("✅ MPS available")
        else:
            device = 'cpu'
            print("✅ Using CPU")
        
        print(f"✅ Device selected: {device}")
    except Exception as e:
        print(f"❌ Device selection failed: {e}")
        return False
    
    # Test dtype selection
    try:
        if device == 'cuda':
            if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8:
                dtype = torch.bfloat16
            else:
                dtype = torch.float16
        elif device == 'mps':
            dtype = torch.float16
        else:
            dtype = torch.float32
        
        print(f"✅ Dtype selected: {dtype}")
    except Exception as e:
        print(f"❌ Dtype selection failed: {e}")
        return False
    
    try:
        print("🔄 Loading model...")
        model = AutoModel.from_pretrained(
            'openbmb/MiniCPM-V-2', 
            trust_remote_code=True, 
            torch_dtype=dtype
        )
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False
    
    try:
        print(f"🔄 Moving model to {device}...")
        model = model.to(device=device, dtype=dtype)
        print(f"✅ Model moved to {device}")
    except Exception as e:
        print(f"❌ Model device move failed: {e}")
        print("🔄 Trying fallback to CPU...")
        try:
            device = 'cpu'
            dtype = torch.float32
            model = model.to(device=device, dtype=dtype)
            print("✅ Model moved to CPU (fallback)")
        except Exception as fallback_error:
            print(f"❌ CPU fallback also failed: {fallback_error}")
            return False
    
    try:
        print("🔄 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            'openbmb/MiniCPM-V-2', 
            trust_remote_code=True
        )
        print("✅ Tokenizer loaded successfully")
    except Exception as e:
        print(f"❌ Tokenizer loading failed: {e}")
        return False
    
    try:
        print("🔄 Setting model to eval mode...")
        model.eval()
        print("✅ Model set to eval mode")
    except Exception as e:
        print(f"❌ Model eval mode failed: {e}")
        return False
    
    print(f"🎉 All VQA components loaded successfully on {device}!")
    return True

if __name__ == "__main__":
    test_vqa_loading() 
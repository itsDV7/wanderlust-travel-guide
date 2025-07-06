import os
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import logging
from typing import Optional

# Set environment variable before any imports
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

logger = logging.getLogger(__name__)

class VQAService:
    """Service class for Visual Question Answering using MiniCPM-V-2 model"""
    
    def __init__(self):
        self.model: Optional[AutoModel] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.device: Optional[str] = None
        self.dtype: Optional[torch.dtype] = None
        self._is_loading = False
        self._load_error = None
        # Don't auto-initialize - let the background thread do it
    
    def _get_device(self):
        """Determine the best available device"""
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        else:
            return 'cpu'
    
    def _get_dtype(self, device):
        """Determine the best dtype for the device"""
        if device == 'cuda':
            # Check if CUDA device supports bfloat16
            if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8:
                return torch.bfloat16
            else:
                return torch.float16
        elif device == 'mps':
            return torch.float16
        else:
            return torch.float32
    
    def _initialize_model(self):
        """Initialize the VQA model and tokenizer"""
        if self._is_loading:
            logger.info("Model is already loading...")
            return
            
        self._is_loading = True
        self._load_error = None
        
        try:
            self.device = self._get_device()
            self.dtype = self._get_dtype(self.device)
            
            logger.info(f"Initializing VQA model on device: {self.device} with dtype: {self.dtype}")
            
            # Load model
            self.model = AutoModel.from_pretrained(
                'openbmb/MiniCPM-V-2', 
                trust_remote_code=True, 
                torch_dtype=self.dtype
            )
            
            # Try to move to selected device, fallback to CPU if it fails
            try:
                self.model = self.model.to(device=self.device, dtype=self.dtype)
                logger.info(f"Model successfully moved to {self.device}")
            except Exception as device_error:
                logger.warning(f"Failed to move model to {self.device}: {device_error}")
                logger.info("Falling back to CPU")
                self.device = 'cpu'
                self.dtype = torch.float32
                self.model = self.model.to(device=self.device, dtype=self.dtype)
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                'openbmb/MiniCPM-V-2', 
                trust_remote_code=True
            )
            
            # Set model to evaluation mode
            self.model.eval()
            
            logger.info(f"VQA model initialized successfully on {self.device}")
            
        except Exception as e:
            self._load_error = str(e)
            logger.error(f"Failed to initialize VQA model: {str(e)}")
            raise
        finally:
            self._is_loading = False
    
    def identify_landmark(self, image_path):
        """
        Identify landmark in the given image
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Contains 'success' (bool), 'landmark_name' (str), and 'error' (str if any)
        """
        if self._is_loading:
            return {
                'success': False,
                'landmark_name': None,
                'error': 'VQA model is still loading. Please try again in a moment.'
            }
        
        if not self.is_ready():
            if self._load_error:
                return {
                    'success': False,
                    'landmark_name': None,
                    'error': f'VQA model failed to load: {self._load_error}'
                }
            return {
                'success': False,
                'landmark_name': None,
                'error': 'VQA model is not ready'
            }
        
        try:
            # Load and convert image
            image = Image.open(image_path).convert('RGB')
            
            # Prepare question
            question = 'What is the name of the landmark in the image?'
            msgs = [{'role': 'user', 'content': question}]
            
            # Get model prediction
            with torch.no_grad():
                res, context, _ = self.model.chat(
                    image=image,
                    msgs=msgs,
                    context=None,
                    tokenizer=self.tokenizer,
                    sampling=True,
                    temperature=0.7
                )
            
            logger.info(f"Landmark identification result: {res}")
            
            return {
                'success': True,
                'landmark_name': res.strip(),
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Error identifying landmark: {str(e)}")
            return {
                'success': False,
                'landmark_name': None,
                'error': str(e)
            }
    
    def chat_with_landmark_context(self, user_message, landmark_name, image_path=None):
        """
        Chat with the VQA model using landmark context
        
        Args:
            user_message (str): User's message
            landmark_name (str): Name of the landmark for context
            image_path (str, optional): Path to the landmark image
            
        Returns:
            dict: Contains 'success' (bool), 'response' (str), and 'error' (str if any)
        """
        if self._is_loading:
            return {
                'success': False,
                'response': None,
                'error': 'VQA model is still loading. Please try again in a moment.'
            }
        
        if not self.is_ready():
            if self._load_error:
                return {
                    'success': False,
                    'response': None,
                    'error': f'VQA model failed to load: {self._load_error}'
                }
            return {
                'success': False,
                'response': None,
                'error': 'VQA model is not ready'
            }
        
        try:
            # Prepare the message with landmark context
            contextual_message = f"About {landmark_name}: {user_message}"
            
            # Prepare messages for the model
            msgs = [{'role': 'user', 'content': contextual_message}]
            
            # Load image if provided
            image = None
            if image_path and os.path.exists(image_path):
                try:
                    image = Image.open(image_path).convert('RGB')
                except Exception as img_error:
                    logger.warning(f"Failed to load image {image_path}: {img_error}")
                    image = None
            
            # Get model response
            with torch.no_grad():
                # For MiniCPM-V-2, we need to provide an image parameter even for text-only chat
                # We'll create a dummy/empty image or use the original image if available
                if image is not None:
                    # Chat with the provided image
                    res, context, _ = self.model.chat(
                        image=image,
                        msgs=msgs,
                        context=None,
                        tokenizer=self.tokenizer,
                        sampling=True,
                        temperature=0.7
                    )
                else:
                    # For text-only chat, we'll create a simple 1x1 pixel image as a placeholder
                    # This satisfies the model's requirement for an image parameter
                    dummy_image = Image.new('RGB', (1, 1), color='white')
                    res, context, _ = self.model.chat(
                        image=dummy_image,
                        msgs=msgs,
                        context=None,
                        tokenizer=self.tokenizer,
                        sampling=True,
                        temperature=0.7
                    )
            
            logger.info(f"Chat response for {landmark_name}: {res}")
            
            return {
                'success': True,
                'response': res.strip(),
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Error in chat with landmark context: {str(e)}")
            return {
                'success': False,
                'response': None,
                'error': str(e)
            }
    
    def is_ready(self):
        """Check if the VQA service is ready to use"""
        return self.model is not None and self.tokenizer is not None
    
    def is_loading(self):
        """Check if the VQA service is currently loading"""
        return self._is_loading
    
    def get_status(self):
        """Get the current status of the VQA service"""
        if self._is_loading:
            return 'loading'
        elif self.is_ready():
            return 'ready'
        elif self._load_error:
            return 'error'
        else:
            return 'not_initialized'

# Global instance
vqa_service = None

def get_vqa_service():
    """Get or create the global VQA service instance"""
    global vqa_service
    if vqa_service is None:
        vqa_service = VQAService()
    return vqa_service 
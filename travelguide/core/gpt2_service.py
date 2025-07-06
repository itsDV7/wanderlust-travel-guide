import os
import torch
from transformers import pipeline, set_seed, Pipeline
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GPT2Service:
    """Service class for GPT-2 text generation for landmark descriptions"""
    
    def __init__(self):
        self.generator: Optional[Pipeline] = None
        self._is_loading = False
        self._load_error = None
        self.device: Optional[str] = None
    
    def _get_device(self):
        """Determine the best available device"""
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        else:
            return 'cpu'
    
    def _initialize_model(self):
        """Initialize the GPT-2 model"""
        if self._is_loading:
            logger.info("GPT-2 model is already loading...")
            return
            
        self._is_loading = True
        self._load_error = None
        
        try:
            self.device = self._get_device()
            logger.info(f"Initializing GPT-2 model on device: {self.device}")
            
            # Set seed for reproducible results
            set_seed(42)
            
            # Load GPT-2 model
            # Use float32 for MPS to avoid LayerNormKernelImpl issues
            dtype = torch.float32 if self.device == 'mps' else (torch.float16 if self.device == 'cuda' else torch.float32)
            
            self.generator = pipeline(
                'text-generation',
                model='gpt2',
                device=0 if self.device == 'cuda' else -1,  # -1 for CPU, 0 for CUDA
                torch_dtype=dtype
            )
            
            logger.info(f"GPT-2 model initialized successfully on {self.device}")
            
        except Exception as e:
            self._load_error = str(e)
            logger.error(f"Failed to initialize GPT-2 model: {str(e)}")
            raise
        finally:
            self._is_loading = False
    
    def generate_landmark_description(self, landmark_name: str, max_length: int = 150, num_return_sequences: int = 1):
        """
        Generate a description about the landmark's significance and history
        
        Args:
            landmark_name (str): Name of the landmark from VQA model
            max_length (int): Maximum length of generated text
            num_return_sequences (int): Number of sequences to generate
            
        Returns:
            dict: Contains 'success' (bool), 'description' (str), and 'error' (str if any)
        """
        if self._is_loading:
            return {
                'success': False,
                'description': None,
                'error': 'GPT-2 model is still loading. Please try again in a moment.'
            }
        
        if not self.is_ready():
            if self._load_error:
                return {
                    'success': False,
                    'description': None,
                    'error': f'GPT-2 model failed to load: {self._load_error}'
                }
            return {
                'success': False,
                'description': None,
                'error': 'GPT-2 model is not ready'
            }
        
        try:
            # Create a prompt for the landmark description
            prompt = f"Write a brief description of the significance and history of {landmark_name}:"
            
            # Generate text
            with torch.no_grad():
                if self.generator is None:
                    return {
                        'success': False,
                        'description': None,
                        'error': 'GPT-2 generator is not initialized'
                    }
                
                # Get the EOS token ID safely
                pad_token_id = None
                if hasattr(self.generator, 'tokenizer') and self.generator.tokenizer is not None:
                    pad_token_id = getattr(self.generator.tokenizer, 'eos_token_id', None)
                
                result = self.generator(
                    prompt,
                    max_length=max_length,
                    num_return_sequences=num_return_sequences,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=pad_token_id
                )
            
            # Extract the generated text
            if result and isinstance(result, list) and len(result) > 0:
                first_result = result[0]
                if isinstance(first_result, dict) and 'generated_text' in first_result:
                    generated_text = first_result['generated_text']
                    
                    # Clean up the text - remove the original prompt and clean formatting
                    if isinstance(generated_text, str):
                        description = generated_text.replace(prompt, '').strip()
                        
                        # If the description is too short, try with a longer max_length
                        if len(description) < 50 and max_length < 200:
                            return self.generate_landmark_description(landmark_name, max_length + 50, num_return_sequences)
                        
                        logger.info(f"Generated description for {landmark_name}: {description[:100]}...")
                        
                        return {
                            'success': True,
                            'description': description,
                            'error': None
                        }
            
            return {
                'success': False,
                'description': None,
                'error': 'No text was generated'
            }
            
        except Exception as e:
            logger.error(f"Error generating landmark description: {str(e)}")
            return {
                'success': False,
                'description': None,
                'error': str(e)
            }
    
    def is_ready(self):
        """Check if the GPT-2 service is ready to use"""
        return self.generator is not None
    
    def is_loading(self):
        """Check if the GPT-2 service is currently loading"""
        return self._is_loading
    
    def get_status(self):
        """Get the current status of the GPT-2 service"""
        if self._is_loading:
            return 'loading'
        elif self.is_ready():
            return 'ready'
        elif self._load_error:
            return 'error'
        else:
            return 'not_initialized'

# Global instance
gpt2_service = None

def get_gpt2_service():
    """Get or create the global GPT-2 service instance"""
    global gpt2_service
    if gpt2_service is None:
        gpt2_service = GPT2Service()
    return gpt2_service 
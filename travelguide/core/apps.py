from django.apps import AppConfig
import threading
import logging
import os

logger = logging.getLogger(__name__)

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """Load VQA model in background when app starts"""
        # Only run in main thread to avoid duplicate loading
        if os.environ.get('RUN_MAIN', None) != 'true':
            logger.info("Skipping VQA model loading (not main thread)")
            return
            
        logger.info("Starting VQA model background loading...")
        
        # Load models in background thread
        def load_models():
            try:
                logger.info("🔄 Models loading started in background thread...")
                
                # Set environment variable
                os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
                
                # Load VQA model
                try:
                    from .vqa_service import get_vqa_service
                    vqa_service = get_vqa_service()
                    
                    logger.info("🔄 Initializing VQA model...")
                    vqa_service._initialize_model()
                    
                    if vqa_service.is_ready():
                        logger.info("✅ VQA model loaded successfully!")
                    else:
                        logger.error("❌ VQA model failed to load")
                except Exception as e:
                    logger.error(f"❌ Error loading VQA model: {str(e)}")
                
                # Load GPT-2 model
                try:
                    from .gpt2_service import get_gpt2_service
                    gpt2_service = get_gpt2_service()
                    
                    logger.info("🔄 Initializing GPT-2 model...")
                    gpt2_service._initialize_model()
                    
                    if gpt2_service.is_ready():
                        logger.info("✅ GPT-2 model loaded successfully!")
                    else:
                        logger.error("❌ GPT-2 model failed to load")
                except Exception as e:
                    logger.error(f"❌ Error loading GPT-2 model: {str(e)}")
                    
            except Exception as e:
                logger.error(f"❌ Error loading models: {str(e)}")
                import traceback
                logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Start background thread
        try:
            model_thread = threading.Thread(target=load_models, daemon=True, name="AI-Models-Loader")
            model_thread.start()
            logger.info("✅ AI models loading thread started")
        except Exception as e:
            logger.error(f"❌ Failed to start AI models loading thread: {e}") 
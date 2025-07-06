from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, LandmarkImageForm
from .models import LandmarkImage, SavedLocation
import os
import logging
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import json

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'core/home.html')

def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name} {user.last_name}!')
                # Redirect to the page they were trying to access, or home
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required(login_url='core:login')
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('core:home')

@login_required(login_url='core:login')
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'core/profile.html', {'form': form})

@login_required(login_url='core:login')
def explore_nearby_view(request):
    """Explore nearby landmarks view"""
    return render(request, 'core/explore_nearby.html')

@login_required(login_url='core:login')
def find_landmark_view(request):
    """Find landmark by image upload view"""
    uploaded_image = None
    landmark_result = None
    
    if request.method == 'POST':
        form = LandmarkImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            
            # Create LandmarkImage instance and save
            landmark_image = LandmarkImage.objects.create(
                user=request.user,
                image=uploaded_image
            )
            
            # Try to identify the landmark using VQA model
            try:
                from .vqa_service import get_vqa_service
                vqa_service = get_vqa_service()
                
                # Check if model is loading
                if vqa_service.is_loading():
                    landmark_result = {
                        'error': 'VQA model is still loading. Please try again in a moment.',
                        'success': False
                    }
                    messages.warning(request, 'AI model is still loading. Please try again in a moment.')
                elif vqa_service.is_ready():
                    # Create a temporary file for VQA processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                        # Write the uploaded file content to the temporary file
                        for chunk in uploaded_image.chunks():
                            temp_file.write(chunk)
                        temp_file.flush()
                        image_path = temp_file.name
                    
                    # Clean up the temporary file after processing
                    try:
                        result = vqa_service.identify_landmark(image_path)
                        os.unlink(image_path)  # Delete temporary file
                    except Exception as e:
                        # Clean up on error too
                        if os.path.exists(image_path):
                            os.unlink(image_path)
                        raise e
                    
                    if result['success']:
                        # Update the landmark image with the identified name
                        landmark_image.landmark_name = result['landmark_name']
                        landmark_image.save()
                        
                        # Try to generate description using GPT-2
                        description = None
                        try:
                            from .gpt2_service import get_gpt2_service
                            gpt2_service = get_gpt2_service()
                            
                            if gpt2_service.is_ready():
                                description_result = gpt2_service.generate_landmark_description(
                                    result['landmark_name']
                                )
                                if description_result['success']:
                                    description = description_result['description']
                                else:
                                    logger.warning(f"GPT-2 description generation failed: {description_result['error']}")
                            else:
                                logger.info("GPT-2 model not ready, skipping description generation")
                        except Exception as e:
                            logger.warning(f"Error generating description with GPT-2: {str(e)}")
                        
                        landmark_result = {
                            'name': result['landmark_name'],
                            'description': description,
                            'success': True
                        }
                    else:
                        landmark_result = {
                            'error': result['error'],
                            'success': False
                        }
                        messages.warning(request, f'Could not identify landmark: {result["error"]}')
                else:
                    # Model is not ready - try to initialize it
                    try:
                        vqa_service._initialize_model()
                        landmark_result = {
                            'error': 'VQA model is initializing. Please try again in a moment.',
                            'success': False
                        }
                        messages.warning(request, 'AI model is initializing. Please try again in a moment.')
                    except Exception as e:
                        landmark_result = {
                            'error': f'VQA model failed to initialize: {str(e)}',
                            'success': False
                        }
                        messages.error(request, 'AI model failed to initialize.')
                    
            except ImportError:
                landmark_result = {
                    'error': 'VQA model dependencies not available',
                    'success': False
                }
                messages.warning(request, 'AI model dependencies are not installed.')
            except Exception as e:
                logger.error(f"Error in landmark identification: {str(e)}")
                landmark_result = {
                    'error': 'An error occurred during landmark identification',
                    'success': False
                }
                messages.error(request, 'An error occurred while identifying the landmark.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LandmarkImageForm()
    
    return render(request, 'core/find_landmark.html', {
        'form': form,
        'uploaded_image': landmark_image.image if 'landmark_image' in locals() else None,
        'landmark_result': landmark_result
    })

@login_required(login_url='core:login')
def vqa_status_view(request):
    """Check VQA model status"""
    try:
        from .vqa_service import get_vqa_service
        vqa_service = get_vqa_service()
        
        status = vqa_service.get_status()
        
        return JsonResponse({
            'status': status,
            'is_ready': vqa_service.is_ready(),
            'is_loading': vqa_service.is_loading()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'is_ready': False,
            'is_loading': False
        })

@login_required(login_url='core:login')
def gpt2_status_view(request):
    """Check GPT-2 model status"""
    try:
        from .gpt2_service import get_gpt2_service
        gpt2_service = get_gpt2_service()
        
        status = gpt2_service.get_status()
        
        return JsonResponse({
            'status': status,
            'is_ready': gpt2_service.is_ready(),
            'is_loading': gpt2_service.is_loading()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'is_ready': False,
            'is_loading': False
        })

@login_required(login_url='core:login')
def vqa_chat_view(request):
    """Chat with VQA model about a landmark"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            landmark_name = data.get('landmark_name', '').strip()
            image_url = data.get('image_path', '').strip()
            
            if not user_message or not landmark_name:
                return JsonResponse({
                    'success': False,
                    'error': 'Message and landmark name are required'
                })
            
            from .vqa_service import get_vqa_service
            vqa_service = get_vqa_service()
            
            if not vqa_service.is_ready():
                return JsonResponse({
                    'success': False,
                    'error': 'VQA model is not ready. Please try again in a moment.'
                })
            
            # Convert image URL to file path if provided
            image_path = None
            if image_url:
                # Remove leading slash and convert to file path
                if image_url.startswith('/media/'):
                    image_path = os.path.join(settings.MEDIA_ROOT, image_url[7:])  # Remove '/media/' prefix
                else:
                    image_path = image_url
            
            # Get the chat response with optional image path
            result = vqa_service.chat_with_landmark_context(user_message, landmark_name, image_path)
            
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            })
        except Exception as e:
            logger.error(f"Error in VQA chat: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred while processing your message'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST requests are allowed'
    })

@login_required(login_url='core:login')
def plan_view(request):
    """Display user's saved locations for travel planning"""
    saved_locations = SavedLocation.objects.filter(user=request.user).order_by('-saved_at')
    return render(request, 'core/plan.html', {'saved_locations': saved_locations})

@login_required(login_url='core:login')
def save_location_view(request):
    """Save a location from explore nearby page"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract location data
            place_id = data.get('place_id')
            name = data.get('name')
            address = data.get('address')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            types = data.get('types', [])
            rating = data.get('rating')
            user_ratings_total = data.get('user_ratings_total')
            
            # Validate required fields
            if not all([place_id, name, address]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required location data'
                })
            
            # Check if location is already saved
            existing_location = SavedLocation.objects.filter(
                user=request.user, 
                place_id=place_id
            ).first()
            
            if existing_location:
                return JsonResponse({
                    'success': False,
                    'error': 'Location already saved'
                })
            
            # Create new saved location
            saved_location = SavedLocation.objects.create(
                user=request.user,
                place_id=place_id,
                name=name,
                address=address,
                latitude=latitude,
                longitude=longitude,
                types=types,
                rating=rating,
                user_ratings_total=user_ratings_total
            )
            
            return JsonResponse({
                'success': True,
                'message': f'{name} has been saved to your travel plan!',
                'location_id': saved_location.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            })
        except Exception as e:
            logger.error(f"Error saving location: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred while saving the location'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST requests are allowed'
    })

@login_required(login_url='core:login')
def remove_saved_location_ajax_view(request, place_id):
    """Remove a saved location via AJAX using place_id"""
    if request.method == 'POST':
        try:
            saved_location = SavedLocation.objects.get(
                place_id=place_id,
                user=request.user
            )
            location_name = saved_location.name
            saved_location.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'{location_name} has been removed from your travel plan.'
            })
            
        except SavedLocation.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Location not found or you do not have permission to remove it.'
            })
        except Exception as e:
            logger.error(f"Error removing saved location: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred while removing the location.'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST requests are allowed'
    })

@login_required(login_url='core:login')
def get_saved_locations_view(request):
    """Get user's saved location IDs for checking saved state"""
    if request.method == 'GET':
        try:
            saved_locations = SavedLocation.objects.filter(user=request.user)
            saved_place_ids = list(saved_locations.values_list('place_id', flat=True))
            
            return JsonResponse({
                'success': True,
                'saved_place_ids': saved_place_ids
            })
            
        except Exception as e:
            logger.error(f"Error getting saved locations: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred while getting saved locations.'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Only GET requests are allowed'
    })

@login_required(login_url='core:login')
def remove_saved_location_view(request, location_id):
    """Remove a saved location from user's plan"""
    try:
        saved_location = SavedLocation.objects.get(
            id=location_id,
            user=request.user
        )
        location_name = saved_location.name
        saved_location.delete()
        
        messages.success(request, f'{location_name} has been removed from your travel plan.')
        return redirect('core:plan')
        
    except SavedLocation.DoesNotExist:
        messages.error(request, 'Location not found or you do not have permission to remove it.')
        return redirect('core:plan')
    except Exception as e:
        logger.error(f"Error removing saved location: {str(e)}")
        messages.error(request, 'An error occurred while removing the location.')
        return redirect('core:plan') 
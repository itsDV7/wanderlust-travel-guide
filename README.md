# 🧭 Wanderlust - AI-Powered Travel Guide App

A comprehensive Django-based travel application that combines AI-powered landmark identification with location-based exploration and travel planning features.

**Creator:** Divyansh Chaudhary, MCS from UIUC

## Tutorial:

[![Travel Guide Tutorial](HomePage.png)](https://folge.me/g/shared/Ynj5NJWdyQezryd/travel-guide-tutorial)

## 🌟 Features

### 🎯 Core Functionality
- **AI Landmark Identification**: Upload images and get instant landmark recognition using advanced computer vision models
- **Nearby Exploration**: Discover landmarks and attractions around your current location using Google Places API
- **Travel Planning**: Save and manage your favorite locations in a personalized travel plan
- **Interactive Chat**: Ask questions about identified landmarks using AI-powered conversational interface

### 🤖 AI-Powered Features
- **VQA (Visual Question Answering) Model**: Identifies landmarks from uploaded images
- **GPT-2 Integration**: Generates detailed descriptions and answers questions about landmarks
- **Real-time Processing**: Instant AI model status monitoring and response generation

### 🗺️ Location Services
- **Google Places Integration**: Real-time nearby location discovery
- **Interactive Maps**: Visual representation of saved locations using Leaflet.js
- **Location Management**: Save, organize, and remove locations from your travel plan

## 🏗️ Project Structure

```
Travel Guide App/
├── requirements.txt                 # Python dependencies
├── travelguide/                    # Main Django project
│   ├── manage.py                   # Django management script
│   ├── db.sqlite3                  # SQLite database
│   ├── core/                       # Main Django app
│   │   ├── models.py               # Database models
│   │   ├── views.py                # View functions and logic
│   │   ├── urls.py                 # URL routing
│   │   ├── forms.py                # Django forms
│   │   ├── admin.py                # Django admin configuration
│   │   ├── apps.py                 # App configuration
│   │   ├── vqa_service.py          # VQA model service
│   │   ├── gpt2_service.py         # GPT-2 model service
│   │   ├── migrations/             # Database migrations
│   │   └── templates/core/         # HTML templates
│   │       ├── home.html           # Landing page
│   │       ├── login.html          # Login page
│   │       ├── signup.html         # Registration page
│   │       ├── profile.html        # User profile page
│   │       ├── explore_nearby.html # Nearby exploration page
│   │       ├── find_landmark.html  # Landmark identification page
│   │       └── plan.html           # Travel planning page
│   ├── static/                     # Static files
│   │   ├── css/                    # Stylesheets
│   │   │   ├── style.css           # Main styles
│   │   │   └── explore.css         # Exploration page styles
│   │   ├── js/                     # JavaScript files
│   │   │   ├── main.js             # Main JavaScript
│   │   │   ├── explore.js          # Exploration functionality
│   │   │   └── signup.js           # Registration validation
│   │   └── images/                 # Static images
│   ├── media/                      # User-uploaded files
│   │   ├── landmark_images/        # Uploaded landmark images
│   │   └── profile_pictures/       # User profile pictures
│   └── travelguide/                # Django project settings
│       ├── settings.py             # Django settings
│       ├── urls.py                 # Main URL configuration
│       ├── wsgi.py                 # WSGI configuration
│       └── asgi.py                 # ASGI configuration
└── test_*.py                       # Test files
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd "Travel Guide App"
```

### Step 2: Set Up Environment Variables
```bash
# Copy the example environment file
cp env.example .env

# Edit .env file with your configuration
# - Generate a new Django SECRET_KEY
# - Add your Google Places API key (optional)
# - Configure other settings as needed
```

### Step 3: Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
cd travelguide
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📋 Dependencies

### Core Dependencies
- **Django 4.2.23**: Web framework
- **Pillow 10.1.0**: Image processing
- **torch 2.1.2**: PyTorch for deep learning
- **torchvision 0.16.2**: Computer vision utilities
- **transformers 4.36.0**: Hugging Face transformers library
- **timm 0.9.10**: Computer vision models
- **numpy**: Numerical computing

### AI/ML Dependencies
- **sentencepiece 0.1.99**: Text tokenization
- **peft 0.7.1**: Parameter-efficient fine-tuning

## 🎯 Key Features Implementation

### 1. AI Landmark Identification
**Location**: `core/vqa_service.py`, `core/views.py`

**How it works**:
- Uses a pre-trained VQA (Visual Question Answering) model
- Processes uploaded images through the model
- Extracts landmark names from AI responses
- Provides detailed descriptions and chat functionality

**Key Components**:
```python
# VQA Service initialization
class VQAService:
    def __init__(self):
        self.model = None
        self.processor = None
        self.is_ready = False
    
    def identify_landmark(self, image_path):
        # Process image and return landmark identification
```

### 2. Nearby Location Exploration
**Location**: `core/views.py`, `static/js/explore.js`

**How it works**:
- Uses Google Places API for location discovery
- Implements geolocation to find user's current position
- Displays nearby landmarks with ratings, types, and addresses
- Allows saving locations to travel plan

**Key Features**:
- Real-time location search
- Interactive save/unsave functionality
- Persistent saved state management

### 3. Travel Planning System
**Location**: `core/models.py`, `core/views.py`, `templates/core/plan.html`

**How it works**:
- `SavedLocation` model stores user's saved places
- Interactive map using Leaflet.js
- AJAX-based save/remove operations
- Supports both regular locations and AI-identified landmarks

**Database Model**:
```python
class SavedLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    types = models.JSONField(default=list)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    saved_at = models.DateTimeField(auto_now_add=True)
```

### 4. User Authentication & Profiles
**Location**: `core/models.py`, `core/views.py`, `core/forms.py`

**Features**:
- Custom user profile with profile pictures
- Secure authentication system
- User-specific saved locations
- Profile management interface

### 5. Interactive Chat System
**Location**: `core/views.py`, `templates/core/find_landmark.html`

**How it works**:
- Real-time chat interface for landmark questions
- Integrates with VQA model for contextual responses
- Maintains conversation context about identified landmarks

## 🎨 Frontend Implementation

### Design System
- **Bootstrap 5.3.0**: Responsive UI framework
- **Bootstrap Icons**: Icon library
- **Custom CSS**: Modern, gradient-based design
- **Squircle Cards**: Rounded corner design elements

### Key JavaScript Features
- **AJAX Integration**: Seamless backend communication
- **Real-time Updates**: Dynamic content loading
- **Form Validation**: Client-side validation
- **Interactive Maps**: Leaflet.js integration

## 🔧 Configuration

### Environment Variables
The application uses environment variables for sensitive configuration. Copy `env.example` to `.env` and configure:

1. **SECRET_KEY**: Generate a new Django secret key
2. **DEBUG**: Set to `False` in production
3. **ALLOWED_HOSTS**: Configure for your domain
4. **GOOGLE_PLACES_API_KEY**: Add your API key for location features
5. **Database**: Consider PostgreSQL for production

### Security Best Practices
- Never commit `.env` files to version control
- Generate a unique SECRET_KEY for each deployment
- Use environment variables for all sensitive data
- Keep DEBUG=False in production
- Regularly update dependencies

### Google Places API
To enable nearby location features:
1. Get a Google Places API key
2. Add it to your environment variables
3. Configure the API in the views

## 🧪 Testing

The project includes several test files:
- `test_vqa.py`: VQA model testing
- `test_gpt2_integration.py`: GPT-2 integration testing
- `test_dependencies.py`: Dependency verification

Run tests with:
```bash
python manage.py test
```

## 🚀 Deployment

### Production Considerations
1. **Static Files**: Run `python manage.py collectstatic`
2. **Database**: Use PostgreSQL or MySQL
3. **Web Server**: Configure with Nginx + Gunicorn
4. **Environment**: Set `DEBUG=False`
5. **Security**: Update `SECRET_KEY` and `ALLOWED_HOSTS`

### Docker Deployment (Recommended)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "travelguide.wsgi:application"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Creator

**Divyansh Chaudhary**  
MCS from UIUC  
- LinkedIn: [https://www.linkedin.com/in/divyansh7c](https://www.linkedin.com/in/divyansh7c)
- GitHub: [https://github.com/itsDV7](https://github.com/itsDV7)

## 🙏 Acknowledgments

- Django community for the excellent web framework
- Hugging Face for the transformer models
- Google Places API for location services
- Bootstrap team for the UI framework
- UIUC for the academic foundation

---

**Built with ❤️ and AI 🤖** 

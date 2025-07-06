from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with Bootstrap styling"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload a profile picture (optional)'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Style all fields with Bootstrap classes
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        
        # Remove help text from all fields for cleaner UI
        for field in self.fields.values():
            if hasattr(field, 'help_text'):
                field.help_text = ''
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Please choose a different one.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered. Please use a different email or try logging in.')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match. Please make sure both passwords are identical.')
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Save profile picture if provided
            profile_picture = self.cleaned_data.get('profile_picture')
            if profile_picture:
                user.profile.profile_picture = profile_picture
                user.profile.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with Bootstrap styling"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile picture"""
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

class LandmarkImageForm(forms.Form):
    """Form for uploading landmark images"""
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'landmark-image-input'
        }),
        help_text='Upload an image of a landmark to identify it'
    )
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (limit to 10MB)
            if image.size > 10 * 1024 * 1024:
                raise ValidationError('Image file size must be less than 10MB.')
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise ValidationError('Please upload a valid image file (JPEG, PNG, or GIF).')
        
        return image 
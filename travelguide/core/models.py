from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Extended user profile with profile picture"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text='Upload a profile picture (optional)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def profile_picture_url(self):
        """Return the profile picture URL"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return None

class LandmarkImage(models.Model):
    """Model to store uploaded landmark images"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='landmark_images')
    image = models.ImageField(
        upload_to='landmark_images/',
        help_text='Uploaded landmark image'
    )
    landmark_name = models.CharField(max_length=255, null=True, blank=True)
    identified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Landmark image by {self.user.username} - {self.landmark_name or 'Unknown'}"

class SavedLocation(models.Model):
    """Model to store locations saved by users from explore nearby"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_locations')
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    place_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    types = models.JSONField(default=list)  # Store place types as JSON array
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    user_ratings_total = models.IntegerField(null=True, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'place_id']
    
    def __str__(self):
        return f"{self.name} - Saved by {self.user.username}"

# Signal to automatically create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        UserProfile.objects.create(user=instance) 
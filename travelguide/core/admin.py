from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, SavedLocation

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_picture')
    
    def get_profile_picture(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return f"✓ Has Profile Picture"
        return "No Profile Picture"
    get_profile_picture.short_description = 'Profile Picture'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(SavedLocation)
class SavedLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'address', 'rating', 'saved_at')
    list_filter = ('saved_at', 'rating', 'types')
    search_fields = ('name', 'address', 'user__username')
    readonly_fields = ('saved_at',)
    date_hierarchy = 'saved_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user') 
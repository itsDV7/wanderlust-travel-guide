from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('explore/', views.explore_nearby_view, name='explore_nearby'),
    path('find-landmark/', views.find_landmark_view, name='find_landmark'),
    path('vqa-status/', views.vqa_status_view, name='vqa_status'),
    path('gpt2-status/', views.gpt2_status_view, name='gpt2_status'),
    path('vqa-chat/', views.vqa_chat_view, name='vqa_chat'),
    path('plan/', views.plan_view, name='plan'),
    path('save-location/', views.save_location_view, name='save_location'),
    path('remove-location/<int:location_id>/', views.remove_saved_location_view, name='remove_saved_location'),
    path('remove-saved-location-ajax/<str:place_id>/', views.remove_saved_location_ajax_view, name='remove_saved_location_ajax'),
    path('get-saved-locations/', views.get_saved_locations_view, name='get_saved_locations'),
] 
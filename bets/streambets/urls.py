from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import IndexPage, UserProfile, logoutUser, ChannelPage


urlpatterns = [
    path('', IndexPage.as_view(), name='main_index_page'),
    path('profile', UserProfile.as_view(), name = 'user_profile_page'),

    path('channel/<str:channel_url>/', ChannelPage.as_view(), name='channel'),
    
    path('logout', logoutUser, name="logout"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
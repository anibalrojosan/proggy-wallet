from django.urls import path

from .views import ProfileDetailView

app_name = 'profiles'

urlpatterns = [
    path('me/', ProfileDetailView.as_view(), name='profile_detail'),
]

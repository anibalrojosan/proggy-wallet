from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .models import UserProfile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Ensure the user only sees their own profile and prevents tampering with the ID in the URL
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

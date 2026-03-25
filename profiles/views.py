from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm
from .models import UserProfile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    "View to display the user's profile"

    model = UserProfile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Ensure the user only sees their own profile and prevents tampering with the ID in the URL
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    "View to update the user's profile"

    model = UserProfile
    form_class = ProfileForm
    template_name = "profiles/profile_form.html"
    success_url = reverse_lazy("profiles:profile_detail")

    def get_object(self, queryset=None):
        # Ensure the user only updates their own profile
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)

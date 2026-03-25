import os
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

from .models import UserProfile


class ProfileTests(TestCase):
    def setUp(self):
        # Create two users for testing cross-access
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.client = Client()

    def test_profile_detail_access_control(self):
        """Logged out users should be redirected to login."""
        response = self.client.get(reverse("profiles:profile_detail"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_profile_auto_creation(self):
        """A profile should be created on first access to the detail view."""
        self.client.login(username="user1", password="password123")
        response = self.client.get(reverse("profiles:profile_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserProfile.objects.filter(user=self.user1).exists())

    def test_profile_edit_access_control(self):
        """Users can only edit their own profile."""
        self.client.login(username="user1", password="password123")
        response = self.client.get(reverse("profiles:profile_edit"))
        self.assertEqual(response.status_code, 200)
        # Verify the instance in the form is user1's profile
        self.assertEqual(response.context["form"].instance.user, self.user1)

    def test_invalid_avatar_upload(self):
        """Files larger than 2MB should be rejected."""
        self.client.login(username="user1", password="password123")

        # Valid JPEG > 2MB so ImageField accepts it and clean_avatar rejects size.
        width = height = 1400
        buffer = BytesIO()
        while True:
            raw = os.urandom(width * height * 3)
            image = Image.frombytes("RGB", (width, height), raw)
            buffer.seek(0)
            buffer.truncate()
            image.save(buffer, format="JPEG", quality=95)
            large_content = buffer.getvalue()
            if len(large_content) > 2 * 1024 * 1024:
                break
            width += 200
            height += 200
        large_file = SimpleUploadedFile(
            "large.jpg",
            large_content,
            content_type="image/jpeg",
        )
        response = self.client.post(reverse("profiles:profile_edit"), {"bio": "Test bio", "avatar": large_file})

        # Ensure the message matches the form validation
        self.assertFormError(response.context["form"], "avatar", "Image is too large. The maximum size is 2MB.")

    def test_valid_profile_update(self):
        """Updating bio and names should work correctly."""
        self.client.login(username="user1", password="password123")
        response = self.client.post(
            reverse("profiles:profile_edit"), {"first_name": "NewName", "last_name": "NewLastName", "bio": "Updated bio"}
        )
        self.assertRedirects(response, reverse("profiles:profile_detail"))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "NewName")
        profile = UserProfile.objects.get(user=self.user1)
        self.assertEqual(profile.bio, "Updated bio")

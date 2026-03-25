from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)

    class Meta:
        model = UserProfile
        fields = ["bio", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, "user", None)
        if user:
            # Preload the first and last name from the user model
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name

    # avatar validation
    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            limit = 1024 * 1024 * 2  # 2MB
            if avatar.size > limit:
                raise ValidationError("Image is too large. The maximum size is 2MB.")

            extension = avatar.name.split(".")[-1].lower()
            if extension not in ["jpg", "jpeg", "png", "webp"]:
                raise ValidationError("Image must be a JPG, JPEG, PNG, or WEBP file")

        return avatar

    # save the profile and the user
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data["first_name"]
            user.last_name = self.cleaned_data["last_name"]
            user.save()
            profile.save()
        return profile

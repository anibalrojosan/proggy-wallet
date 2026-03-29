"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from wallet import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/guest-login/", views.guest_login, name="guest_login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("menu/", views.menu, name="menu"),
    path("deposit/", views.deposit, name="deposit"),
    path("transfer/", views.transfer, name="transfer"),
    path("history/", views.TransactionHistoryView.as_view(), name="history"),
    path("", lambda request: redirect("menu"), name="root_redirect"),
    path("profile/", include("profiles.urls", namespace="profiles")),
    path("reports/", include("reports.urls", namespace="reports")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""wifin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from wifi_app.views import *

urlpatterns = [
    path('',login_page, name="login"),
    path('landing/',LandingPageview.as_view(), name="landing-page"),
    path('index/',IndexPageview.as_view(), name="index-page"),
    path('index/interstitial/',InterstitialPageview.as_view(), name="interstitial-page"),
    path('index/interstitial/login_mahala',Login_mahalaPageview.as_view(), name="login_mahala-page"),
    path('admin/', admin.site.urls),
    path(
        "ads.txt",
        RedirectView.as_view(url=staticfiles_storage.url("ads.txt")),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

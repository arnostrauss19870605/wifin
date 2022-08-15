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
from django.contrib.sitemaps import GenericSitemap 
from django.contrib.sitemaps.views import sitemap 

from wifi_app.models import Post

info_dict = {
    'queryset': Post.objects.all(),
}

urlpatterns = [
    path('',login_page, name="login"),
    
    
    path('landing/<domain>/<domain_id>/',landing_page, name="landing-page"),
    path('landing/',landing_page_nop, name="landing-page-nop"),

    path('landing_1/<domain>/<domain_id>/',landing_page_1, name="landing-page-1"),
    path('landing_1/',landing_page_nop_1, name="landing-page-nop-1"),

    path('index/<domain>/<domain_id>/',index, name="index-page"),
    path('index/',index_nop, name="index-page-nop"),
    
    path('test/',test, name="test-page"),
    
    path('interstitial/<domain>/<domain_id>/',interstitial, name="interstitial-page"),
    path('interstitial/',interstitial_nop, name="interstitial-page-nop"),

    path('interstitial_1/<domain>/<domain_id>/',interstitial_1, name="interstitial-page-1"),
    path('interstitial_1/',interstitial_nop_1, name="interstitial-page-nop-1"),

    path('index/interstitial/login_mahala',Login_mahalaPageview.as_view(), name="login_mahala-page"),
    path('admin/', admin.site.urls),
    path(
        "ads.txt",
        RedirectView.as_view(url=staticfiles_storage.url("ads.txt")),
    ),
    path('markdownx/', include('markdownx.urls')),
    path('post/<slug>/', post, name = 'post'),
    path('about/', about,name = 'about' ),
    path('posts/', allposts, name = 'allposts'),

    path('sitemap.xml', sitemap, # new
        {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.65)}},
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

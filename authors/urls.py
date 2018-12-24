"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from .pages.general import GeneralRoutes

# produce a schema view
schema_view = get_swagger_view(title='Authors Haven Code Titans API')

urlpatterns = [
    path('', schema_view, name="main-view"),
    path('admin/', admin.site.urls),
    path('api/', include('authors.apps.authentication.urls')),
    path('api/', include('authors.apps.followers.urls')),
    path('api/', include('authors.apps.profiles.urls')),
    path('api/', include('authors.apps.articles.urls')),
    path('api/', include('authors.apps.likedislike.urls')),
    path('api/', include('authors.apps.read_stats.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('home', GeneralRoutes.home, name="home"),
    path('privacy', GeneralRoutes.privacy, name="privacy"),
]

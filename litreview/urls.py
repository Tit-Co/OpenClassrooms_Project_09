"""
URL configuration for litreview project.

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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include

from core import views as core_views
from accounts import views as accounts_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', core_views.index, name='index'),
    path('log_in/', accounts_views.log_in, name='log-in'),
    path('sign_up/', accounts_views.sign_up, name='sign-up'),
    path('feed/', include('feed.urls')),
    path('log_out/', accounts_views.log_out, name='log-out'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
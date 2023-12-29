"""
URL configuration for djangoMart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from .import views
from django.conf.urls.static import static #This 2 files import for media files
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('store/', include('store.urls')),
    path('order/', include('orders.urls')),
    # path('category/', include('category.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# We bonding our media file url link with the main url 
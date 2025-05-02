"""
URL configuration for my_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings # Ayarları import et
from django.conf.urls.static import static

import products # Statik/Medya dosyaları için

urlpatterns = [
    path('admin/', admin.site.urls),
    # accounts uygulamasının URL'lerini 'accounts/' altında arayacak:
    path('accounts/', include('accounts.urls')),

    # cart uygulamasının URL'lerini 'cart/' altında arayacak:
    path('cart/', include('cart.urls')),

    # products uygulamasının URL'lerini ana dizinde ('/') arayacak:
    path('', include('products.urls')),

    path('', include('django.contrib.auth.urls')), # Giriş, çıkış ve şifre sıfırlama için hazır URL'ler
]

# Sadece Geliştirme(DEBUG=True) modunda medya dosyalarını sunmak için:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
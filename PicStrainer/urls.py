"""
URL configuration for PicStrainer project.

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
from django.urls import path, include
from pic import views as picViews
from Docs import views as DocViews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',picViews.upload_image, name= 'home'),
    path('',picViews.Start),
    path('upload/', picViews.upload_image, name='upload_image'),
    path('visualization/', picViews.Show_Images, name="Show_Images"),
    path('', picViews.Return_Home, name='Return_Home'),
    path('accounts/', include('accounts.urls')),
    path('Docs/', DocViews.upload_doc, name='upload_doc'),
    path('VisualDocs/', DocViews.Show_Docs, name='Show_Docs'),
    path('Docs/', DocViews.GoDocs, name='Go_Docs'),
    path('visualization/<path:imagen_url>/', picViews.imagen_detalle_generica, name='detalle_imagen_generica'),
    path('super_resolution/', picViews.super_resolution, name='super_resolution')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


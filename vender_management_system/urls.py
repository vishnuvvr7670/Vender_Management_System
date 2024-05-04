"""
URL configuration for vender_management_system project.

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
from venders.views import *
from rest_framework.routers import DefaultRouter
DRO=DefaultRouter()
DRO.register('VenderModelViewSet',VenderModelViewSet,basename='VenderModelViewSet')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('venders/',include(DRO.urls)),
    path('get_vender_performance/',get_vender_performance,name='get_vender_performance'),
    path('acknowledge_purchase_order/',acknowledge_purchase_order,name='acknowledge_purchase_order'),
]

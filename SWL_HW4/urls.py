"""SWL_HW4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from account.views import update_client_profile, create_client, get_client_profile, update_admin_profile, \
    get_admin_profile, login_account, GatewayAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gateway-api', GatewayAPI.as_view({'post': 'list'}), name='gateway-api'),
    path('api/client-register', create_client, name='client-register'),
    path('api/login', login_account, name='login'),
    path('api/client-profile-view', get_client_profile, name='client-profile-view'),
    path('api/client-profile-update', update_client_profile, name='client-profile-update'),
    path('api/admin-profile-view', get_admin_profile, name='admin-profile-view'),
    path('api/admin-profile-update', update_admin_profile, name='admin-profile-update'),
]

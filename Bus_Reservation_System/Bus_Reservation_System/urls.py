"""Bus_Reservation_System URL Configuration

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
from macpath import basename
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from Bus import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


routers = DefaultRouter()
routers.register("buses",views.BusView,basename="buses")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token',obtain_auth_token),
    path('api/v1/user/register',views.UserRegistrationView.as_view()),
    path('api/v1/user/login',views.UserLoginView.as_view()),
    path('booking/',views.BookingView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/booking/<int:id>',views.BookingView.as_view()),
   


] + routers.urls

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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/register',views.UserRegistrationView.as_view()),
    path('api/v1/user/<int:id>',views.UserDetailView.as_view()),
    path('api/buses',views.BusView.as_view()),
    path('api/buses/<int:id>',views.BusDetailsView.as_view()),
    path('api/booking/',views.BookingView.as_view()),
    path('api/booking/<int:id>',views.ReservationDetailView.as_view()),
    path('api/buslists',views.BusSearchView.as_view()),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

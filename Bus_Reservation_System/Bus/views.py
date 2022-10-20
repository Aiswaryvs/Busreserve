import email
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Bus import serializers
from Bus.models import BusList, Reservation
from Bus.serializers import BusSerializer, UserRegistrationSerializer, BookingSerializer, UserLoginSerializer
from rest_framework import permissions, authentication
from django.contrib.auth import authenticate
from .tasks import *

# Create your views here.
"""view for CRED operations of Buses"""
class BusView(viewsets.ModelViewSet):
    serializer_class = BusSerializer
    queryset = BusList.objects.all()
    model = BusList
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

"""view for User registration"""
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg:Registration Successfull'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""view for User Login"""
class UserLoginView(APIView):
     def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(request,email=email,password=password)
            if user is not None:
                return Response({'msg:Login Successfull'},
                status=status.HTTP_200_OK)
            else:
                return Response({"msg": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST)
       




"""get: for listing reservations
   post: for reservation"""
class BookingView(APIView):
    serializer_class = BookingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            all_reservation = Reservation.objects.all()
            serializer = self.serializer_class(all_reservation, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("\nException Occured", error)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        # email=request.user.email
        id = request.data["user"]
        user_email = User.objects.get(id=id)
        email = user_email.email
        print(request.user)
        if serializer.is_valid():
            serializer.save()
            send_mail_task.delay(email)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    
    
   
               

# def index(request):
#     send_mail_task.delay()
#     return HttpResponse("hello")



# class PriceView(viewsets.ModelViewSet):
#     serializer_class = PriceSerializer
#     queryset = Price.objects.all()
#     model = Price
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]



    

    
    



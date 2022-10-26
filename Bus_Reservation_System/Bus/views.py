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
        bus_id = request.data["bus"]
        seats = BusList.objects.get(id=bus_id)
        bus_name = seats.bus_name
        place = seats.from_place
        to = seats.to
        date = request.data["reservation_date"]
        id = request.data["user"]
        user_email = User.objects.get(id=id)
        email = user_email.email
        if seats.available_seats<=seats.total_seats and seats.available_seats!=0:
            if serializer.is_valid():
                serializer.save()
                seat_no = (seats.total_seats-seats.available_seats)+1
                seats.available_seats = seats.available_seats-1
                print(seats.available_seats)
                msg = 'Your Booking for Bus' '\t' f"{bus_name} from {place} to {to} on date {date} was successfully Reserved. Your SeatNo:{seat_no}"
                print(msg)
                seats.save()
                send_mail_task.delay(email,msg)
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
        else:
            return Response({"msg": "Seats are unavailable"})

    
   
    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        bus_id = request.data["bus"]
        seat = BusList.objects.get(id=bus_id)
        instance = Reservation.objects.get(id=id)
        bus_name = seat.bus_name
        place = seat.from_place
        to = seat.to
        date = request.data["reservation_date"]
        serializer = self.serializer_class(data=request.data, instance=instance)
        id = request.data["user"]
        user_email = User.objects.get(id=id)
        email = user_email.email
        if serializer.is_valid():
            status = serializer.validated_data.get("status")
            serializer.save()
            if status=="cancel":
                seat.available_seats = seat.available_seats+1
                msg1 = 'Your Booking for Bus' '\t' f"{bus_name} from {place} to {to} on date {date} has been cancelled."
                print(seat.available_seats)
                seat.save()
                send_mail_cancel_task.delay(email,msg1)
                return Response(data=serializer.data)
            else:
                seat.available_seats = seat.available_seats-1
                seat.save()
        else:
            return Response(data=serializer.errors)     


import email
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Bus.models import BusList, Reservation
from Bus.serializers import *
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

    def get(self, request, *args, **kwargs):
        try:
            all_user = User.objects.all()
            serializer = self.serializer_class(all_user, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        except Exception as error:
            print("\nException Occured", error)

    def post(self,request,format=None):    
        response={"status":status.HTTP_400_BAD_REQUEST,"message":"User Creation Failed"}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            response["status"] = status.HTTP_201_CREATED
            response["message"] = "Registration Successfull"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class UserDetailView(APIView):
    serializer_class = UserRegistrationSerializer
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        user = User.objects.get(id=id)
        serializer =self.serializer_class(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        instance = User.objects.get(id=id)
        response={"status":status.HTTP_400_BAD_REQUEST,"message":"User Details Updation Failed"}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response["status"]=status.HTTP_200_OK
            response["message"]="Updation Successfull"
            response["data"]=serializer.data
            name = serializer.validated_data.get("name")
            email = serializer.validated_data.get("email")
            instance.name = name
            instance.email = email
            instance.save()
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,*args,**kwargs):
        response = {"status":status.HTTP_400_BAD_REQUEST,"message":"User Deletion Failed"}
        id = kwargs.get("id")
        user = User.objects.get(id=id)
        user.delete()
        response["message"] = "user Details Are Removed"
        response["status"] = status.HTTP_200_OK
        return Response(response,status=status.HTTP_200_OK)



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
        try:
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
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Bus Reservation Failed"}
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
                    response["status"] = status.HTTP_201_CREATED
                    response["message"] = "Reservation Successfull"
                    response["data"] = serializer.data
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
            else:
                return Response({"msg": "Seats are unavailable"})

        except Exception as error:
            print("\nException Occured", error)
    
class ReservationDetailView(APIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        reservation = Reservation.objects.get(id=id)
        serializer = self.serializer_class(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def put(self,request,*args,**kwargs):
        try:
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
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"User Details Updation Failed"}
            if seat.available_seats<=seat.total_seats and seat.available_seats!=0:
                if serializer.is_valid():
                    status = serializer.validated_data.get("status")
                    serializer.save()
                    if status=="cancel":
                        seat.available_seats = seat.available_seats+1
                        msg1 = 'Your Booking for Bus' '\t' f"{bus_name} from {place} to {to} on date {date} has been cancelled."
                        seat.save()
                        send_mail_cancel_task.delay(email,msg1)
                        response["status"] = status.HTTP_200_OK
                        response["message"] = "Reservation Updation Successfull"
                        response["data"] = serializer.data
                        return Response(response,status=status.HTTP_200_OK)
                    elif status=="booked":
                        seat.available_seats = seat.available_seats-1
                        seat.save()
                        seat_no = (seat.total_seats-seat.available_seats)+1
                        msg = 'Your Booking for Bus' '\t' f"{bus_name} from {place} to {to} on date {date} was successfully Reserved. Your SeatNo:{seat_no}"
                        send_mail_task.delay(email,msg)
                        return Response(data=serializer.data)
                else:
                    return Response(data=serializer.errors)  
            else:
                return Response({"msg": "Seats are unavailable"})
            
        except Exception as error:
                print("\nException Occured", error)


    def delete(self,request,*args,**kwargs):
        response = {"status":status.HTTP_400_BAD_REQUEST,"message":"Reservation Deletion Failed"}
        id = kwargs.get("id")
        reservation = Reservation.objects.get(id=id)
        reservation.delete()
        response["message"] = "Reservation Details Are Removed"
        response["status"] = status.HTTP_200_OK
        return Response(response,status=status.HTTP_200_OK)



class BusSearchView(APIView):
    serializer_class = BusSearchSerializer
    
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(request.data)
        source = request.data["from_place"]
        destination = request.data["to"]
        buslists = BusList.objects.filter(from_place=source,to=destination)
        print(buslists)



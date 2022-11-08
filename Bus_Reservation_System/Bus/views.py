import email
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Bus.models import BusList, Reservation
from Bus.serializers import *
import os,sys
from rest_framework import permissions
from .tasks import *
import logging
# logger = logging.getLogger('django')
db_logger = logging.getLogger('django')



# Create your views here.
"""
get : listing of buses
post : creation of bus """
class BusView(APIView):
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Fetching Buses Details are  Failed"}
            all_buses = BusList.objects.all()
            serializer = self.serializer_class(all_buses, many=True)
            response["status"] = status.HTTP_200_OK
            response["message"] = " Buses Details fetched successfully"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

    def post(self,request,format=None):    
        response={"status":status.HTTP_400_BAD_REQUEST,"message":"Bus Creation Failed"}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            response["status"] = status.HTTP_201_CREATED
            response["message"] = "Bus Creation Successfull"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
"""
get : get the details of specific bus
put : update details of specific bus
delete : delete specific bus """
class BusDetailsView(APIView):
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,**kwargs):
        try:
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Bus with this Id is not Exist"}
            id = kwargs.get("id")
            bus = BusList.objects.get(id=id)
            serializer =self.serializer_class(bus)
            response["status"] = status.HTTP_200_OK
            response["message"] = " Bus Details fetched successfully"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   

    def put(self,request,**kwargs):
            try:
                id = kwargs.get("id")
                instance = BusList.objects.get(id=id)
                response={"status":status.HTTP_400_BAD_REQUEST,"message":"Bus Details Updation Failed"}
                serializer = self.serializer_class(data=request.data, instance=instance)
                if serializer.is_valid():
                    serializer.save()
                    response["status"]=status.HTTP_200_OK
                    response["message"]="Updation Successfull"
                    response["data"]=serializer.data
                    return Response(response, status=status.HTTP_200_OK)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        try:
            response = {"status":status.HTTP_400_BAD_REQUEST,"message":"Bus Deletion Failed"}
            id = kwargs.get("id")
            bus = BusList.objects.get(id=id)
            bus.delete()
            response["message"] = "Bus Details Are Removed"
            response["status"] = status.HTTP_200_OK
            return Response(response,status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

            


"""
    get: list users
    post: User registration"""
class UserRegistrationView(APIView):

    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        try:
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Fetching Users Details are  Failed"}
            all_user = User.objects.all()
            serializer = self.serializer_class(all_user, many=True)
            response["status"] = status.HTTP_200_OK
            response["message"] = " Users Details fetched successfully"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

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


"""
 get: get details of the specific user
 put : update  specific user details
 delete : deletion of specific user"""
class UserDetailView(APIView):
    serializer_class = UserRegistrationSerializer
    def get(self,request,**kwargs):
        try:
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"User with this Id is not Exist"}
            id = kwargs.get("id")
            user = User.objects.get(id=id)
            serializer =self.serializer_class(user)
            response["status"] = status.HTTP_200_OK
            response["message"] = " User Details fetched successfully"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)       

    def put(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            instance = User.objects.get(id=id)

            response={"status":status.HTTP_400_BAD_REQUEST,"message":"User Details Updation Failed"}
            serializer = self.serializer_class(data=request.data, instance=instance)
            if serializer.is_valid():
                name = serializer.validated_data.get("name")
                email = serializer.validated_data.get("email")
                password = serializer.validated_data.get("password")
                instance.name = name
                instance.email = email
                instance.set_password(password)
                instance.save()
                response["status"]=status.HTTP_200_OK
                response["message"]="Updation Successfull"
                response["data"]=serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,*args,**kwargs):
        try:
            response = {"status":status.HTTP_400_BAD_REQUEST,"message":"User Deletion Failed"}
            id = kwargs.get("id")
            user = User.objects.get(id=id)
            user.delete()
            response["message"] = "user Details Are Removed"
            response["status"] = status.HTTP_200_OK
            return Response(response,status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)       



"""get: for listing reservations
   post: for reservation"""
class BookingView(APIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Fetching Reservation Lists are failed"}
            all_reservation = Reservation.objects.all()
            serializer = self.serializer_class(all_reservation, many=True)
            response["status"] = status.HTTP_200_OK
            response["message"] = "fetching Reservation Details is Successful"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST) 
        

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
                    msg = f"Your Booking for Bus {bus_name} from {place} to {to} on date {date} was successfully Reserved. Your SeatNo:{seat_no}"
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

        except Exception:
           return Response(response, status=status.HTTP_400_BAD_REQUEST)

"""
  get: for getting the reservation with specific ID
  put: for cancel the reservation
  delete : for deleting the reservation details of the reservation with specific id"""  
class ReservationDetailView(APIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        try:
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Reservation with this Id is not Exist"}
            id = kwargs.get("id")
            reservation = Reservation.objects.get(id=id)
            serializer = self.serializer_class(reservation)
            response["status"] = status.HTTP_200_OK
            response["message"] = "fetching Reservation Details is Successful"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST) 

    
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
            if serializer.is_valid():
                status = serializer.validated_data.get("status")
                instance.status = status
                instance.save()
                if status=="cancel":
                    seat.available_seats = seat.available_seats+1
                    msg1 = f"Your Booking for Bus {bus_name} from {place} to {to} on date {date} has been cancelled."
                    seat.save()
                    send_mail_cancel_task.delay(email,msg1)
                    return Response(data=serializer.data)
                else:
                    return Response({"cancellation of Bus Reservation Failed"}) 
            else:
                return Response({"cancellation of Bus Reservation Failed"}) 
            
        except Exception :
            return Response({"cancellation of Bus Reservation Failed"}) 


    def delete(self,request,*args,**kwargs):
        try:
            response = {"status":status.HTTP_400_BAD_REQUEST,"message":"Reservation Deletion Failed"}
            id = kwargs.get("id")
            reservation = Reservation.objects.get(id=id)
            reservation.delete()
            response["message"] = "Reservation Details Are Removed"
            response["status"] = status.HTTP_200_OK
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            return Response(response, status=status.HTTP_400_BAD_REQUEST) 



"""
for searching of buses with particular source and destination """
class BusSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "Buses are not available"}
        source = request.data["from_place"]
        destination = request.data["to"]
        buslists = BusList.objects.filter(from_place__icontains=source, to__icontains=destination)
        bus_list = []
        for bus in buslists:
            buslst=bus.bus_name
            bus_list.append(buslst)
            response["status"] = status.HTTP_200_OK
            response["data"] = bus_list
            response["message"] = 'Buses are Available'
        return Response(response, status=status.HTTP_200_OK)


                
        
                    
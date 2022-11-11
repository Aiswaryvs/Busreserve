from django.shortcuts import render
from rest_framework import viewsets
from demofile.serializers import ProfileSerializer
from demofile.models import *
from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from demofile.serializers import EmployeeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
# Create your views here.

class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    model= Profile


class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class =  EmployeeSerializer
    lookup_field = "id"

class EmployeeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class =  EmployeeSerializer
    lookup_field = "id"

class EmployeeListView(ListModelMixin,GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class =  EmployeeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class =  EmployeeSerializer

    def create(self, request, *args, **kwargs):
        response={"status":status.HTTP_400_BAD_REQUEST,"message":"creation Failed"}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response["status"] = status.HTTP_200_OK
        response["message"] = " Created successfully"
        response["data"] = serializer.data
        return Response(response, status=status.HTTP_201_CREATED)

class FilterView(APIView):
    def post(self,request,*args,**kwargs):
        response = {'status':status.HTTP_400_BAD_REQUEST, 'message': "data  not available"}
        # from_age = request.data["from"]
        # to_age =request.data["to"]
        date = request.data["j_date"]
        # emp_lists = Employee.objects.filter(age__range=[from_age,to_age] ,j_date=date)
        emp_lists =Employee.objects.filter(j_date__year__lte=2022)
        list = []
        for emp in emp_lists:
            emplst=emp.name
            emplst=emp.experience
            list.append(emplst)
            response["status"] = status.HTTP_200_OK
            response["data"] = list
            response["message"] = 'Available Data'
        return Response(response, status=status.HTTP_200_OK)


                


from pyexpat import model
from rest_framework import serializers
from Bus.models import BusList, Reservation, User


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusList
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name","email","password"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class BookingSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Reservation
        fields = ["bus","user","current_date","reservation_date","status"]

  






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
    # bus=BusSerializer(many=False,read_only=True)
    # user=serializers.CharField(read_only=True)
    class Meta:
        model=Reservation
        fields=["bus","user","current_date","reservation_date","status"]

    # def create(self,validated_data):
    #     # user=self.context.get("user")
    #     # bus=self.context.get("bus")
    #     return Reservation.objects.create(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email','password']





# class PriceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Price
#         fields = "__all__"

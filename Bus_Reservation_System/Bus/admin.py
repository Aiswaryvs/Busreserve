from django.contrib import admin
from Bus.models import BusList, User, Reservation

# Register your models here.

admin.site.register(Reservation)
admin.site.register(BusList)
admin.site.register(User)
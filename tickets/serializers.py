from rest_framework import serializers
from .models import *

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk','reservation', 'name', 'mobile']
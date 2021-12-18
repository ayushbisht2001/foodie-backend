from django.db.models import fields
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings
from .models import *

class CuisinesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Cuisines
        fields = "__all__"

class AddressSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = "__all__"


class RestaurantSerializers(serializers.ModelSerializer):  
    
    cuisines = CuisinesSerializers(many = True)
    address = AddressSerializers(many=False)
    class Meta:
        model = Restaurant
        fields = "__all__"
        
    def save(self):     
        restaurant = Restaurant(**self.validated_data )
        restaurant.save()
        return restaurant
        



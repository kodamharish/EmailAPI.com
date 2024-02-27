from rest_framework.serializers import ModelSerializer
from .models import *

from rest_framework import serializers
import json



    
class JSONDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)



class EmailSerializer(serializers.Serializer):
    to_email = serializers.EmailField()
    subject=serializers.CharField()
    message=serializers.CharField()
    api = serializers.URLField(required=False) #Validates that the provided data is a URL
    jsondata = serializers.ListField(required=False,child=JSONDataSerializer())


    
    





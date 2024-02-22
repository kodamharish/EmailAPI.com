from rest_framework.serializers import ModelSerializer
from .models import *
from django.core.mail import send_mail
from rest_framework import serializers


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model= Employee
        fields='__all__'
    
    

class EmailSerializer(serializers.Serializer):
    to_email = serializers.EmailField()
    subject=serializers.CharField()
    message=serializers.CharField()
    api = serializers.CharField(required=False)
    #file=serializers.FileField()
    #file = serializers.FileField(required=False)
    #files = serializers.ListField(child=serializers.FileField(), required=False)

    




#payload
# {
#     "name": "Harish",
#     "email": "kodam846@gmail.com",
#     "subject": "Hello",
#     "message": "Test message"
# }
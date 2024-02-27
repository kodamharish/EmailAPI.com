from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmailSerializer
from .models import *
import os
from openpyxl import load_workbook, Workbook
from django.core.mail import EmailMessage
from project1.settings import BASE_DIR
#import xlsxwriter
from django.conf import settings
import pandas as pd
import requests
import json

# Create your views here.

def index(request):
    employee=Employee.objects.all()
    context={'Emp':employee}
    return render(request,'index.html',context)

class FormDataSendEmail(APIView):
    def post(self, request):
        # Check the content type of the request
        if 'application/json' in request.content_type:
            serializer = EmailSerializer(data=request.data)
        else:
            serializer = EmailSerializer(data=request.data)
        #serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            files = request.FILES.getlist('files')  # Get list of files
            email = EmailMessage(
                subject=subject,
                body=message,
                to=[to_email],
            )
            # Attach multiple files if provided
            for file in files:
                email.attach(file.name, file.read(), file.content_type)
            # Send the email
            email.send(fail_silently=False)  # Ensure errors are not silently ignored
            return Response({'message': 'Email sent successfully'}, status=200)
        else:
            return Response(serializer.errors, status=400)

class APISendMail(APIView):
    def post(self, request):
        # Check the content type of the request
        if 'application/json' in request.content_type:
            serializer = EmailSerializer(data=request.data)
        else:
            serializer = EmailSerializer(data=request.data)
            return Response({'error': 'Content type must be application/json'}, status=400)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            emp_api_url = serializer.validated_data['api']  # Get API URL if provided

            if emp_api_url:  # Check if API URL is provided
                # Fetch data from EMP API
                response = requests.get(emp_api_url)
                if response.status_code == 200:
                    emp_data = response.json()
                    # Convert JSON data to pandas DataFrame
                    df = pd.DataFrame(emp_data)
                    # Create a writer object for Excel
                    save_path = os.path.join(settings.BASE_DIR, 'static', 'Data', 'API_Data.xlsx')
                    writer = pd.ExcelWriter(save_path, engine='xlsxwriter')
                    df.to_excel(writer, index=False, sheet_name='API_Data')
                    # Close the ExcelWriter (this should automatically save the Excel file)
                    writer.close()
                    email = EmailMessage(
                        subject=subject,
                        body=message,
                        to=[to_email],
                    )
                    static_files_folder = os.path.join(BASE_DIR, 'static', 'Data')
                    # Iterate through files in the folder and attach Excel files
                    for file_name in os.listdir(static_files_folder):
                        if file_name.endswith('.xlsx'):
                            file_path = os.path.join(static_files_folder, file_name)
                            with open(file_path, 'rb') as file:
                                file_data = file.read()
                            email.attach(file_name, file_data)

                    email.send(fail_silently=False)
                    # Email the Excel file
                    return Response({'message': 'Excel file generated and emailed successfully!'})
                else:
                    return Response({'error': 'Failed to fetch data from EMP API'}, status=500)
            else:
                return Response({'error': 'API URL not provided'}, status=400)
        else:
            #return Response({'error': 'Invalid data provided'})
            return Response(serializer.errors, status=400)

class JSONDataSendMail(APIView):
    def post(self, request):
        # Check the content type of the request
        if 'application/json' in request.content_type:
            serializer = EmailSerializer(data=request.data)
        else:
            return Response({'error': 'Content type must be application/json'}, status=400)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            jsondata = serializer.validated_data['jsondata']
            # Convert JSON data to pandas DataFrame
            df = pd.DataFrame(jsondata)
            # Create a writer object for Excel
            save_path = os.path.join(settings.BASE_DIR, 'static', 'Data', 'JSON_Data.xlsx')
            writer = pd.ExcelWriter(save_path, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='JSON_Data')
            # Close the ExcelWriter (this should automatically save the Excel file)
            writer.close()
            email = EmailMessage(
                subject=subject,
                body=message,
                to=[to_email],
            )
            static_files_folder = os.path.join(settings.BASE_DIR, 'static', 'Data')
            # Iterate through files in the folder and attach Excel files
            for file_name in os.listdir(static_files_folder):
                if file_name.endswith('JSON_Data.xlsx'):
                    file_path = os.path.join(static_files_folder, file_name)
                    with open(file_path, 'rb') as file:
                        file_data = file.read()
                    email.attach(file_name, file_data)
            email.send(fail_silently=False)
            # Email the Excel file
            return Response({'message': 'Excel file generated and emailed successfully!'})
        else:
            return Response(serializer.errors, status=400)


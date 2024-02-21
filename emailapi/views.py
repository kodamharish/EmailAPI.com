from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from .serializers import EmailSerializer
from .models import *

import os
from openpyxl import load_workbook, Workbook
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmailSerializer
from django.core.mail import EmailMessage
from project1.settings import BASE_DIR
import os
import xlsxwriter
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmailSerializer
from django.core.mail import EmailMessage
from django.conf import settings



# Create your views here.

class DupSendEmail(APIView):
    def post(self, request):
        # Check the content type of the request
        if 'application/json' in request.content_type:
            serializer = EmailSerializer(data=request.data)
        else:
            serializer = EmailSerializer(data=request.data)

        # Validate the serializer
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            #file = serializer.validated_data.get('file')  # Use get() to handle None if file is not provided
            #file = request.FILES.get('file')
            files = request.FILES.getlist('files')  # Get list of files

            # Create EmailMessage instance
            email = EmailMessage(
                subject=subject,
                body=message,
                to=[to_email],
            )

            # Attach the file if provided
            #if file:
                #email.attach(file.name, file.read(), file.content_type)

            # Attach multiple files if provided
            for file in files:
                email.attach(file.name, file.read(), file.content_type)

            # Send the email
            #email.send()
            # Send the email
            email.send(fail_silently=False)  # Ensure errors are not silently ignored


            return Response({'message': 'Email sent successfully'}, status=200)
        else:
            
            return Response(serializer.errors, status=400)
        



class SendEmail(APIView):
    def post(self, request):
        # Check the content type of the request
        if 'application/json' in request.content_type:
            serializer = EmailSerializer(data=request.data)
        else:
            serializer = EmailSerializer(data=request.data)

        #serializer = EmailSerializer(data=request.data)
        save_path = os.path.join(BASE_DIR, 'static', 'files', 'Employee.xlsx')
        # Retrieve the existing employee IDs from the Excel file, if it exists
        existing_employee_ids = set()
        if os.path.exists(save_path):
            workbook = load_workbook(filename=save_path)
            worksheet = workbook.active
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                existing_employee_ids.add(row[0])  # Assuming employee ID is in the first column
                #print(existing_employee_ids)
        # Retrieve all employees
        employees = Employee.objects.all()

        # Filter out employees whose IDs are already written to the Excel file
        new_employees = [emp for emp in employees if emp.id not in existing_employee_ids]

        # Open the Excel file or create a new workbook if it doesn't exist
        if os.path.exists(save_path):
            workbook = load_workbook(filename=save_path)
        else:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = 'Employee Data'
            worksheet.append(['ID', 'Name', 'Email', 'Address', 'Phone Number'])

        # Write new employee data to the worksheet
        worksheet = workbook.active
        for emp in new_employees:
            worksheet.append([emp.id, emp.name, emp.email, emp.address, emp.phoneno])

        # Save the workbook
        workbook.save(save_path)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            #static_files_folder = os.path.join(settings.STATIC_ROOT, 'files')
            static_files_folder = os.path.join(BASE_DIR, 'static', 'files')


            email = EmailMessage(
                subject=subject,
                body=message,
                to=[to_email],
            )

            # Iterate through files in the folder and attach Excel files
            for file_name in os.listdir(static_files_folder):
                if file_name.endswith('.xlsx'):
                    file_path = os.path.join(static_files_folder, file_name)
                    with open(file_path, 'rb') as file:
                        file_data = file.read()
                    email.attach(file_name, file_data)

            email.send(fail_silently=False)

            return Response({'message': 'Email sent successfully'}, status=200)
        else:
            return Response(serializer.errors, status=400)





def index(request):
    employee=Employee.objects.all()
    context={'Emp':employee}
    return render(request,'index.html',context)





# def generate_excel(request):
#     # Define the path to the Excel file
#     save_path = os.path.join(BASE_DIR, 'static', 'files', 'Employee.xlsx')

#     # Retrieve the existing employee IDs from the Excel file, if it exists
#     existing_employee_ids = set()
#     if os.path.exists(save_path):
#         workbook = load_workbook(filename=save_path)
#         worksheet = workbook.active
#         for row in worksheet.iter_rows(min_row=2, values_only=True):
#             existing_employee_ids.add(row[0])  # Assuming employee ID is in the first column
#             print(existing_employee_ids)

#     # Retrieve all employees
#     employees = Employee.objects.all()

#     # Filter out employees whose IDs are already written to the Excel file
#     new_employees = [emp for emp in employees if emp.id not in existing_employee_ids]

#     # If there are no new employees, return a response indicating no updates
#     if not new_employees:
#         return HttpResponse("No new employee data to update.")

#     # Open the Excel file or create a new workbook if it doesn't exist
#     if os.path.exists(save_path):
#         workbook = load_workbook(filename=save_path)
#     else:
#         workbook = Workbook()
#         worksheet = workbook.active
#         worksheet.title = 'Employee Data'
#         worksheet.append(['ID', 'Name', 'Email', 'Address', 'Phone Number'])

#     # Write new employee data to the worksheet
#     worksheet = workbook.active
#     for emp in new_employees:
#         worksheet.append([emp.id, emp.name, emp.email, emp.address, emp.phoneno])

#     # Save the workbook
#     workbook.save(save_path)

#     return HttpResponse("Excel sheet updated successfully.")


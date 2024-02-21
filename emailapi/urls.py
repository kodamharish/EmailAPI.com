from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('send_email',SendEmail.as_view(), name='send_email'),
    #path('genexcel',generate_excel,name='gen'),
    path('export/', ExportExcelAPIView.as_view(), name='export-excel-view'),
    
]

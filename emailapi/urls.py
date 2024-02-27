from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('form_data_send_mail',FormDataSendEmail.as_view(), name='form_data_send_mail'),
    path('api_send_mail',APISendMail.as_view(), name='api_send_mail'),
    path('json_data_send_mail',JSONDataSendMail.as_view(), name='json_data_send_mail'),

    
]

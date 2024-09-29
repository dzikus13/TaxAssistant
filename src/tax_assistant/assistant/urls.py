from django.urls import path
from . import views

urlpatterns = [
    path('process_input/', views.process_input),
    path('get_us_code/', views.get_us_code),
    path('get_xml/', views.get_xml),
]


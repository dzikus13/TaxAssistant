from django.urls import path
from . import views

urlpatterns = [
    path('generate_xml/', views.process_input),
]


from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('process_input/', csrf_exempt(views.process_input)),
    path('get_us_code/', csrf_exempt(views.get_us_code)),
    path('get_xml/', csrf_exempt(views.get_xml)),
]


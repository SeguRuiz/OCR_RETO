from django.urls import path

from .views import hola_mundo

urlpatterns = [path("hola-mundo/", hola_mundo, name="hola-mundo")]

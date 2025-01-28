from django.urls import path

from .views import hola_mundo, procesar_archivo

urlpatterns = [
    path("hola-mundo/", hola_mundo, name="hola-mundo"),
    path("procesar-archivo/", procesar_archivo, name="procesar-archivo-url"),
]

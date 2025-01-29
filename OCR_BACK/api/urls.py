from django.urls import path

from .views import (
    ExtractFieldsByPageAPIView,
    GoogleVisionOCRAPIView,
    GoogleVisionOCRAPIViewPaginacion,
    OCRAPIView,
    hola_mundo
)

urlpatterns = [
    path("hola-mundo/", hola_mundo, name="hola-mundo"),
    path("procesar-archivo-gratis/", OCRAPIView.as_view(), name="procesar-archivo-url"),
    path(
        "procesar-archivo-paga/",
        GoogleVisionOCRAPIView.as_view(),
        name="procesar-archivo-paga-url",
    ),
    path(
        "procesar-archivo-paga-paginacion/",
        GoogleVisionOCRAPIViewPaginacion.as_view(),
        name="procesar-archivo-paga-paginacion-url",
    ),
    path(
        "procesar-archivo-paga-paginacion-opencv/",
        ExtractFieldsByPageAPIView.as_view(),
        name="procesar-archivo-paga-paginacion-opencv-url",
    ),
]

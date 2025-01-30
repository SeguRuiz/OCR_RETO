from django.urls import path

from .views import (
    UPLOADTODRIVE,
    ExtractFieldsByPageAPIView,
)

urlpatterns = [
    path(
        "procesar-archivo-paginacion/",
        ExtractFieldsByPageAPIView.as_view(),
        name="procesar-archivo-paga-paginacion-opencv-url",
    ),
    path(
        "subir-a-drive/",
        UPLOADTODRIVE.as_view(),
        name="subir-a-drive",
    ),
]

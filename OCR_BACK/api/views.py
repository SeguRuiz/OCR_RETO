from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ArchivoSerializer

# Create your views here.


@api_view(["GET"])
def hola_mundo(request):
    return Response({"mensaje": "hola mundo!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def procesar_archivo(request):
    serializer = ArchivoSerializer(data=request.data)

    if serializer.is_valid():
        return Response({"mensaje": "El archivo es valido"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

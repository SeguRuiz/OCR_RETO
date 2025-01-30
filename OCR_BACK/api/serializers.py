from rest_framework import serializers

class ArchivoSerializer(serializers.Serializer):
    archivo = serializers.FileField()

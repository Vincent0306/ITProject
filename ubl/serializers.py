from rest_framework import serializers

# Serializer for the json file upload
class FileUploadSerializer(serializers.Serializer):
    json_file = serializers.FileField()
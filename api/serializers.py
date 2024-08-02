from rest_framework import serializers

class TextSerializer(serializers.Serializer):
    user_project_initial_description = serializers.CharField(max_length=250_000)
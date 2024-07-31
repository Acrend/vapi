from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextSerializer
import random
import time

class RandomAnimalView(APIView):
    def get(self, request, format=None):
        animals = ['chien', 'chat', 'souris']
        return Response({"animal": random.choice(animals)})

class GetInfo(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            info = serializer.validated_data['info']
            return Response({"message": "Texte reçu avec succès !"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PromptRequest(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            parameters = serializer.validated_data['parameters']
            return Response({"message": "Texte reçu avec succès !"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
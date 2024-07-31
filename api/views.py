from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextSerializer
import random
import time

class RandomAnimalView(APIView):
    def get(self, request, format=None):
        animals = ['chien', 'chat', 'souris']
        return Response({"animal": random.choice(animals),"info":'This a simple test'})

class GetInfo(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            request = serializer.validated_data['request']
            info = serializer.validated_data['info']
            sub_check_number = 10 # this must be computed
            estimed_time = 50
            sub_id_list = ['1','2']
            response_container = {
                "sub_check_number":sub_check_number,
                "estimed_time":estimed_time,
                "sub_id_list":sub_id_list
                }
            return Response(response_container, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubRequest(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            sub_id = serializer.validated_data['sub_id']
            model_parameters = serializer.validated_data['model_parameters']
            if not model_parameters: #if no LLM parameters are given, the we set some by default
                model_parameters = {"temperature":0.2}
            # the prompt must be create here and we need to call the other api then
            return Response({"message": "Texte reçu avec succès !"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
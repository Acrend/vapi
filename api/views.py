from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextSerializer
from .load_data import dbm, load_db
import random
import time

class RandomAnimalView(APIView):
    def get(self, request, format=None):
        animals = ['chien', 'chat', 'souris']
        return Response({"animal": random.choice(animals),"info":'This a simple test'})

class GetInfo(APIView):
    def post(self, request, *args, **kwargs):
        # print(len(dbm.database))
        data = request.data
        serializer = TextSerializer(data=data)

        compute_time = 1 #in second
        if serializer.is_valid():
            sub_check_number = len(dbm.database) # this must be computed
            estimed_time = sub_check_number*compute_time
            sub_id_list = dbm.index_list
            response_container = {
                "user_project_initial_description" : data['user_project_initial_description'],
                "sub_check_number":sub_check_number,
                "estimed_time":estimed_time,
                "sub_id_list":sub_id_list
                }
            return Response(response_container, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubRequest(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = TextSerializer(data=data)
        if serializer.is_valid():
            sub_id = serializer.validated_data['sub_id']
            model_parameters = serializer.validated_data['model_parameters']
            if not model_parameters: #if no LLM parameters are given, the we set some by default
                model_parameters = {"temperature":0.2}
            # the prompt must be create here and we need to call the other api then
            return Response({"message": "Texte reçu avec succès !"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReloadDB(APIView):
    def post(self, request, *args, **kwargs):
        global dbm
        dbm = load_db()
        return Response({'message': 'Database reloaded successfully'}, status=status.HTTP_200_OK)
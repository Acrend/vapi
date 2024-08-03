from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from .serializers import TextSerializer
from .load_data import dbm, load_db
import random
import json
import requests
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
            sub_id = data['sub_id']
            url = config("OLLAMA_API_URL")
            project_description = data['user_project_initial_description']
            sub = dbm.format_sub(sub_id)
            prompt = f"*Aide ou subvention à analyser :*\n{sub}\n\n____\n*Projet de l'utilisateur :*\n{project_description}"
            data = {
                "model": "mistral-nemo:12b-instruct-2407-q4_0",
                "system":"""Tu aides l'utilistateur à determiner si les aides sont atribuables à un projet, tu répondera exclusivement par "OUI" ou "NON" Réponds uniquement au format JSON suivant {"response":"TA REPONSE"}""",
                "prompt": prompt,
                "format":"json",
                "stream": False,
                "options": {
                    "seed": 0,
                    "top_k": 20,
                    "top_p": 0.9,
                    "min_p": 0.0,
                    "temperature": 0.2,
                    "repeat_penalty": 1.2,
                    "presence_penalty": 1.5,
                    "frequency_penalty": 1.0,
                    "num_ctx": 2048*16
                    }
                    }
            headers = {'Content-Type': 'application/json'}
            try :
                response = requests.post(url, data=json.dumps(data), headers=headers)
                response = json.loads(response.json()['response'])
            except Exception as error:
                print(error)
                return Response({"message": "something went wrong"}, status=status.HTTP_201_CREATED)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReloadDB(APIView):
    def post(self, request, *args, **kwargs):
        global dbm
        dbm = load_db()
        return Response({'message': 'Database reloaded successfully'}, status=status.HTTP_200_OK)
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
        url = config("OLLAMA_API_URL")
        data = request.data
        
        prompt_system = """Tu aides l'utilisateur à déterminer la compatibilité de l'aide ou subvention à analyser par rapport à la description de son projet.
Réponds uniquement par un chiffre de 1 à 5.
- Attribue 5 si l'aide ou la subvention correspond parfaitement aux objectifs et aux besoins du projet. 
  - Les objectifs de l'aide/subvention sont totalement alignés avec les besoins du projet.
  - Les conditions et exigences de l'aide/subvention sont complètement satisfaites par le projet.
- Attribue 4 si l'aide ou la subvention correspond très bien aux objectifs et aux besoins du projet. 
  - Les objectifs de l'aide/subvention sont majoritairement alignés avec les besoins du projet.
  - La plupart des conditions et exigences de l'aide/subvention sont satisfaites par le projet.
- Attribue 3 si l'aide ou la subvention correspond partiellement aux objectifs et aux besoins du projet.
  - Les objectifs de l'aide/subvention sont partiellement alignés avec les besoins du projet.
  - Certaines conditions et exigences de l'aide/subvention sont satisfaites par le projet.
- Attribue 2 si l'aide ou la subvention a une correspondance minimale avec les objectifs et les besoins du projet.
  - Les objectifs de l'aide/subvention sont rarement alignés avec les besoins du projet.
  - Peu de conditions et exigences de l'aide/subvention sont satisfaites par le projet.
- Attribue 1 si la description du projet n'est pas suffisamment détaillée ou est trop vague, ou si l'aide ou la subvention n'a aucune correspondance avec les objectifs et les besoins du projet.
  - Les objectifs de l'aide/subvention ne sont pas du tout alignés avec les besoins du projet.
  - Aucune des conditions et exigences de l'aide/subvention n'est satisfaite par le projet.

Si un élément ou paragraphe spécifique de l'aide ou subvention semble correspondre aux besoins du projet, utilise cette information pour attribuer la note en conséquence.
Ne donne aucune explication, aucun autre mot ou phrase, juste un des chiffres indiqués ci-dessus.
Réponds exclusivement par un chiffre unique entre 1 et 5, sans aucun texte supplémentaire."""
        
        serializer = TextSerializer(data=data)
        subvention_score = 0
        if serializer.is_valid():
            sub_id = data['sub_id']
            project_description = data['user_project_initial_description']
            seed_number = data['seed_number']

            sub = dbm.format_sub(sub_id)

            prompt_user = f"*Aide ou subvention à analyser :*\n{sub}\n\n____\n*Projet de l'utilisateur :*\n{project_description}"
            headers = {'Content-Type': 'application/json'}
            for seed in range(seed_number):
                data = {
                    "model": "mistral-nemo:12b-instruct-2407-q8_0",
                    "system": prompt_system ,
                    "prompt": prompt_user,
                    "stream": False,
                    "options": {
                        "seed": seed,
                        "top_k": 20,
                        "top_p": 0.9,
                        "temperature": 0.2,
                        "repeat_penalty": 1.2,
                        "presence_penalty": 1.5,
                        "frequency_penalty": 1.0,
                        "num_ctx": 16384,
                        "num_predict":32
                        }
                        }
                try :
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                except Exception as error:
                    print('-----------------------------------------')
                    print('Sommething went wrong')
                    print(error)
                try :
                    subvention_score += int(response.json()['response'])
                except Exception as error:
                    print('-----------------------------------------')
                    print('llm awnser not with the excepted format')
                    print(response.json()['response'])
            response = {'subvention_score':subvention_score,'sub_title':dbm.database.loc[sub_id]['name']}
                    
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReloadDB(APIView):
    def post(self, request, *args, **kwargs):
        global dbm
        dbm = load_db()
        return Response({'message': 'Database reloaded successfully'}, status=status.HTTP_200_OK)
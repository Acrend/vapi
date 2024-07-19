from rest_framework.response import Response
from rest_framework.views import APIView

class AnimalsView(APIView):
    animals = ['chien', 'chat', 'souris']

    def get(self, request, index):
        try:
            # Convertit l'index en entier et retourne l'animal correspondant
            index = int(index)
            if index < len(self.animals):
                return Response({'animal': self.animals[index]})
            else:
                return Response({'error': 'Index out of range'}, status=404)
        except ValueError:
            return Response({'error': 'Invalid index'}, status=400)

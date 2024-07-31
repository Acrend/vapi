from django.urls import path
from .views import RandomAnimalView, GetInfo, SubRequest

urlpatterns = [
    path('animal/', RandomAnimalView.as_view(), name='random-animal'),
    path('get-info/', RandomAnimalView.as_view(), name='get-info'),
    path('prompt-request/', PromptRequest.as_view(), name='prompt-request')
]
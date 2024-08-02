from django.urls import path
from .views import RandomAnimalView, GetInfo, SubRequest,ReloadDB

urlpatterns = [
    path('animal/', RandomAnimalView.as_view(), name='random-animal'),
    path('get-info/', GetInfo.as_view(), name='get-info'),
    path('sub-request/', SubRequest.as_view(), name='sub-request'),
    path('reload-db/', ReloadDB.as_view(), name='reload-db')
]
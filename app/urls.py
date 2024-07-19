from django.urls import path
from .views import AnimalsView

urlpatterns = [
    path('animals/<int:index>/', AnimalsView.as_view(), name='animal-by-index'),
]
from django.urls import path
from .views import SimilarityAPIView

urlpatterns = [
    path('similarity/', SimilarityAPIView.as_view(), name='similarity'),
]

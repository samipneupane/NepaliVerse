from django.urls import path
from .views import SimilarityAPIView, TranslationAPIView

urlpatterns = [
    path('similarity/', SimilarityAPIView.as_view(), name='similarity'),
    path('translation/', TranslationAPIView.as_view(), name='translation'),
    path('core/translation/', TranslationAPIView.as_view(), name='translation'),
] 

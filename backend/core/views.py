from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SimilaritySerializer

from django.core.files.storage import default_storage
from django.conf import settings
import os

from logic.similarity.main import compare_speech_similarity


class SimilarityAPIView(CreateAPIView):
    serializer_class = SimilaritySerializer

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['input_text']
            audio_file = serializer.validated_data['audio']

            file_path = os.path.join(settings.MEDIA_ROOT, 'media', audio_file.name)
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            try:
                results = compare_speech_similarity(file_path, input_text)
                os.remove(file_path)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

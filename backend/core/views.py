from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SimilaritySerializer, TranslationSerializer

from django.core.files.storage import default_storage
from django.conf import settings
import os

from logic.similarity.main import compare_speech_similarity
from logic.translation.inference import en_ne_conversion, text_to_speech
from logic.unicode.englishToUnicode import translate_nepali_to_english
from logic.unicode.inference import predict_output

import base64
from io import BytesIO
import librosa

class SimilarityAPIView(CreateAPIView):
    serializer_class = SimilaritySerializer

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['input_text']
            audio_file = serializer.validated_data['audio']

            # file_path = os.path.join(settings.MEDIA_ROOT, 'media', audio_file.name)
            # os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            audio_data = BytesIO()
            for chunk in audio_file.chunks():
                audio_data.write(chunk)
            audio_data.seek(0)

            # with default_storage.open(file_path, 'wb+') as destination:
            #     for chunk in audio_file.chunks():
            #         destination.write(chunk)
            # audio, sr = librosa.load(file_path, sr=None)

            try:
                results = compare_speech_similarity(audio_data, input_text)
                # results = compare_speech_similarity(file_path, input_text)
                # os.remove(file_path)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class TranslationAPIView(CreateAPIView):
    serializer_class = TranslationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            input_text = serializer.validated_data['input_text']
            try:
                nepali_translation = en_ne_conversion(input_text)
                try:
                    base64_audio = text_to_speech(nepali_translation)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                # unicode_nepali = translate_nepali_to_english(nepali_translation)
                unicode_nepali = predict_output(nepali_translation)

                response_data = {
                    "nepali_translation": nepali_translation,
                    "unicode_nepali": unicode_nepali,
                    "audio_file": base64_audio
                    # request.build_absolute_uri(os.path.join(settings.MEDIA_URL, audio_synthetic))
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
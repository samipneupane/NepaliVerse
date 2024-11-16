from rest_framework import serializers

class SimilaritySerializer(serializers.Serializer):
    input_text = serializers.CharField(max_length=1000)
    audio = serializers.FileField()


class TranslationSerializer(serializers.Serializer):
    input_text = serializers.CharField(max_length=1000)
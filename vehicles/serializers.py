from rest_framework import serializers

class DummySerializer(serializers.Serializer):
    file = serializers.FileField()

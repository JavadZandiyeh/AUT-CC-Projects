from rest_framework import serializers


class LinkShortenerSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    longUrl = serializers.CharField(max_length=1000)

from rest_framework import serializers


class UTMSerializer(serializers.Serializer):
    utm_source = serializers.CharField(required=False, allow_blank=True)
    utm_medium = serializers.CharField(required=False, allow_blank=True)
    utm_campaign = serializers.CharField(required=False, allow_blank=True)
    utm_term = serializers.CharField(required=False, allow_blank=True)
    utm_content = serializers.CharField(required=False, allow_blank=True)

class MessageSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()
    message = serializers.CharField(max_length=4096)
    value = serializers.CharField(max_length=4096)
    name = serializers.CharField(max_length=4096)
    quiz = serializers.CharField(max_length=4096)
    utm = UTMSerializer(required=False)

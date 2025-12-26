from rest_framework import serializers

class UTMSerializer(serializers.Serializer):
    utm_source = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    utm_medium = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    utm_campaign = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    utm_term = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    utm_content = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class MessageSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()
    message = serializers.CharField(max_length=40960)
    value = serializers.CharField(max_length=40960)
    name = serializers.CharField(max_length=40960)
    quiz = serializers.CharField(max_length=40960, required=False, allow_blank=True)
    utm = UTMSerializer(required=False)
from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()
    message = serializers.CharField(max_length=4096)
    value = serializers.CharField(max_length = 4096)
    name = serializers.CharField(max_length = 4096)

from rest_framework.response import Response
from Lending.models import Settings
from rest_framework.views import APIView
from rest_framework import status
from .serializers import MessageSerializer
from .telegram_bot import send_message
import asyncio

class ApiBotView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            chat_id = serializer.validated_data['chat_id']
            message = serializer.validated_data['message']
            settings = Settings.objects.first()
            try:
                asyncio.run(send_message(chat_id, message, settings.botTelegramToken))
                return Response({"status": "message sent"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

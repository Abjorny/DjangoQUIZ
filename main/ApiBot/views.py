from rest_framework.response import Response
from Lending.models import Settings
from rest_framework.views import APIView
from rest_framework import status
from .serializers import MessageSerializer
from Lending.models import LendingPage
from .telegram_bot import send_message
import asyncio, requests, threading

class ApiBotView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            utm_content = request.GET.get('utm_content', "")
            host = request.get_host()
            lengingPage = LendingPage.objects.filter(
                domain = str(host)
            ).first()
            print(host)
            print(request.META.get("HTTP_HOST"))
            print(request.META.get("HTTP_X_FORWARDED_HOST"))
            print(request.META)

            if lengingPage and lengingPage.is_crm:
                value = serializer.validated_data['value']
                name = serializer.validated_data['name']
                requests.post(
                    url= "https://delivery-boost.ru/toamo.php",
                    data = {
                        "value": value,
                        "name": name,
                        "utm_content": utm_content
                    }
                )

            chat_id = serializer.validated_data['chat_id']
            message = serializer.validated_data['message']
            settings = Settings.objects.first()
            try:
                asyncio.run(send_message(chat_id, message, settings.botTelegramToken))
                return Response({"status": "message sent"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

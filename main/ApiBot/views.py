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
            parts = host.split('.')
            subdomain = parts[0] if len(parts) > 2 else None
            lengingPage = LendingPage.objects.filter(
                domain = str(host)
            ).first()
            chat_id = serializer.validated_data['chat_id']
            message = serializer.validated_data['message']
            if lengingPage and lengingPage.is_crm:
                try:
                    value = serializer.validated_data['value']
                    name = serializer.validated_data['name']
                    data = {
                            "phone": value,
                            "name": message,
                            "utm_content": utm_content,
                            "utm_term": "",
                            "utm_campaign": "deliv_poisk_rf",
                            "utm_medium": "cpc",
                            "utm_source" : "yandex_cpc",
                            "domain": str(subdomain) 
                    }
                    requests.post(
                        url= "https://delivery-boost.ru/toamo.php",
                        data = data
                    )
                except:
                    pass




            settings = Settings.objects.first()
            try:
                asyncio.run(send_message(chat_id, message, settings.botTelegramToken))
                return Response({"status": "message sent"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from Lending.models import Settings
from rest_framework.views import APIView
from rest_framework import status
from .serializers import MessageSerializer
from Lending.models import LendingPage
from .telegram_bot import send_message
import asyncio, requests, threading
from django.utils.html import strip_tags

class ApiBotView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        print( request.data)
        if not serializer.is_valid():
            print("uncurrct")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        chat_id = data.get('chat_id')
        message = data.get('message')
        value = data.get('value')
        name = data.get('name')
        quiz = strip_tags(data.get('quiz', ''))
        utm = data.get('utm', {}) 

        host = request.get_host()
        parts = host.split('.')
        subdomain = parts[0] if len(parts) > 2 else None

        lendingPage = LendingPage.objects.filter(domain=str(host)).first()
        print("lend", lendingPage)
        if lendingPage and lendingPage.is_crm:
            try:
                crm_data = {
                    "phone": value,
                    "name": name,
                    "quiz": quiz,
                    "utm_source": utm.get("utm_source", ""),
                    "utm_medium": utm.get("utm_medium", ""),
                    "utm_campaign": utm.get("utm_campaign", ""),
                    "utm_term": utm.get("utm_term", ""),
                    "utm_content": utm.get("utm_content", ""),

                    "domain": str(subdomain),
                }
                print("ok")

                requests.post(
                    url="https://delivery-boost.ru/toamo.php",
                    data=crm_data,
                    timeout=5
                )

                print("gocrm")
            except Exception as e:
                print("CRM error:", e)

        settings = Settings.objects.first()

        try:
            print("sendtg")
            asyncio.run(
                send_message(chat_id, message, settings.botTelegramToken)
            )
            return Response({"status": "message sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

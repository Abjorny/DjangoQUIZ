from django.urls import path
from .views import ApiBotView

urlpatterns = [
    path('send-message/', ApiBotView.as_view(), name='send-message'),
]

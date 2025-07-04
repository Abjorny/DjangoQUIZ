from Lending.views import index, polit
from django.urls import path, include

urlpatterns = [
    path('', index),
     path('polit', polit,name = "polit"),
     path('api/', include('ApiBot.urls')),
]

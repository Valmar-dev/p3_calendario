from django.shortcuts import render

# evento/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from .serializers import EventoSerializer

class EventoCadastro(APIView):  
    def post(self, request):
        serializer = EventoSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()
            return Response({
                "message": "Evento cadastrado com sucesso!",
                "evento": serializer.data  # Dados do evento cadastrado
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Erro ao cadastrar evento.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render

# evento/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from .serializers import EventoSerializer

class EventoList(APIView):
    def get(self, request):
        # Pega os parâmetros da query string
        ano = request.query_params.get('ano')
        mes = request.query_params.get('mes')

        # Verifica se ambos os parâmetros foram fornecidos
        if not ano or not mes:
            return Response(
                {"error": "Parâmetros 'ano' e 'mes' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtra os eventos pelo ano e mês
        eventos = Evento.objects.filter(data__year=ano, data__month=mes)
        serializer = EventoSerializer(eventos, many=True)  # Converte os eventos para o formato JSON
        return Response(serializer.data, status=status.HTTP_200_OK)

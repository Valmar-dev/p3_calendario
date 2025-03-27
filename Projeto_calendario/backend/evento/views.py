from functools import cache
from django.core.cache import cache
from django.shortcuts import render

# evento/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from .serializers import EventoSerializer
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta
from django.db import models


# Cadastro de eventos. Método POST
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


# Retornando dados do baco para o front. Método GET
class EventoList(APIView):
    def get(self, request):
        # Pega os parâmetros mes e dia da query string
        mes = request.GET.get("mes")
        dia = request.GET.get("dia")

        if not mes or not dia:
            return Response({"message": "Informe 'mes' e 'dia' como parâmetros na URL."}, status=400)
        
        try:
            # Converte mes e dia para inteiros
            mes = int(mes)
            dia = int(dia)
        except ValueError:
            return Response({"message": "Os parâmetros 'mes' e 'dia' devem ser números inteiros."}, status=400)

        # Filtra os eventos de acordo com o mês e o dia
        eventos = Evento.objects.filter(ultima_data__month=mes, ultima_data__day=dia)

        # Serializa os eventos encontrados
        serializer = EventoSerializer(eventos, many=True)
        
        return Response(serializer.data)  # Retorna a lista de eventos em formato JSON


# rota para ajudar a verificar as notificações, coleta tambem o ano
class EventosProximos30Dias(APIView):
    def get(self, request):
        try:
            # Chave de cache única por dia
            hoje = datetime.now().date()
            cache_key = f"eventos_30dias_{hoje}"
            
            # Busca no cache
            eventos_cache = cache.get(cache_key)
            
            if eventos_cache is not None:
                return Response(eventos_cache)
            
            # Se não estiver no cache, busca no banco
            data_futura = hoje + timedelta(days=30)
            eventos = Evento.objects.filter(
                ultima_data__range=[hoje, data_futura]
            ).order_by('ultima_data')
            
            serializer = EventoSerializer(eventos, many=True)
            dados_serializados = serializer.data
            
            # Armazena no cache
            cache.set(cache_key, dados_serializados, timeout=86400)  # 24h
            
            return Response(dados_serializados)
            
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar eventos: {str(e)}"},
                status=500
            )

# Fução para deletar. Método DELETE
class EventoDelete(APIView):
    def delete(self, request, pk):
        try:
            evento = Evento.objects.get(id=pk)  # Busca o evento pelo id
            evento.delete()  # Deleta o evento
            return Response({"message": "Evento deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT) # Mensagem de confirmação
        except Evento.DoesNotExist:
            raise NotFound(detail="Evento não encontrado")

# Função para atualizar. Método PUT
class EventoUpdate(APIView):
    def put(self, request, pk):
        try:
            evento = Evento.objects.get(pk=pk)  # Encontra o evento através id (pk)
        except Evento.DoesNotExist:
            return Response({"error": "Evento não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventoSerializer(evento, data=request.data)  # Atualiza com os dados enviados no corpo da requisição
        if serializer.is_valid():
            serializer.save()  # Salva as atualizações
            return Response({"message": "Evento atualizado com sucesso!", "evento": serializer.data}, status=status.HTTP_200_OK) # Mensagem de que confirmação
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# Função para GET para receber apenas um evento
class EventoDetail(APIView):
    def get(self, request, id):
        # Tenta buscar o evento pelo ID. Se não encontrar, retorna 404 automaticamente.
        evento = get_object_or_404(Evento, id=id)
        
        # Verifica se o evento existe no banco, caso contrário retorna uma mensagem de erro
        if not evento:
            return Response({"message": "Nenhum evento encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Serializa o evento encontrado
        serializer = EventoSerializer(evento)
        
        # Retorna o evento serializado com status 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EventoMensal(APIView):
    def get(self, request):
        ano = request.GET.get("ano")
        mes = request.GET.get("mes")

        if not ano or not mes:
            return Response({"message": "Os parâmetros 'ano' e 'mes' são obrigatórios."}, status=400)

        try:
            ano = int(ano)
            mes = int(mes)
        except ValueError:
            return Response({"message": "Os parâmetros 'ano' e 'mes' devem ser números inteiros."}, status=400)
        
        eventos = Evento.objects.filter(
            data__year__lte=ano,
            ultima_data__year__gte=ano,
            data__month__lte=mes,
            ultima_data__month__gte=mes
        )
        
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)



class EventoSempre(APIView):
    def get(self, request):
        mes = request.GET.get("mes")

        if not mes:
            return Response({"message": "Os parâmetros 'mes' é obrigatório."}, status=400)

        try:
            mes = int(mes)
        except ValueError:
            return Response({"message": "Os parâmetros 'mes' deve ser números inteiro."}, status=400)
        eventos = Evento.objects.filter(sempre=True, ultima_data__month=mes)

        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)  # Retorna a lista de eventos no formato JSON

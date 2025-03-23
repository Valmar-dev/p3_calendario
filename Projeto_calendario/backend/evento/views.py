from django.shortcuts import render

# evento/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from .serializers import EventoSerializer
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

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
        eventos = Evento.objects.filter(data__month=mes, data__day=dia)

        # Serializa os eventos encontrados
        serializer = EventoSerializer(eventos, many=True)
        
        return Response(serializer.data)  # Retorna a lista de eventos em formato JSON


    

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
        evento = get_object_or_404(Evento, id=id)  # Busca evento pelo ID ou retorna 404
        serializer = EventoSerializer(evento)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Funão para buscar apenas o mes e ano GET
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
        eventos = Evento.objects.filter(data__year=ano, data__month=mes)
        if not eventos.exists():
            return Response({"message": "Nenhum evento encontrado para esse mês."}, status=404)
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)  # Retorna a lista de eventos no formato JSON

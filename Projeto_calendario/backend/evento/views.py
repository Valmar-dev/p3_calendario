from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json
from calendario.firebase_config import enviar_notificacao
from .utils import ler_token  # Importe a função



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
        eventos = Evento.objects.filter(ultima_data__month=mes, ultima_data__day=dia)

        # Serializa os eventos encontrados
        serializer = EventoSerializer(eventos, many=True)
        
        return Response(serializer.data)  # Retorna a lista de eventos em formato JSON

# retornar eventos que tenham sempre = true
class EventoSempre(APIView):
    def get(self, request):
        # Pega os parâmetros mês e ano da query string
        mes = request.GET.get("mes")

        if not mes:
            return Response({"message": "Informe 'mes' e 'ano' como parâmetros na URL."}, status=400)
        
        try:
            mes = int(mes)
            ano = int(ano)
        except ValueError:
            return Response({"message": "Os parâmetros 'mes' e 'ano' devem ser números inteiros."}, status=400)

        # Filtra apenas os eventos que têm 'sempre=True'
        eventos = Evento.objects.filter(sempre=True, data__month=mes)

        serializer = EventoSerializer(eventos, many=True)
        
        return Response(serializer.data)
    

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
        eventos = Evento.objects.filter(ultima_data__year=ano, ultima_data__month=mes)
        if not eventos.exists():
            return Response({"message": "Nenhum evento encontrado para esse mês."}, status=404)
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)  # Retorna a lista de eventos no formato JSON

@csrf_exempt
def verificar_eventos(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = data.get("token")  # Token do Firebase do usuário

        if not token:
            return JsonResponse({"error": "Token não fornecido"}, status=400)

        hoje = datetime.today().date()
        um_mes_antes = hoje + timedelta(days=30)  # Data de um mês antes
        um_dia_antes = hoje + timedelta(days=1)   # Data de um dia antes

        eventos = Evento.objects.all()
        notificacoes_enviadas = 0

        for evento in eventos:
            if evento.data:
                evento_data = evento.data  # Já está no formato YYYY-MM-DD no banco

                # Verifica se o evento ocorre 1 mês antes ou 1 dia antes
                if evento_data == um_mes_antes or evento_data == um_dia_antes:
                    titulo = "Lembrete de Evento"
                    mensagem = f"O evento '{evento.descricao}' ocorrerá em {evento_data}!"
                    response = enviar_notificacao(token, titulo, mensagem)
                    print(f"Notificação enviada: {response}")
                    notificacoes_enviadas += 1

        return JsonResponse({"message": f"{notificacoes_enviadas} notificações enviadas!"})
    
    return JsonResponse({"error": "Método inválido"}, status=400)


@csrf_exempt
def registrar_token(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            token = body.get('token', None)

            if token:
                salvar_token(token)  # Salva o token usando a função do utils.py

                return JsonResponse({"status": "sucesso", "message": "Token recebido com sucesso"})
            else:
                return JsonResponse({"status": "erro", "message": "Token não fornecido"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "erro", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "erro", "message": "Método não permitido"}, status=405)
    

def verificar_eventos(request):
    if request.method == "POST":
        token = ler_token()  # Lê o token usando a função do utils.py

        if not token:
            return JsonResponse({"error": "Token não encontrado"}, status=400)

        hoje = datetime.today().date()
        um_mes_antes = hoje + timedelta(days=30)  # Data de um mês antes
        um_dia_antes = hoje + timedelta(days=1)   # Data de um dia antes

        eventos = Evento.objects.all()
        notificacoes_enviadas = 0

        for evento in eventos:
            if evento.data:
                evento_data = evento.data  # Já está no formato YYYY-MM-DD no banco

                # Verifica se o evento ocorre 1 mês antes ou 1 dia antes
                if evento_data.date() == um_mes_antes.date() or evento_data.date() == um_dia_antes.date():
                    titulo = "Lembrete de Evento"
                    mensagem = f"O evento '{evento.descricao}' ocorrerá em {evento_data}!"
                    response = enviar_notificacao(token, titulo, mensagem)
                    print(f"Notificação enviada: {response}")
                    notificacoes_enviadas += 1

        return JsonResponse({"message": f"{notificacoes_enviadas} notificações enviadas!"})
    
    return JsonResponse({"error": "Método inválido"}, status=400)
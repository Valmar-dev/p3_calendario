import firebase_admin
from firebase_admin import credentials, messaging

# Carregar credenciais do Firebase com o caminho correto para o arquivo JSON
cred = credentials.Certificate("C:/Users/ezequ/OneDrive/Documentos/Estudos/p3_calendario/Projeto_calendario/backend/calendario/callendario-51b66-firebase-adminsdk-fbsvc-4e733100e0.json")
firebase_admin.initialize_app(cred)

def enviar_notificacao(token, titulo, mensagem):
    """Envia uma notificação push para um dispositivo"""
    notificacao = messaging.Message(
        notification=messaging.Notification(title=titulo, body=mensagem),
        token=token
    )
    try:
        # Envia a notificação
        response = messaging.send(notificacao)
        return response
    except Exception as e:
        return str(e)

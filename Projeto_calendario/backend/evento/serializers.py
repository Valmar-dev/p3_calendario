# evento/serializers.py
from rest_framework import serializers
from .models import Evento  # Importa o modelo Evento

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'  # Aqui você pode listar os campos ou usar '__all__' para incluir todos

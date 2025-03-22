# evento/serializers.py
from rest_framework import serializers
from .models import Evento  # Importa o modelo Evento

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'  

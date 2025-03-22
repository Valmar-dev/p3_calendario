from django.core.validators import RegexValidator
from django.db import models

class Evento(models.Model):
    descricao = models.TextField()
    data = models.DateTimeField()
    ultima_data = models.DateTimeField(null=True, blank=True)
    sempre = models.BooleanField(default=False)
    cor = models.CharField(
        max_length=7,  # Exemplo: "#FFFFFF"
        validators=[RegexValidator(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$', message="Insira um código hexadecimal válido.")],
    )

from django.db import models

class Evento(models.Model):
    data = models.DateTimeField()  # Armazena o ano e o mes do evento

    def __str__(self):
        return str(self.data)  # Exibe a data do evento no admin, por exemplo


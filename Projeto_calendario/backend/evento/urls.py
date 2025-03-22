# evento/urls.py
from django.urls import path
from .views import EventoCadastro, EventoList

urlpatterns = [
    path('cadastro/', EventoCadastro.as_view(), name='evento-cadastro'),
    path('eventos/', EventoList.as_view(), name='retorna-eventos'),
]
